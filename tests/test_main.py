import pytest
import warnings
import matplotlib
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgba
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


def test_calendar_categorical_default_colors():
    """Test categorical values use the default tab10 colors."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(3)]
    values = ["work", "rest", "work"]
    fig, ax = plt.subplots()

    patches = calendar(dates, values, ax=ax)
    tab10 = plt.get_cmap("tab10").colors

    assert patches[0].get_facecolor() == to_rgba(tab10[0])
    assert patches[1].get_facecolor() == to_rgba(tab10[1])
    assert patches[2].get_facecolor() == to_rgba(tab10[0])

    plt.close("all")


def test_calendar_categorical_dict_colors():
    """Test categorical values can use an explicit category-color mapping."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(3)]
    values = ["work", "rest", "work"]
    fig, ax = plt.subplots()

    patches = calendar(
        dates,
        values,
        colors={"work": "#0f766e", "rest": "#f59e0b"},
        ax=ax,
    )

    assert patches[0].get_facecolor() == to_rgba("#0f766e")
    assert patches[1].get_facecolor() == to_rgba("#f59e0b")
    assert patches[2].get_facecolor() == to_rgba("#0f766e")

    plt.close("all")


def test_calendar_categorical_list_colors_and_legend_order():
    """Test list colors are assigned and shown in first-appearance order."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(3)]
    values = ["low", "high", "medium"]
    fig, ax = plt.subplots()

    rects = calendar(
        dates,
        values,
        colors=["#ef4444", "#22c55e", "#3b82f6"],
        legend=True,
        ax=ax,
    )

    assert rects[0].get_facecolor() == to_rgba("#ef4444")
    assert rects[1].get_facecolor() == to_rgba("#22c55e")
    assert rects[2].get_facecolor() == to_rgba("#3b82f6")

    legend = ax.get_legend()
    assert legend is not None
    assert len(ax.patches) == len(rects)
    assert [handle.get_facecolor() for handle in legend.legend_handles] == [
        to_rgba("#ef4444"),
        to_rgba("#22c55e"),
        to_rgba("#3b82f6"),
    ]
    assert [text.get_text() for text in legend.get_texts()] == [
        "low",
        "high",
        "medium",
    ]

    plt.close("all")


def test_calendar_categorical_duplicate_dates_last_wins():
    """Test duplicate categorical dates use the last value."""
    dates = [datetime(2024, 1, 1), datetime(2024, 1, 1)]
    values = ["work", "rest"]
    fig, ax = plt.subplots()

    patches = calendar(
        dates,
        values,
        colors={"work": "#0f766e", "rest": "#f59e0b"},
        ax=ax,
    )

    assert len(patches) == 1
    assert patches[0].get_facecolor() == to_rgba("#f59e0b")

    plt.close("all")


def test_calendar_categorical_custom_legend_labels():
    """Test categorical legend labels can be overridden."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(2)]
    values = ["work", "rest"]
    fig, ax = plt.subplots()

    calendar(
        dates,
        values,
        colors={"work": "#0f766e", "rest": "#f59e0b"},
        legend=True,
        legend_labels=["Working", "Resting"],
        ax=ax,
    )

    legend = ax.get_legend()
    assert legend is not None
    assert [text.get_text() for text in legend.get_texts()] == [
        "Working",
        "Resting",
    ]

    plt.close("all")


def test_calendar_categorical_legend_with_long_labels():
    """Test categorical legends use Matplotlib's layout for long labels."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(4)]
    values = [
        "Customer support",
        "Deep strategy work",
        "Documentation review",
        "Release coordination",
    ]
    fig, ax = plt.subplots()

    calendar(
        dates,
        values,
        colors=["#0f766e", "#f59e0b", "#2563eb", "#dc2626"],
        legend=True,
        ax=ax,
    )

    legend = ax.get_legend()
    assert legend is not None
    assert [text.get_text() for text in legend.get_texts()] == values
    assert len(ax.patches) == len(values)

    plt.close("all")


def test_calendar_categorical_legend_kws():
    """Test categorical legend layout can be customized with legend_kws."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(3)]
    values = ["low", "high", "medium"]
    fig, ax = plt.subplots()

    rects = calendar(
        dates,
        values,
        colors=["#ef4444", "#22c55e", "#3b82f6"],
        legend=True,
        legend_kws={"ncol": 1, "frameon": True, "loc": "lower center"},
        ax=ax,
    )

    legend = ax.get_legend()
    assert legend is not None
    assert len(ax.patches) == len(rects)
    assert legend.get_frame_on()
    assert legend._ncols == 1
    assert legend._loc == 8

    plt.close("all")


def test_calendar_categorical_colors_too_short():
    """Test categorical list colors must cover all observed categories."""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(2)]
    values = ["work", "rest"]
    fig, ax = plt.subplots()

    with pytest.raises(ValueError, match="at least as many colors"):
        calendar(dates, values, colors=["#0f766e"], ax=ax)

    plt.close("all")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"cmap": "Reds"},
        {"vmin": 0},
        {"vmax": 10},
        {"vcenter": 5},
        {"legend_bins": 3},
        {"less_label": "Low"},
        {"more_label": "High"},
    ],
)
def test_calendar_categorical_rejects_numeric_only_arguments(kwargs):
    """Test numeric-only arguments raise for categorical values."""
    dates = [datetime(2024, 1, 1)]
    values = ["work"]
    fig, ax = plt.subplots()

    with pytest.raises(ValueError, match="categorical data"):
        calendar(dates, values, ax=ax, **kwargs)

    plt.close("all")


@pytest.mark.parametrize("legend", [True, False])
@pytest.mark.parametrize("legend_bins", [2, 4, 10])
@pytest.mark.parametrize("legend_labels", [None, "auto", []])
@pytest.mark.parametrize("legend_labels_kws", [None, {"color": "red", "size": "10"}])
@pytest.mark.parametrize("less_label", ["Less", "Moins"])
@pytest.mark.parametrize("more_label", ["More", "Plus"])
def test_legend_works(
    legend, legend_bins, legend_labels, legend_labels_kws, less_label, more_label
):
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
        less_label=less_label,
        more_label=more_label,
    )

    patches = ax.patches
    if legend:
        assert len(patches) == len(values) + legend_bins
    else:
        assert len(patches) == len(values)

    plt.close("all")


@pytest.mark.parametrize("month_grid", [True, False])
@pytest.mark.parametrize(
    "month_grid_kws", [{}, {"edgecolor": (0, 0, 1, 1), "linestyle": "--"}]
)
def test_month_grid(month_grid, month_grid_kws):
    """Test that month_grid and month_grid_kws arguments work"""
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(7)]
    values = [1, 2, 3, 4, 5, 6, 7]
    fig, ax = plt.subplots()
    rects = calendar(
        dates,
        values,
        month_grid=month_grid,
        month_grid_kws=month_grid_kws,
        ax=ax,
    )

    non_rect_patches = set(ax.patches) - set(rects)
    assert len(non_rect_patches) == int(month_grid)

    if month_grid:
        path_patch = non_rect_patches.pop()
        assert isinstance(path_patch, PathPatch)

        for k, v in month_grid_kws.items():
            assert getattr(path_patch, f"get_{k}")() == v

    plt.close("all")


def dayplot_version():
    assert dayplot.__version__ == "0.6.0"
