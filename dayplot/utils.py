import pandas as pd
import importlib.resources


def load_dataset():
    csv_path = importlib.resources.files("dayplot.data").joinpath("sample.csv")
    df = pd.read_csv(csv_path)
    df["dates"] = pd.to_datetime(df["dates"], format="%Y-%m-%d")
    df["values"] = df["values"].astype(int)
    return df


if __name__ == "__main__":
    data = load_dataset()
    print(data["dates"])
    print(data["values"])
