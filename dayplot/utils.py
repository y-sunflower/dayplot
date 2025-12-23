import os
import narwhals as nw
from narwhals.typing import IntoDataFrame
from typing import Union, Literal
from datetime import date
from datetime import datetime


PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_dataset(backend: Literal["pandas", "polars", "pyarrow", "modin", "cudf"] = "pandas", **kwargs) -> IntoDataFrame:
    """
    Load a simple dataset with fake daily data. This function is a simple wrapper
    around the [`narwhals.read_csv()`](https://narwhals-dev.github.io/narwhals/api-reference/narwhals/#narwhals.read_csv)
    function.

    Args:
        backend: The output format of the dataframe. Note that, for example,
            if you set `backend="polars"`, you must have polars installed. Must
            be one of the following: "pandas", "polars", "pyarrow", "modin",
            "cudf". Default to "pandas".
        kwargs: Additional arguments passed to [`narwhals.read_csv()`](https://narwhals-dev.github.io/narwhals/api-reference/narwhals/#narwhals.read_csv).

    Returns:
        A dataframe with the specified dataset.
    """
    dataset_path = os.path.join(PACKAGE_DIR, "sample.csv")
    df = nw.read_csv(dataset_path, backend=backend, **kwargs)

    return df.to_native()


def _parse_date(d: Union[datetime, str, date]) -> date:
    if isinstance(d, datetime):
        return d.date()
    elif isinstance(d, str):
        return datetime.strptime(d, "%Y-%m-%d").date()
    elif isinstance(d, date):
        return d
    raise TypeError("Unsupported date type")
