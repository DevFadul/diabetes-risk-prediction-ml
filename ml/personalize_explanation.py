import os
import joblib
import shap
import pandas as pd
import numpy as np

# ====================
# CONFIG
# ====================
DATA_PATH = "data/diabetes.csv"
MODEL_PATH = "ml/models/best_model.pkl"
SCALER_PATH = "ml/models/scaler.pkl"
RESULTS_DIR = "ml/results/personalized"
TOP_K = 5  # You chose Option B: Top 5 features

os.makedirs(RESULTS_DIR, exist_ok=True)

print("📌 Loading model and data...")

# Load data
data = pd.read_csv(DATA_PATH)
X = data.drop(columns=["Outcome"])  # Feature columns only
y = data["Outcome"]                 # Label

# Load model + scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Scale features
X_scaled = scaler.transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

print(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")

# ====================
# SHAP Explainer
# ====================
print("⚙️ Computing SHAP values...")

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_scaled)

# For binary classifier: shap_values returns [class0, class1]
if isinstance(shap_values, list):
    shap_values = shap_values[1]

shap_values = np.array(shap_values)

print("SHAP values computed.")

# ====================
# Generate explanations
# ====================
def explain_instance(idx):
    sample = X_scaled.iloc[idx:idx+1]
    shap_sample = shap_values[idx]

    # Feature impact sorted by absolute importance
    feature_info = []
    for f, v, s in zip(X.columns, X.iloc[idx].values, shap_sample):
    # s is a 2-element array → [impact for class 0, impact for class 1]
        feature_info.append({
        "feature": f,
        "value": float(v),
        "impact": float(s[1])  # keep only diabetes-positive impact
    })

    df = pd.DataFrame(feature_info)
    df = df.reindex(df["impact"].abs().sort_values(ascending=False).index)
    top_features = df.head(TOP_K)



    # Model prediction
    pred = model.predict(sample)[0]
    prob = model.predict_proba(sample)[0][1]

    result = {
        "index": idx,
        "prediction": int(pred),
        "probability": float(np.round(prob, 4)),
        "top_features": top_features.to_dict(orient="records")
    }

    return result


print("📝 Saving personalized JSON explanations...")
summaries = []

for i in range(len(X)):
    explanation = explain_instance(i)
    summaries.append(explanation)

    file_path = os.path.join(RESULTS_DIR, f"explanation_{i}.json")
    pd.DataFrame(explanation["top_features"]).to_json(file_path, orient="records", indent=4)

print(f"✔ Generated {len(summaries)} explanation files → {RESULTS_DIR}/")

# ====================
# Save summary
# ====================
summary_df = pd.DataFrame([{
    "sample": e["index"],
    "prediction": e["prediction"],
    "probability": e["probability"]
} for e in summaries])

summary_df.to_csv(os.path.join(RESULTS_DIR, "summary.csv"), index=False)

print("📎 Saved summary.csv")
print("🎉 Done — Personalized explanations created successfully!")
