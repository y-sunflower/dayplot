import pytest
from datetime import datetime, date

from dayplot.utils import _parse_date


def test_parse_date_from_datetime():
    dt = datetime(2023, 1, 15, 12, 30, 45)
    result = _parse_date(dt)
    assert isinstance(result, date)
    assert result == date(2023, 1, 15)


def test__parse_date_from_date():
    d = date(2023, 1, 15)
    result = _parse_date(d)
    assert isinstance(result, date)
    assert result == d


def test__parse_date_from_str_valid():
    d_str = "2023-01-15"
    result = _parse_date(d_str)
    assert isinstance(result, date)
    assert result == date(2023, 1, 15)


def test_parse_date_from_str_invalid_format():
    d_str = "01-15-2023"  # Wrong format for the function (%Y-%m-%d)
    with pytest.raises(ValueError):
        _parse_date(d_str)


def test_parse_date_from_unsupported_type():
    with pytest.raises(TypeError):
        _parse_date(123)  # An integer is not supported by the function
