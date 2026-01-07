from utils import db_connect
engine = db_connect()

# your code here

import os
import pandas as pd
from sklearn.model_selection import train_test_split


RAW_PATH = os.path.join("data", "raw", "AB_NYC_2019.csv")
OUT_DIR = os.path.join("data", "processed")


def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError("No existe el archivo en: " + path)
    return pd.read_csv(path)


def clean_data(df):
    df_clean = df.copy()

    df_clean["last_review"] = pd.to_datetime(df_clean["last_review"], errors="coerce")
    df_clean["reviews_per_month"] = df_clean["reviews_per_month"].fillna(0)

    df_clean["name"] = df_clean["name"].fillna("unknown")
    df_clean["host_name"] = df_clean["host_name"].fillna("unknown")

    df_clean = df_clean[df_clean["price"].between(1, 500)]

    return df_clean


def split_and_save(df, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    train_path = os.path.join(out_dir, "train.csv")
    test_path = os.path.join(out_dir, "test.csv")

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print("Guardado train en:", train_path)
    print("Guardado test en:", test_path)
    print("train shape:", train_df.shape)
    print("test shape:", test_df.shape)


def main():
    df = load_data(RAW_PATH)
    df_clean = clean_data(df)
    split_and_save(df_clean, OUT_DIR)


if __name__ == "__main__":
    main()

