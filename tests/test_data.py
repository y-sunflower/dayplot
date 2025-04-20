import pandas as pd
from dayplot import load_dataset


def test_load_dataset():
    df = load_dataset()
    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) == 2
    assert "dates" in df.columns
    assert "values" in df.columns
    assert len(df) == 500
