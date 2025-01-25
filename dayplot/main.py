import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm
import matplotlib
import numpy as np

from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Union, Optional, Dict
from datetime import date
import warnings

from dayplot._parse_date import parse_date


def calendar(
    dates: List[Union[date, datetime, str]],
    values: List[Union[int, float]],
    start_date: Optional[Union[date, datetime, str]] = None,
    end_date: Optional[Union[date, datetime, str]] = None,
    color_for_none: Optional[str] = None,
    edgecolor: str = "black",
    edgewidth: float = 0.0,
    cmap: Union[str, LinearSegmentedColormap] = "Greens",
    month_kws: Optional[Dict] = None,
    day_kws: Optional[Dict] = None,
    day_x_margin: float = 0.02,
    month_y_margin: float = 0.4,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    vcenter: Optional[float] = None,
    boxstyle: Union[str, matplotlib.patches.BoxStyle] = "square",
    ax: Optional[matplotlib.axes.Axes] = None,
    **kwargs,
) -> List[matplotlib.patches.Rectangle]:
    """
    Create a calendar heatmap (GitHub-style) from input dates and values,
    supporting both positive and negative values via a suitable colormap scale.

    This function generates a calendar heatmap similar to GitHub's contribution graph, where
    each cell represents a day colored according to the corresponding value. The chart is
    organized by weeks (columns) and days of the week (rows), starting from a specified
    start date to an end date.

    When vmin, vmax, and vcenter are not specified, they default to the data's
    minimum, maximum, and zero (if data spans negative and positive values),
    respectively. Providing any of vmin, vmax, or vcenter manually will override
    the automatic calculation for that parameter.

    Parameters
    ----------
    dates
        A list of date-like objects (e.g., datetime.date, datetime.datetime, or
        strings in "YYYY-MM-DD" format). Must have the same length as values.
    values
        A list of numeric values corresponding to each date in dates. These values
        represent contributions or counts for each day and must have the same length
        as dates.
    start_date
        The earliest date to display on the chart. Can be a date, datetime, or a
        string in "YYYY-MM-DD" format. If not provided, the minimum date found in
        dates will be used.
    end_date
        The latest date to display on the chart. Can be a date, datetime, or a
        string in "YYYY-MM-DD" format. If not provided, the maximum date found in
        dates will be used.
    color_for_none
        Color to use for days with no contributions (i.e., count zero). Defaults to
        "#e8e8e8", a light gray color. This parameter is ignored when `values` has
        negative values.
    edgecolor
        Color of the edges for each day's rectangle. Defaults to "black".
    edgewidth
        Line width for the edges of each day's rectangle. Defaults to 0.5.
    cmap
        A valid Matplotlib colormap name or a LinearSegmentedColormap instance.
        Defaults to "Greens". The colormap is used to determine the fill color
        intensity of each day's cell based on its value.
    month_kws
        Additional keyword arguments passed to the matplotlib.axes.Axes.text function when
        labeling month names (outside of x, y and s).
    day_kws
        Additional keyword arguments passed to the matplotlib.axes.Axes.text function when
        labeling weekday names on the y-axis (outside of x, y and s).
    day_x_margin
        Distance between the day labels (Monday, Tuesday, etc.) and the graph. The greater
        the distance, the further to the left the text will be.
    month_y_margin
        Distance between the month labels (January, February, etc.) and the graph. The greater
        the distance, the more text will appear at the top.
    vmin
        The lower bound for the color scale. If None, it is determined automatically from the
        data. If data contains both positive and negative values and `vcenter` is not provided,
        `vmin` will default to the data's minimum. Providing `vmin` overrides the automatic
        calculation.
    vmax
        The upper bound for the color scale. If None, it is determined automatically from the
        data. If data contains both positive and negative values and `vcenter` is not provided,
        `vmax` will default to the data's maximum. Providing `vmax` overrides the automatic
        calculation.
    vcenter
        The midpoint for the color scale, typically used with diverging colormaps (e.g., "RdBu")
        to position a central reference (e.g., zero). If None and the data spans negative and
        positive values, `vcenter` will default to 0. Providing vcenter overrides this automatic
        setting.
    boxstyle
        The style of each box. This will be passed to matplotlib.patches.FancyBboxPatch. Available
        values are: "square", "circle", "ellipse", "larrow"
    ax
        A matplotlib axes. If None, plt.gca() will be used. It is advisable to make
        this explicit to avoid unexpected behaviour, particularly when manipulating a
        figure with several axes.
    kwargs
        Any additional arguments that will be passed to matplotlib.patches.FancyBboxPatch. For example,
        you can set `alpha`, `hatch`, `linestyle`, etc.
        You can find them all here: https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.FancyBboxPatch.html

    Returns
    -------
    A list of matplotlib.patches.FancyBboxPatch (one for each cell).

    Notes
    -----
    - The function aggregates multiple entries for the same date by summing their
      values.

    Examples
    --------
    >>> import dayplot as dp
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
    ...     'values': [5, 10, 3]
    ... })
    >>> fig, ax = dp.calendar(
    ...     df['date'],
    ...     df['values'],
    ...     start_date='2024-01-01',
    ...     end_date='2024-01-31'
    ...)
    >>> fig.show()
    """

    month_kws = month_kws or {}
    day_kws = day_kws or {}

    implemented_boxstyle = [
        "square",
        "circle",
        "round",
        "round4",
        "sawtooth",
        "roundtooth",
    ]
    not_implemented_boxstyle = [
        "ellipse",
        "larrow",
        "rarrow",
        "darrow",
    ]
    if isinstance(boxstyle, str):
        if boxstyle not in implemented_boxstyle:
            if boxstyle in not_implemented_boxstyle:
                return NotImplementedError
            else:
                raise ValueError(
                    f"Invalid boxstyle value. Must be in {implemented_boxstyle}"
                )
    elif not isinstance(boxstyle, matplotlib.patches.BoxStyle):
        raise ValueError(
            f"boxstyle must either be a string or a matplotlib.patches.BoxStyle, not {boxstyle}"
        )

    if len(dates) != len(values):
        raise ValueError("`dates` and `values` must have the same length.")

    if len(dates) == 0 or len(values) == 0:
        raise ValueError("`dates` and `values` cannot be empty.")

    date_counts = defaultdict(float)
    for d, v in zip(dates, values):
        d = parse_date(d)
        date_counts[d] += v

    min_data_date = min(date_counts.keys())
    max_data_date = max(date_counts.keys())

    if start_date is None:
        start_date = min_data_date
    else:
        start_date = parse_date(start_date)

    if end_date is None:
        end_date = max_data_date
    else:
        end_date = parse_date(end_date)

    if isinstance(start_date, datetime):
        start_date = start_date.date()
    elif isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    if isinstance(end_date, datetime):
        end_date = end_date.date()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    delta_days = (end_date - start_date).days + 1
    full_range = [start_date + timedelta(days=i) for i in range(delta_days)]

    data_for_plot = []
    for d in full_range:
        days_from_start = (d - start_date).days
        start_date_sun = (start_date.weekday() + 1) % 7
        week_index = (days_from_start + start_date_sun) // 7
        day_of_week = (d.weekday() + 1) % 7
        count = date_counts.get(d, 0)
        data_for_plot.append((week_index, day_of_week, count))

    total_weeks = (end_date - start_date).days // 7 + 1

    if ax is None:
        ax = plt.gca()
    ax.set_aspect("equal")

    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    elif not isinstance(cmap, LinearSegmentedColormap):
        raise ValueError(
            "Invalid `cmap` input. It must be either a valid matplotlib colormap string "
            f"or a matplotlib.colors.LinearSegmentedColormap instance, not {cmap}"
        )

    all_counts = np.array(list(date_counts.values()))
    min_count, max_count = all_counts.min(), all_counts.max()

    if vmin is None:
        vmin = min_count
    if vmax is None:
        vmax = max_count if max_count != 0 else 1

    if vcenter is not None:
        is_diverging = True
        norm = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    else:
        # If we have both negative and positive values, use a diverging
        # scale with 0 in the center. Otherwise, we use a simple Normalize.
        if min_count < 0 < max_count:
            is_diverging = True
            norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
        else:
            is_diverging = False
            norm = Normalize(vmin=vmin, vmax=vmax)

    rect_patches = []
    for week, weekday, count in data_for_plot:
        if is_diverging:
            if color_for_none is not None:
                warnings.warn(
                    "color_for_none argument is ignored when values argument contains negative values.",
                    UserWarning,
                )
            face_color = cmap(norm(count))
        elif not is_diverging:
            if count == 0:
                if color_for_none is None:
                    color_for_none = "#e8e8e8"
                face_color = color_for_none
            else:
                face_color = cmap(norm(count))

        rect = patches.Rectangle(
            xy=(week, weekday),
            width=1,
            height=1,
            linewidth=edgewidth,
            edgecolor=edgecolor,
            facecolor=face_color,
        )
        rect = patches.FancyBboxPatch(
            xy=(week + 0.35, weekday + 0.35),
            width=0.3,
            height=0.3,
            linewidth=edgewidth,
            edgecolor=edgecolor,
            facecolor=face_color,
            boxstyle=boxstyle,
            **kwargs,
        )
        ax.add_patch(rect)
        rect_patches.append(rect)

    month_text_style = dict(ha="center", va="center", size=11)
    month_text_style.update(month_kws)
    month_starts = [d for d in full_range if d.day == 1]
    for m_start in month_starts:
        week_of_month = ((m_start - start_date).days + start_date.weekday()) // 7
        ax.text(
            week_of_month + 0.5,
            -month_y_margin,
            m_start.strftime("%b"),
            **month_text_style,
        )

    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.set_xlim(-0.5, total_weeks + 0.5)
    ax.set_ylim(-0.5, 7.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()

    day_text_style = dict(
        transform=ax.get_yaxis_transform(), ha="left", va="center", size=11
    )
    day_text_style.update(day_kws)

    ticks = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for y_tick, day_label in zip(ticks, labels):
        ax.text(-day_x_margin, y_tick, day_label, **day_text_style)

    plt.tight_layout()
    return rect_patches


if __name__ == "__main__":
    import numpy as np
    import dayplot as dp

    df = dp.load_dataset()

    fig, ax = plt.subplots(figsize=(15, 6))
    calendar(
        df["dates"],
        df["values"],
        start_date="2024-01-01",
        end_date="2024-12-31",
    )
    fig.savefig("test.png", dpi=300, bbox_inches="tight")
    plt.close()
