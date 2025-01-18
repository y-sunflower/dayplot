import pandas as pd
import importlib.resources


def load_sample():
    csv_path = importlib.resources.files("dayplot.data").joinpath("sample.csv")

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df["values"] = df["values"].astype(int)
    return df


if __name__ == "__main__":
    data = load_sample()

    print(data["date"])
    print(data["values"])
