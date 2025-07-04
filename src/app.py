import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
import joblib
import os

# Import functions from your utils.py
from src.utils import load_bank_data, preprocess_bank_data, split_train_test_data

def perform_eda_summary(df, numerical_cols, categorical_cols):
    """
    Performs a summary of Exploratory Data Analysis (EDA) on the raw DataFrame.
    This is a text-based summary for the main app.py script.
    Full interactive EDA with plots is expected to be done in explore.ipynb.
    """
    print("\n--- Starting EDA Summary ---")
    print("DataFrame Info:")
    df.info()
    print("\nDescriptive Statistics for Numerical Features:")
    print(df[numerical_cols].describe())

    print("\nValue Counts for Categorical Features (Top 5 for brevity):")
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n--- {col} ---")
            print(df[col].value_counts().head())

    print("\nDistribution of the Target Variable 'y' (before conversion):")
    print(df['y'].value_counts())
    print(df['y'].value_counts(normalize=True))

    # Example of saving a basic plot to processed data folder
    # This plot will show the distribution of the target variable
    plt.figure(figsize=(6, 4))
    sns.countplot(x='y', data=df)
    plt.title('Distribution of Target Variable (y)')
    os.makedirs('data/processed', exist_ok=True) # Ensure directory exists
    plt.savefig('data/processed/target_distribution_raw.png')
    plt.close() # Close plot to prevent display in non-notebook environments
    print("EDA summary plots saved to data/processed/")
    print("--- EDA Summary Complete ---")

def train_and_evaluate_model(pipeline, X_train, y_train, X_test, y_test, model_name="Logistic Regression", plot_cmap=plt.cm.Blues):
    """
    Trains a given pipeline model and evaluates its performance on the test set.
    Prints classification report, ROC AUC score, and saves a confusion matrix plot.
    """
    print(f"\n--- Training and Evaluating {model_name} Model ---")
    print(f"Training the {model_name} Model...")
    pipeline.fit(X_train, y_train)
    print(f"{model_name} Model training complete.")

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1] # Probabilities for the positive class (1: 'yes')

    print(f"\nClassification Report ({model_name} Model):")
    print(classification_report(y_test, y_pred))

    roc_auc = roc_auc_score(y_test, y_proba)
    print(f"\nROC AUC Score ({model_name} Model): {roc_auc:.4f}")

    # Confusion Matrix Plot
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Deposit (0)', 'Deposit (1)'])
    plt.figure(figsize=(8, 6)) # Create a new figure for each plot
    disp.plot(cmap=plot_cmap, values_format='d', ax=plt.gca()) # Use current axes
    plt.title(f'{model_name} Confusion Matrix')
    # Ensure 'models' directory exists before saving
    os.makedirs('models', exist_ok=True)
    plt.savefig(f'models/{model_name.lower().replace(" ", "_")}_confusion_matrix.png')
    plt.close() # Close plot to prevent display in non-notebook environments
    print(f"Confusion Matrix plot saved to models/{model_name.lower().replace(' ', '_')}_confusion_matrix.png")

    return pipeline, y_pred, y_proba

def save_model(model, filename="best_bank_marketing_logistic_regression_model.joblib"):
    """
    Saves the trained model (pipeline) to the 'models' directory using joblib.
    """
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True) # Ensure directory exists

    model_path = os.path.join(model_dir, filename)
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully to: {model_path}")

# --- Main execution block ---
if __name__ == "__main__":
    print("--- Starting Logistic Regression Project ---")

    # Step 1: Load the dataset
    raw_df = load_bank_data()
    if raw_df is None:
        exit("Failed to load data. Exiting.")

    # Identify initial numerical and categorical columns for EDA summary (before 'y' conversion)
    initial_numerical_cols = raw_df.select_dtypes(include=np.number).columns.tolist()
    initial_categorical_cols = raw_df.select_dtypes(include='object').columns.tolist()
    perform_eda_summary(raw_df.copy(), initial_numerical_cols, initial_categorical_cols)

    # Step 2: Perform Data Preprocessing and Splitting
    # This function now returns X, y, and the preprocessor (ColumnTransformer)
    X, y, preprocessor_pipeline, _, _ = preprocess_bank_data(raw_df)
    if X is None:
        exit("Failed to preprocess data. Exiting.")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_train_test_data(X, y, stratify_by_y=True)
    if X_train is None:
        exit("Failed to split train and test data. Exiting.")

    # Step 3: Build a baseline Logistic Regression model
    # The preprocessor_pipeline is passed directly to the model pipeline
    baseline_model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor_pipeline),
        ('classifier', LogisticRegression(random_state=42, solver='liblinear'))
    ])
    baseline_model, _, _ = train_and_evaluate_model(
        baseline_model_pipeline, X_train, y_train, X_test, y_test,
        model_name="Baseline Logistic Regression", plot_cmap=plt.cm.Blues
    )

    # Step 4: Optimize the model
    # Optimization Strategy: Addressing Class Imbalance with class_weight='balanced'
    optimized_model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor_pipeline),
        ('classifier', LogisticRegression(random_state=42, solver='liblinear', class_weight='balanced'))
    ])
    optimized_model, _, _ = train_and_evaluate_model(
        optimized_model_pipeline, X_train, y_train, X_test, y_test,
        model_name="Optimized Logistic Regression", plot_cmap=plt.cm.Greens
    )

    # Step 5: Save the optimized model
    save_model(optimized_model)

    print("\n--- Logistic Regression Project Execution Complete ---")
    print("Check 'data/processed/' and 'models/' folders for outputs (e.g., plots, saved model).")

    #use python -m src.app to run the app