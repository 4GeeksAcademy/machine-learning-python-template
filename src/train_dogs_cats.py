"""Entrena EfficientNet-B0 con el dataset etiquetado Dogs vs. Cats."""

import argparse
import csv
import json
import random
import re
import shutil
import tempfile
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

URL = "https://storage.googleapis.com/datascience-materials/dogs-vs-cats.zip"
CLASSES = ("cat", "dog")
SIZE = (200, 200)
SEED = 42
FILENAME = re.compile(r"(cat|dog)\.(\d+)\.jpg", re.IGNORECASE)


def collect_images(raw):
    raw.mkdir(parents=True, exist_ok=True)
    files = [p for p in raw.rglob("*.jpg") if FILENAME.fullmatch(p.name)]
    if not files:
        archive = raw / "dogs-vs-cats.zip"
        if not archive.exists():
            with tempfile.TemporaryDirectory(dir=raw) as temporary:
                download = Path(temporary) / archive.name
                urlretrieve(URL, download)
                download.replace(archive)
        with tempfile.TemporaryDirectory(dir=raw) as temporary:
            stage = Path(temporary)

            def extract_images(source):
                for member in source.infolist():
                    name = Path(member.filename).name
                    if FILENAME.fullmatch(name):
                        destination = stage / name.lower()
                        with source.open(member) as original, destination.open("xb") as image:
                            shutil.copyfileobj(original, image)

            with ZipFile(archive) as source:
                extract_images(source)
                if not any(stage.glob("*.jpg")):
                    nested = next(
                        (m for m in source.namelist() if Path(m).name == "train.zip"),
                        None,
                    )
                    if nested is not None:
                        with source.open(nested) as training, ZipFile(training) as images:
                            extract_images(images)
            files = sorted(stage.glob("*.jpg"))
            if not files:
                raise ValueError(f"No se encontraron imágenes etiquetadas en {archive}")
            destination = raw / "train"
            destination.mkdir(exist_ok=True)
            files = [path.replace(destination / path.name) for path in files]

    if len({p.name.lower() for p in files}) != len(files):
        raise ValueError("Se encontraron nombres de imagen duplicados en los datos de origen.")
    return sorted(files, key=lambda p: (p.name.split(".")[0], int(p.name.split(".")[1])))


