import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import joblib
import os

def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # go up to project root
    file_path = os.path.join(base_dir, "data", "diabetes.csv")
    df = pd.read_csv(file_path)
    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]
    return X, y


def train_models():
    X, y = load_data()

    # Train-test split BEFORE SMOTE (completely separate test set)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Apply SMOTE to training data only
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=500),
        "Random Forest": RandomForestClassifier(n_estimators=200),
        "SVM": SVC(probability=True)
    }

    results = []
    best_model = None
    highest_f1 = 0

    for name, model in models.items():
        model.fit(X_train_resampled, y_train_resampled)
        y_pred = model.predict(X_test_scaled)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        results.append([name, accuracy, precision, recall, f1])

        print(f"\n{name} Results:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")

        if f1 > highest_f1:
            highest_f1 = f1
            best_model = model

    results_df = pd.DataFrame(
        results, columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"]
    )


    os.makedirs("ml/results", exist_ok=True)
    results_df.to_csv("ml/results/smote_model_results.csv", index=False)

    os.makedirs("ml/models", exist_ok=True)
    joblib.dump(best_model, "ml/models/best_model.pkl")
    joblib.dump(scaler, "ml/models/scaler.pkl")

    print("\nBest model saved!")
    print(results_df)

if __name__ == "__main__":
    train_models()
