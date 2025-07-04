import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline # Pipeline is used within ColumnTransformer setup

def load_bank_data(url="https://raw.githubusercontent.com/4GeeksAcademy/logistic-regression-project-tutorial/main/bank-marketing-campaign-data.csv"):
    """
    Loads the bank marketing campaign dataset directly from a URL.
    The separator is specified as ';'.
    """
    try:
        df = pd.read_csv(url, sep=';')
        print("Bank Marketing Dataset loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading bank marketing data: {e}")
        return None

def preprocess_bank_data(df):
    """
    Performs preprocessing for the bank marketing dataset:
    - Converts the 'y' target variable to numerical (0 for 'no', 1 for 'yes').
    - Identifies numerical and categorical columns.
    - Creates and returns a ColumnTransformer (preprocessor) for scaling numerical
      features and one-hot encoding categorical features.
    - Returns X, y, the preprocessor, and the lists of numerical/categorical columns.
    """
    if df is None:
        return None, None, None, None, None

    df_processed = df.copy()

    # Convert 'y' to numerical (0 for 'no', 1 for 'yes')
    df_processed['y'] = df_processed['y'].map({'no': 0, 'yes': 1})
    print("Target variable 'y' converted to numerical (0/1).")

    # Define features (X) and target (y)
    X = df_processed.drop('y', axis=1)
    y = df_processed['y']

    # Identify numerical and categorical columns dynamically
    numerical_cols = X.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = X.select_dtypes(include='object').columns.tolist()

    print(f"Identified Numerical Columns for Preprocessing: {numerical_cols}")
    print(f"Identified Categorical Columns for Preprocessing: {categorical_cols}")

    # Create preprocessors for numerical and categorical columns
    numerical_transformer = StandardScaler() # Standardize numerical features
    categorical_transformer = OneHotEncoder(handle_unknown='ignore') # One-hot encode categorical features

    # Combine transformers using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ],
        remainder='passthrough' # Keep any other columns that were not specified
    )
    print("ColumnTransformer for preprocessing created.")
    return X, y, preprocessor, numerical_cols, categorical_cols

def split_train_test_data(X, y, test_size=0.2, random_state=42, stratify_by_y=True):
    """
    Splits the features (X) and target (y) into training and testing sets.
    Uses stratification by default to maintain class balance in both sets.
    """
    if X is None or y is None:
        return None, None, None, None

    stratify_param = y if stratify_by_y else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=stratify_param
    )
    print(f"Data split into training (shape: {X_train.shape}) and testing (shape: {X_test.shape}) sets.")
    print(f"y_train 'yes' proportion: {y_train.value_counts(normalize=True).get(1, 0):.4f}")
    print(f"y_test 'yes' proportion: {y_test.value_counts(normalize=True).get(1, 0):.4f}")
    return X_train, X_test, y_train, y_test
