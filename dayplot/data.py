def load_dataset():
    import pandas as pd
    import importlib.resources

    csv_path = importlib.resources.files("dayplot.data").joinpath("sample.csv")
    df = pd.read_csv(csv_path)
    df["dates"] = pd.to_datetime(df["dates"], format="%Y-%m-%d")
    df["values"] = df["values"].astype(int)
    return df
