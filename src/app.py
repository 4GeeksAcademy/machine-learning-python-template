"""Sentiment inference for WeLoveReviews customer reviews.

Reads data/raw/reviews.csv, predicts a 1-5 star sentiment for every review with a
pinned Hugging Face model and writes data/processed/reviews_with_sentiment.csv.

Usage:
    python src/app.py
"""

import time
from pathlib import Path

import pandas as pd
from transformers import pipeline

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "raw" / "reviews.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "reviews_with_sentiment.csv"

# Pinned model: name + exact commit on the Hugging Face Hub
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
MODEL_REVISION = "8f6f4e3a8f70be4b65d3a4a8762b6d781cda240d"
BATCH_SIZE = 32

# Below this probability the prediction is flagged for human review (see explore.ipynb, section 6)
LOW_CONFIDENCE_THRESHOLD = 0.5


def star_band(stars: int) -> str:
    if stars <= 2:
        return "Negativo"
    if stars == 3:
        return "Neutral"
    return "Positivo"


def load_reviews(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = {"review_id", "rating", "review_text"} - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")
    df["review_text"] = df["review_text"].fillna("").str.strip().str.replace(r"\s+", " ", regex=True)
    return df


def load_model():
    return pipeline(
        "text-classification",
        model=MODEL_NAME,
        revision=MODEL_REVISION,
        truncation=True,
        device=-1,
    )


def predict(df: pd.DataFrame, classifier) -> pd.DataFrame:
    predictions = classifier(df["review_text"].tolist(), batch_size=BATCH_SIZE)

    out = df.copy()
    out["pred_stars"] = [int(p["label"].split()[0]) for p in predictions]  # "4 stars" -> 4
    out["pred_score"] = [round(p["score"], 4) for p in predictions]
    out["sentiment"] = out["pred_stars"].map(star_band)
    out["rating_band"] = out["rating"].map(star_band)
    out["band_match"] = out["sentiment"] == out["rating_band"]
    out["false_negative"] = (out["rating"] >= 4) & (out["pred_stars"] <= 2)
    out["needs_review"] = out["pred_score"] < LOW_CONFIDENCE_THRESHOLD
    out["model"] = f"{MODEL_NAME}@{MODEL_REVISION[:7]}"
    return out


def print_summary(df: pd.DataFrame) -> None:
    bands = ["Positivo", "Neutral", "Negativo"]
    summary = pd.DataFrame({
        "estrellas (%)": df["rating_band"].value_counts(normalize=True).mul(100),
        "modelo (%)": df["sentiment"].value_counts(normalize=True).mul(100),
    }).reindex(bands).fillna(0).round(1)

    print(summary.to_string())
    print(f"\nMedia de estrellas: cliente {df['rating'].mean():.2f} | modelo {df['pred_stars'].mean():.2f}")
    print(f"Coincidencia de banda: {df['band_match'].mean():.1%}")
    print(f"Falsos negativos (4-5★ -> 1-2★): {df['false_negative'].sum()}")
    print(f"Marcadas para revisión (confianza < {LOW_CONFIDENCE_THRESHOLD}): {df['needs_review'].sum()}")


def main() -> None:
    reviews = load_reviews(RAW_PATH)
    print(f"Reseñas cargadas: {len(reviews)}")

    t0 = time.perf_counter()
    classifier = load_model()  # loaded once, reused for every batch
    print(f"Modelo {MODEL_NAME} ({MODEL_REVISION[:7]}) cargado en {time.perf_counter() - t0:.1f} s")

    t0 = time.perf_counter()
    enriched = predict(reviews, classifier)
    print(f"Inferencia completada en {time.perf_counter() - t0:.1f} s\n")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(OUTPUT_PATH, index=False)

    print_summary(enriched)
    print(f"\nGuardado en {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
