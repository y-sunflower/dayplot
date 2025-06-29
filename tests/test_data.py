from dayplot import load_dataset
import pytest


@pytest.mark.parametrize("backend", ["pandas", "polars"])
def test_load_dataset(backend):
    df = load_dataset(backend=backend)
    assert len(df.columns) == 2
    assert "dates" in df.columns
    assert "values" in df.columns
    assert len(df) == 500
