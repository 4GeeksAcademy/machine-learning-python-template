import pandas as pd
from transformers import pipeline

MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"


def stars_to_sentiment(label: str) -> str:
    try:
        star = int(str(label).split()[0])

        if not 1 <= star <= 5:
            return "UNKNOWN"

        if star <= 2:
            return "NEGATIVE"

        if star == 3:
            return "NEUTRAL"

        return "POSITIVE"

    except (ValueError, IndexError):
        return "UNKNOWN"


def load_reviews(path="data/raw/reviews.csv"):
    return pd.read_csv(path)


def run_inference(df, classifier):
    results = classifier(df["review_text"].tolist(), truncation=True, batch_size=16)
    df["predicted_stars"] = [int(result["label"].split()[0]) for result in results]
    df["predicted_sentiment"] = [stars_to_sentiment(result["label"]) for result in results]
    df["confidence"] = [round(result["score"], 4) for result in results]
    return df


def write_output(df, path="data/processed/reviews_with_sentiment.csv"):
    df.to_csv(path, index=False)


def main():
    classifier = pipeline("text-classification", model=MODEL_NAME)

    df = load_reviews()
    df = run_inference(df, classifier)
    write_output(df)

    print(f"Total reviews analyzed: {len(df)}")
    print(f"Mean star rating: {df['rating'].mean():.2f} / 5")
    print("Sentiment breakdown (from nlptown model):")
    counts = df["predicted_sentiment"].value_counts()
    for band in ["POSITIVE", "NEUTRAL", "NEGATIVE"]:
        n = counts.get(band, 0)
        print(f"  {band}: {n} ({n / len(df):.1%})")


if __name__ == "__main__":
    main()


