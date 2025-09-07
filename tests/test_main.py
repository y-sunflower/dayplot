import pytest
import warnings
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
import string

import pandas as pd
import polars as pl

from dayplot import calendar
import dayplot


@pytest.fixture
def sample_data():
    """
    Provides some sample dates and values for testing.
    Returns (dates, values) where each is a list.
    """
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(10)]
    values = [i for i in range(10)]  # 0...9
    return dates, values


def test_calendar_mismatched_lengths():
    """
    Test that passing mismatched dates and values raises a ValueError.
    """
    dates = [datetime(2024, 1, 1), datetime(2024, 1, 2)]
    values = [10]

    with pytest.raises(ValueError) as exc_info:
        fig, ax = plt.subplots()
        calendar(dates, values, ax=ax)

    assert "`dates` and `values` must have the same length." in str(exc_info.value)


def test_calendar_custom_colormap(sample_data):
    """
    Test using a custom LinearSegmentedColormap.
    """
    dates, values = sample_data
    custom_cmap = LinearSegmentedColormap.from_list("custom", ["white", "blue"])
    fig, ax = plt.subplots()
    calendar(dates, values, cmap=custom_cmap, ax=ax)


def test_calendar_string_cmap(sample_data):
    """
    Test using a valid string colormap name (e.g., "Reds").
    """
    dates, values = sample_data
    fig, ax = plt.subplots()
    calendar(dates, values, cmap="Reds", ax=ax)


def test_calendar_invalid_cmap(sample_data):
    """
    Test that passing an invalid colormap raises a ValueError.
    """
    dates, values = sample_data

    with pytest.raises(ValueError):
        fig, ax = plt.subplots()
        calendar(dates, values, cmap=123, ax=ax)


def test_warning_color_for_none(sample_data):
    """
    Test that passing an invalid colormap raises a ValueError.
    """
    dates, values = sample_data
    values[0] = -19

    with pytest.warns(UserWarning):
        warnings.warn(
            "color_for_none argument is ignored when values argument contains negative values.",
            UserWarning,
        )
        fig, ax = plt.subplots()
        calendar(dates, values, ax=ax)


def test_calendar_all_zeros():
    """
    Test when all values are zero; ensures fallback behavior for p90 calculation.
    """
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(5)]
    values = [0, 0, 0, 0, 0]

    fig, ax = plt.subplots()
    calendar(dates, values, ax=ax)

    patches = ax.patches
    for rect in patches:
        assert rect.get_facecolor()[:3] == (232 / 255, 232 / 255, 232 / 255), (
            "Expected color_for_none for zero values."
        )


def test_calendar_empty_data():
    """
    Test behavior when passing empty lists for dates and values.
    """
    dates = []
    values = []

    with pytest.raises(ValueError):
        fig, ax = plt.subplots()
        calendar(dates, values, ax=ax)


def test_calendar_custom_date_range(sample_data):
    """
    Test that specifying a custom start_date and end_date that encompass the data
    doesn't cause errors and includes the correct range.
    """
    dates, values = sample_data
    fig, ax = plt.subplots()
    calendar(dates, values, start_date="2024-01-01", end_date="2024-01-15", ax=ax)

    patches = ax.patches
    assert len(patches) >= 15, "Expected at least 15 day patches."


def test_calendar_inverted_y_axis(sample_data):
    """
    Test that the y-axis is inverted (Sunday at the top).
    We can check the transform or the order of patches.
    """
    dates, values = sample_data
    fig, ax = plt.subplots()
    calendar(dates, values, ax=ax)

    y_limits = ax.get_ylim()
    assert y_limits[0] > y_limits[1], "Y-axis should be inverted (top > bottom)."


def test_calendar_patch_count(sample_data):
    """
    Verify the correct number of day patches are drawn for the date range.
    """
    dates, values = sample_data
    fig, ax = plt.subplots()
    calendar(dates, values, ax=ax)
    patches = ax.patches
    assert len(patches) == 10, f"Expected 10 patches for 10 days, got {len(patches)}."


def test_calendar_patch_type(sample_data):
    """
    Verify that the calendar output is an iterable of patches.
    """
    dates, values = sample_data
    fig, ax = plt.subplots()
    rect_patches = calendar(dates, values, ax=ax)
    for rect_patch in rect_patches:
        assert isinstance(rect_patch, matplotlib.patches.FancyBboxPatch)


def test_calendar_p90_scaling():
    """
    Test that outlier values do not cause the colormap to break.
    We use one large value and several small ones.
    """
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(5)]
    values = [1, 2, 2, 2, 100]  # Include an outlier
    fig, ax = plt.subplots()
    calendar(dates, values, cmap="Greens", ax=ax)

    patches = ax.patches
    assert len(patches) == 5
    assert patches[-1].get_facecolor()[:3] != (232 / 255, 232 / 255, 232 / 255), (
        "Outlier day should not have the 'no data' color."
    )


def test_calendar_invalid_week_starts_on():
    """Test that an invalid week_starts_on raises a ValueError."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(7)]
    values = [1, 2, 3, 4, 5, 6, 7]
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        calendar(dates, values, week_starts_on="InvalidDay", ax=ax)


def test_calendar_week_starts_on_monday():
    """Test when week_starts_on is set to Monday."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(7)]
    values = [1, 2, 3, 4, 5, 6, 7]
    fig, ax = plt.subplots()
    calendar(dates, values, week_starts_on="Monday", ax=ax)
    patches = ax.patches
    assert len(patches) == 7


@pytest.mark.parametrize("backend", [pd, pl])
def test_diffrerent_df_backends(backend):
    """Test that it works with different backends"""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(7)]
    values = [1, 2, 3, 4, 5, 6, 7]
    df = backend.DataFrame({"dates": dates, "values": values})

    fig, ax = plt.subplots()
    calendar(df["dates"], df["values"], ax=ax)

    patches = ax.patches
    assert len(patches) == 7


@pytest.mark.parametrize("legend", [True, False])
@pytest.mark.parametrize("legend_bins", [2, 4, 10])
@pytest.mark.parametrize("legend_labels", [None, "auto", []])
@pytest.mark.parametrize("legend_labels_kws", [None, {"color": "red", "size": "10"}])
def test_legend_works(legend, legend_bins, legend_labels, legend_labels_kws):
    """Test that legend arguments work"""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(7)]
    values = [1, 2, 3, 4, 5, 6, 7]
    if legend_labels == []:
        legend_labels = list(string.ascii_lowercase)[:legend_bins]
    fig, ax = plt.subplots()
    calendar(
        dates,
        values,
        legend=legend,
        legend_bins=legend_bins,
        legend_labels=legend_labels,
        legend_labels_kws=legend_labels_kws,
    )

    patches = ax.patches
    if legend:
        assert len(patches) == len(values) + legend_bins
    else:
        assert len(patches) == len(values)

    plt.close("all")


def dayplot_version():
    assert dayplot.__version__ == "0.4.2"
