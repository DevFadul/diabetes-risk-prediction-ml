import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_data(df):
    print("Basic info:")
    print(df.info())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nSummary Statistics:")
    print(df.describe())
# Function for analyzing the dataset and try to find missing or abnormal values
if __name__ == "__main__":
    path = "/Users/mdfadul/diabetes-risk-prediction-ml/data/diabetes.csv"
    df = pd.read_csv(path)
    analyze_data(df)

# Loaded dataset
df = pd.read_csv("/Users/mdfadul/diabetes-risk-prediction-ml/data/diabetes.csv") 

# Plot distribution of Glucose by outcome
plt.figure(figsize=(8,5))
sns.histplot(data=df, x='Glucose', hue='Outcome', bins=30, kde=True)
plt.title('Glucose Distribution by Outcome')
plt.show()

# Correlation heatmap
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.show()

# Imbalance check
print(df['Outcome'].value_counts())
print(df['Outcome'].value_counts(normalize=True))
