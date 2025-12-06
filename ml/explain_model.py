import os
import joblib
import pandas as pd
import numpy as np
import shap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ===========================
# Helper: resolve project root
# ===========================
def get_project_root():
    return os.path.dirname(os.path.dirname(__file__))

# ===========================
# Load data + model
# ===========================
def load_data():
    file_path = os.path.join(get_project_root(), "data", "diabetes.csv")
    df = pd.read_csv(file_path)
    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]
    return X, y

def load_model_and_scaler():
    model_path = os.path.join(get_project_root(), "ml", "models", "best_model.pkl")
    scaler_path = os.path.join(get_project_root(), "ml", "models", "scaler.pkl")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


# ===========================
# SHAP explanation
# ===========================
def explain_model():
    print("Loading data and model...")
    X, y = load_data()
    model, scaler = load_model_and_scaler()

    # Train-test split with preserved feature names
    X_train, X_test, _, _ = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Preserve feature names through scaling
    X_train_scaled = pd.DataFrame(scaler.transform(X_train), columns=X.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X.columns)

    # Select a sample to build the SHAP explainer background
    background = X_train_scaled.sample(n=100, random_state=42)
    print(f"Building KernelExplainer with background size: {background.shape}")

    # Use consistent prediction function
    def predict_proba(data):
        return model.predict_proba(data)[:, 1]

    explainer = shap.KernelExplainer(predict_proba, background)

    # Explain on a subset of test data (faster)
    X_test_sample = X_test_scaled.sample(n=50, random_state=42)
    shap_values = explainer.shap_values(X_test_sample)

    # ===========================
    # Save results
    # ===========================
    results_dir = os.path.join(get_project_root(), "ml", "results")
    os.makedirs(results_dir, exist_ok=True)

    np.save(os.path.join(results_dir, "shap_values.npy"), shap_values)
    np.save(os.path.join(results_dir, "shap_base_value.npy"), explainer.expected_value)
    X_test_sample.to_csv(os.path.join(results_dir, "shap_test_sample.csv"), index=False)

    print("\nSHAP values and samples saved!")

    # ===========================
    # Visualizations
    # ===========================
    plt.title("SHAP Summary Plot")
    shap.summary_plot(shap_values, X_test_sample, show=False)
    plt.savefig(os.path.join(results_dir, "shap_summary_plot.png"), bbox_inches="tight")
    plt.close()

    shap.plots.bar(shap.Explanation(values=shap_values, data=X_test_sample,
                                    feature_names=X.columns))
    plt.title("Feature Importance (SHAP Bar Plot)")
    plt.savefig(os.path.join(results_dir, "shap_bar_plot.png"), bbox_inches="tight")
    plt.close()

    print("📊 SHAP summary and bar plots saved!")
    print("✨ Model explainability complete!")


if __name__ == "__main__":
    explain_model()
