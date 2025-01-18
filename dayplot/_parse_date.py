from typing import Union
from datetime import date
from datetime import datetime


def parse_date(d: Union[datetime, str, date]) -> date:
    if isinstance(d, datetime):
        return d.date()
    elif isinstance(d, str):
        return datetime.strptime(d, "%Y-%m-%d").date()
    elif isinstance(d, date):
        return d
    raise TypeError("Unsupported date type")