def partition(files):
    splits = {name: [] for name in ("train", "validation", "test")}
    rng = random.Random(SEED)
    for label, name in enumerate(CLASSES):
        rows = [(path, label) for path in files if path.name.lower().startswith(name + ".")]
        if len(rows) < 10:
            raise ValueError(f"Se necesitan al menos diez imágenes de la clase {name}.")
        rng.shuffle(rows)
        holdout = len(rows) // 10
        splits["test"].extend(rows[:holdout])
        splits["validation"].extend(rows[holdout:2 * holdout])
        splits["train"].extend(rows[2 * holdout:])
    return splits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=Path("data/raw/dogs-vs-cats"))
    parser.add_argument("--processed", type=Path, default=Path("data/processed"))
    parser.add_argument("--models", type=Path, default=Path("models"))
    parser.add_argument("--mode", choices=("directory", "ram"), default="directory")
    parser.add_argument("--epochs", type=int, default=25)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()
    if min(args.epochs, args.batch_size) < 1:
        parser.error("--epochs y --batch-size deben ser positivos")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from tensorflow import keras
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    keras.utils.set_random_seed(SEED)
    files = collect_images(args.raw)
    splits = partition(files)
    args.processed.mkdir(parents=True, exist_ok=True)
    args.models.mkdir(parents=True, exist_ok=True)

    for name in ("dog", "cat"):
        examples = [p for p in files if p.name.lower().startswith(name + ".")][:9]
        fig, axes = plt.subplots(3, 3, figsize=(9, 9), layout="constrained")
        for axis, path in zip(axes.flat, examples):
            with keras.utils.load_img(path) as img:
                axis.imshow(img)
                axis.set_title(f"{path.name} · {img.width} × {img.height}")
            axis.axis("off")
        fig.savefig(args.processed / f"examples_{name}.png", dpi=120)
        plt.close(fig)

    def directory_data(root, split):
        for name in CLASSES:
            (root / split / name).mkdir(parents=True)
        for path, label in splits[split]:
            target = root / split / CLASSES[label] / path.name
            try:
                target.hardlink_to(path.resolve())
            except OSError:
                shutil.copyfile(path, target)
        return ImageDataGenerator().flow_from_directory(
            root / split, classes=list(CLASSES), target_size=SIZE,
            interpolation="bilinear", class_mode="sparse",
            batch_size=args.batch_size, shuffle=split == "train", seed=SEED,
        )

    class ImageBatches(keras.utils.PyDataset):
        def __init__(self, rows, shuffle):
            super().__init__()
            photos = np.empty((len(rows), *SIZE, 3), dtype=np.uint8)
            labels = np.array([label for _, label in rows], dtype=np.int32)
            for index, (path, _) in enumerate(rows):
                with keras.utils.load_img(path, target_size=SIZE, interpolation="bilinear") as img:
                    photos[index] = np.asarray(img)
            self.photos, self.labels = (photos, labels)
            self.indices = np.arange(len(rows))
            self.shuffle = shuffle
            self.rng = np.random.default_rng(SEED)
            self.on_epoch_end()

        def __len__(self):
            return (len(self.indices) + args.batch_size - 1) // args.batch_size

        def __getitem__(self, index):
            start = index * args.batch_size
            indices = self.indices[start:start + args.batch_size]
            return self.photos[indices], self.labels[indices]

        def on_epoch_end(self):
            if self.shuffle:
                self.rng.shuffle(self.indices)

    with (
        tempfile.TemporaryDirectory(prefix="dogs-cats-", dir=args.processed) as temporary,
        tempfile.TemporaryDirectory(prefix="checkpoint-", dir=args.models) as model_stage,
    ):
        if args.mode == "directory":
            trdata = directory_data(Path(temporary), "train")
            validation = directory_data(Path(temporary), "validation")
            tsdata = directory_data(Path(temporary), "test")
            test_names, test_labels = tsdata.filenames, tsdata.classes
        else:
            trdata = ImageBatches(splits["train"], shuffle=True)
            validation = ImageBatches(splits["validation"], shuffle=False)
            tsdata = ImageBatches(splits["test"], shuffle=False)
            test_names = [path.name for path, _ in splits["test"]]
            test_labels = tsdata.labels

        model = keras.Sequential([
            keras.Input(shape=(*SIZE, 3)),
            keras.applications.EfficientNetB0(
                include_top=False, weights=None, input_shape=(*SIZE, 3),
            ),
            keras.layers.GlobalAveragePooling2D(),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(2, activation="softmax"),
        ])
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                      metrics=["accuracy"])
        from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

        checkpoint = Path(model_stage) / "dogs_vs_cats.keras"
        history = model.fit(
            trdata, validation_data=validation, epochs=args.epochs,
            callbacks=[
                ModelCheckpoint(checkpoint, monitor="val_loss", save_best_only=True),
                EarlyStopping(monitor="val_loss", patience=5),
            ],
        )
        best = keras.models.load_model(checkpoint)
        scores = best.evaluate(tsdata, return_dict=True)
        probabilities = best.predict(tsdata)
        checkpoint.replace(args.models / checkpoint.name)

    with (args.processed / "dogs_vs_cats_predictions.csv").open("w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["image", "actual", "predicted", "p_cat", "p_dog"])
        for name, label, row in zip(test_names, test_labels, probabilities, strict=True):
            writer.writerow([name, CLASSES[label], CLASSES[row.argmax()], *row.tolist()])

    report = {
        "split_sizes": {name: len(rows) for name, rows in splits.items()},
        "best_epoch": int(np.argmin(history.history["val_loss"])) + 1,
        "test": {name: float(value) for name, value in scores.items()},
    }
    (args.processed / "dogs_vs_cats_metrics.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
