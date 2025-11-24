import pandas as pd
def load_dataset():
    df = pd.read_csv("../data/diabetes.csv")
    print("Dataset successfully loaded!\n")
    print("This is the head\n",df.head())
    print("This is the info\n", df.info())
    print("This is the decription\n", df.describe())
    return df

if __name__ == "__main__":
    load_dataset()

