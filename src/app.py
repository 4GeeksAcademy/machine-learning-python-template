import argparse
import re
from pathlib import Path

import pandas as pd
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "nlptown/bert-base-multilingual-uncased-sentiment"

BANDS = {
    1: "Negativo",
    2: "Negativo",
    3: "Neutral",
    4: "Positivo",
    5: "Positivo",
}


def analyse_reviews(input_path, output_path, batch_size=16):
    if batch_size < 1:
        raise ValueError("batch_size must be positive.")

    # Reuse the exact revision recorded during notebook analysis.
    revision = (ROOT / "model_revision.txt").read_text().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("model_revision.txt must contain a model commit SHA.")

    df = pd.read_csv(input_path)

    required = {"review_id", "rating", "review_text"}
    if not required.issubset(df.columns):
        raise ValueError(f"Required columns: {sorted(required)}")

    if df.empty or df["review_id"].isna().any():
        raise ValueError("The dataset is empty or contains missing IDs.")

    if not df["review_id"].is_unique:
        raise ValueError("Review IDs must be unique.")

    if not df["rating"].isin(BANDS).all():
        raise ValueError("Ratings must be integers from 1 to 5.")

    texts = df["review_text"]
    if texts.isna().any() or texts.astype(str).str.strip().eq("").any():
        raise ValueError("Review texts must not be missing or blank.")

    texts = texts.astype(str).tolist()

    # Load once, outside the inference loop.
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=revision
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID, revision=revision
    )
    model.eval()

    label_to_stars = {}
    for label_id, label in model.config.id2label.items():
        match = re.fullmatch(r"([1-5]) stars?", label)
        if not match:
            raise ValueError(f"Unexpected model label: {label}")
        label_to_stars[int(label_id)] = int(match.group(1))

    max_length = model.config.max_position_embeddings
    token_lengths = [
        len(tokenizer.encode(text, truncation=False))
        for text in texts
    ]

    stars = []
    scores = []

    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            inputs = tokenizer(
                texts[start:start + batch_size],
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt",
            )

            probabilities = model(**inputs).logits.softmax(dim=-1)
            batch_scores, label_ids = probabilities.max(dim=-1)

            stars.extend(
                label_to_stars[label_id]
                for label_id in label_ids.tolist()
            )
            scores.extend(batch_scores.tolist())

    results = df.copy()
    results["predicted_stars"] = stars
    results["sentiment"] = results["predicted_stars"].map(BANDS)
    results["model_score"] = scores
    results["token_count"] = token_lengths
    results["was_truncated"] = results["token_count"] > max_length
    results["model_id"] = MODEL_ID
    results["model_revision"] = revision
    results["rating_sentiment"] = results["rating"].map(BANDS)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    print(f"Reviews processed: {len(results)}")
    print(f"Truncated texts: {results['was_truncated'].sum()}")
    print(f"Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Predict review sentiment using a fixed model revision."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data/raw/reviews.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data/processed/reviews_with_sentiment.csv",
    )
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()

    analyse_reviews(args.input, args.output, args.batch_size)


if __name__ == "__main__":
    main()