import pandas as pd

def analyze_data(df):
    print("Basic info:")
    print(df.info())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nSummary Statistics:")
    print(df.describe())

if __name__ == "__main__":
    path = "/Users/mdfadul/diabetes-risk-prediction-ml/data/diabetes.csv"
    df = pd.read_csv(path)
    analyze_data(df)