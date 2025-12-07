import os
import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = "ml/results"
MODEL_DIR = "ml/models"
DATA_PATH = os.path.join("data", "diabetes.csv")

BEST_MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")


def load_model_and_data():
    print("Loading model and data...")

    model = joblib.load(BEST_MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    df = pd.read_csv(DATA_PATH)
    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]

    return model, scaler, X, y


def prepare_samples(scaler, X):
    # Scale features but keep DataFrame with named columns
    X_scaled = scaler.transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

    # Reduce sample size for SHAP performance
    background = X_scaled_df.sample(20, random_state=42)
    sample = X_scaled_df.sample(20, random_state=42)

    print(f"Using background size: {background.shape}, sample size: {sample.shape}")
    return background, sample


def build_explainer(model, background):
    # Use fast TreeExplainer if the model supports it
    if hasattr(model, "tree_"):
        print("Using TreeExplainer...")
        explainer = shap.TreeExplainer(model)
    else:
        print("Using KernelExplainer (slower)...")
        explainer = shap.KernelExplainer(model.predict_proba, background)

    return explainer


def save_results(shap_values, sample, features):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Save raw SHAP values
    shap_values_array = shap_values.values if hasattr(shap_values, "values") else shap_values
    npy_path = os.path.join(RESULTS_DIR, "shap_values.npy")
    import numpy as np
    np.save(npy_path, shap_values_array)
    print(f"Saved SHAP values ➜ {npy_path}")

    # Summary bar plot
    bar_path = os.path.join(RESULTS_DIR, "shap_summary_bar.png")
    shap.summary_plot(shap_values, sample, plot_type="bar", feature_names=features, show=False)
    plt.tight_layout()
    plt.savefig(bar_path)
    plt.close()
    print(f"Saved bar plot ➜ {bar_path}")

    # Summary dot plot
    dot_path = os.path.join(RESULTS_DIR, "shap_summary_dot.png")
    shap.summary_plot(shap_values, sample, feature_names=features, show=False)
    plt.tight_layout()
    plt.savefig(dot_path)
    plt.close()
    print(f"Saved dot plot ➜ {dot_path}")

  # Force plot for one prediction
    force_path = os.path.join(RESULTS_DIR, "shap_force_plot.png")
    #shap.force_plot(
    #base_value=explainer.expected_value[1],
    #shap_values=shap_values[1],
    #features=sample,
    #feature_names=features,
    #matplotlib=True,
    #show=False
#)

    plt.savefig(force_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved force plot ➜ {force_path}")



def main():
    model, scaler, X, y = load_model_and_data()
    background, sample = prepare_samples(scaler, X)

    global explainer  # used in force plot save
    explainer = build_explainer(model, background)

    print("Computing SHAP values... this may take a minute.")
    shap_values = explainer.shap_values(sample)

    print("Saving results...")
    save_results(shap_values, sample, X.columns)

    print("\n🎉 SHAP analysis completed & saved in ml/results/")


if __name__ == "__main__":
    main()
