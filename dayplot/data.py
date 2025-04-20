def load_dataset():
    """
    Load a simple dataset with fake daily data.

    Requires `pandas` to be installed.

    Returns
    ---

    Pandas DataFrame with 2 columns: "dates" and "values".

    Example
    ---

    ```python
    import dayplot as dp

    df = load_dataset()
    ```
    """
    import pandas as pd
    import importlib.resources

    csv_path = importlib.resources.files("dayplot").joinpath("sample.csv")
    df = pd.read_csv(csv_path)
    df["dates"] = pd.to_datetime(df["dates"], format="%Y-%m-%d")
    df["values"] = df["values"].astype(int)
    return df
