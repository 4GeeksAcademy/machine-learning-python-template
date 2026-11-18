"""Entrena y evalúa el agrupamiento de California Housing."""
import argparse
import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import classification_report, confusion_matrix, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

ROOT = Path(__file__).resolve().parent
FEATURES = ["Latitude", "Longitude", "MedInc"]
LABELS = list(range(6))
SEED = 42


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, help="Ruta opcional al housing.csv de 4Geeks.")
    args = parser.parse_args()
    if args.csv:
        data = pd.read_csv(args.csv)
    elif (ROOT / "housing.csv").is_file():
        data = pd.read_csv(ROOT / "housing.csv")
    else:
        data = fetch_california_housing(
            as_frame=True, data_home=ROOT / ".cache"
        ).data

    features = data[FEATURES].apply(pd.to_numeric, errors="raise")
    train, test = train_test_split(features, test_size=0.2, random_state=SEED)

    clustering = make_pipeline(
        StandardScaler(), KMeans(n_clusters=6, n_init=20, random_state=SEED)
    )
    clustering.fit(train)
    train_labels = clustering.predict(train)
    test_labels = clustering.predict(test)
    train = train.assign(cluster=pd.Categorical(train_labels, categories=LABELS))
    test = test.assign(cluster=pd.Categorical(test_labels, categories=LABELS))

    # Las clases proceden de regiones de Voronoi definidas en tres variables.
    # SVC lineal aprende una frontera por cada par de clases.
    classifier = make_pipeline(StandardScaler(), SVC(kernel="linear"))
    classifier.fit(train[FEATURES], train_labels)
    predicted = classifier.predict(test[FEATURES])

    results = ROOT / "results"
    models = ROOT / "models"
    results.mkdir(exist_ok=True)
    models.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 8), layout="constrained")
    scatter = ax.scatter(
        train.Longitude, train.Latitude, c=train_labels, cmap="tab10",
        vmin=0, vmax=9, s=9, alpha=0.4, label="Entrenamiento",
    )
    ax.scatter(
        test.Longitude, test.Latitude, c=test_labels, cmap="tab10",
        vmin=0, vmax=9, s=14, marker="x", alpha=0.75, label="Prueba",
    )
    ax.set(xlabel="Longitud", ylabel="Latitud", title="California Housing · seis clústeres")
    ax.legend()
    fig.colorbar(scatter, ax=ax, ticks=LABELS, label="Clúster")
    fig.savefig(results / "clusters.png", dpi=160)
    plt.close(fig)

    summary = (
        train.groupby("cluster", observed=True)
        .agg(block_groups=("MedInc", "size"), median_income=("MedInc", "median"),
             mean_latitude=("Latitude", "mean"), mean_longitude=("Longitude", "mean"))
    )
    summary.to_csv(results / "cluster_summary.csv")
    train.assign(split="train").to_csv(results / "train_clusters.csv", index=False)
    test.assign(split="test", supervised_cluster=predicted).to_csv(
        results / "test_clusters.csv", index=False
    )

    scaled_test = clustering.named_steps["standardscaler"].transform(test[FEATURES])
    metrics = {
        "train_rows": len(train),
        "test_rows": len(test),
        "test_silhouette": silhouette_score(
            scaled_test, test_labels, sample_size=min(3000, len(test)),
            random_state=SEED,
        ),
        "classification_report": classification_report(
            test_labels, predicted, labels=LABELS, output_dict=True, zero_division=0,
        ),
        "confusion_matrix_labels": LABELS,
        "confusion_matrix": confusion_matrix(
            test_labels, predicted, labels=LABELS
        ).tolist(),
    }
    report = json.dumps(metrics, indent=2)
    (results / "metrics.json").write_text(report + "\n", encoding="utf-8")
    joblib.dump(clustering, models / "kmeans.joblib")
    joblib.dump(classifier, models / "classifier.joblib")
    print(summary.to_string())
    print(report)


if __name__ == "__main__":
    main()
