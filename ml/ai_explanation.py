import json
import os
import pandas as pd

# Paths
DATA_PATH = "data/diabetes.csv"
EXPLANATION_FOLDER = "explanations"

# Friendly descriptions of features
FEATURE_DESCRIPTIONS = {
    "Pregnancies": "number of pregnancies",
    "Glucose": "blood sugar level",
    "BloodPressure": "blood pressure level",
    "SkinThickness": "skin thickness related to body fat",
    "Insulin": "insulin level",
    "BMI": "body mass index",
    "DiabetesPedigreeFunction": "family history of diabetes",
    "Age": "age"
}

def generate_sentence(feature, impact, direction):
    """Turn feature impact into a simple sentence."""
    desc = FEATURE_DESCRIPTIONS.get(feature, feature)

    if direction == "positive":
        return f"Your {desc} increased your diabetes risk."
    else:
        return f"Your {desc} helped lower your diabetes risk."

def generate_explanation(json_data):
    """Convert JSON explanation into readable text."""
    pred = json_data["prediction"]
    impacts = json_data["top_impacts"]

    lines = []

    if pred == 1:
        lines.append("The model predicts a higher chance of diabetes.")
    else:
        lines.append("The model predicts a lower chance of diabetes.")

    lines.append("Here are the top factors that influenced your result:")

    for item in impacts:
        feature = item["feature"]
        impact = item["impact"]
        direction = "positive" if impact > 0 else "negative"
        lines.append("- " + generate_sentence(feature, impact, direction))

    return "\n".join(lines)

def main():
    print("📌 Generating human-friendly AI explanations...")

    for i in range(768):
        try:
            json_path = os.path.join(EXPLANATION_FOLDER, f"explanation_{i}.json")
            output_path = os.path.join(EXPLANATION_FOLDER, f"explanation_{i}.txt")

            if not os.path.exists(json_path):
                continue

            with open(json_path, "r") as f:
                data = json.load(f)

            explanation_text = generate_explanation(data)

            with open(output_path, "w") as out:
                out.write(explanation_text)

        except Exception as e:
            print(f"Error on file {i}: {e}")

    print("✅ All text explanations generated!")

if __name__ == "__main__":
    main()
