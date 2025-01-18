import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

from collections import defaultdict
from datetime import datetime, timedelta


def github_chart(
    dates,
    values,
    start_date=None,
    end_date=None,
    color_for_none="#e8e8e8",
    edgecolor="black",
    edgewidth=0.5,
    cmap="Greens",
    month_kws={},
    day_kws={},
    day_x_margin=0.02,
    month_y_margin=0.4,
):
    """
    Create a GitHub-style heatmap (contribution chart) from input dates and values.

    This function generates a calendar heatmap similar to GitHub's contribution graph, where
    each cell represents a day colored according to the corresponding value. The chart is
    organized by weeks (columns) and days of the week (rows), starting from a specified
    start date to an end date.

    Parameters
    ----------
    dates : list
        A list of date-like objects (e.g., `datetime.date`, `datetime.datetime`, or
        strings in "YYYY-MM-DD" format). Must have the same length as `values`.
    values : list of int or float
        A list of numeric values corresponding to each date in `dates`. These values
        represent contributions or counts for each day and must have the same length
        as `dates`.
    start_date : {None, date, datetime, str}, optional
        The earliest date to display on the chart. Can be a `date`, `datetime`, or a
        string in "YYYY-MM-DD" format. If not provided, the minimum date found in
        `dates` will be used.
    end_date : {None, date, datetime, str}, optional
        The latest date to display on the chart. Can be a `date`, `datetime`, or a
        string in "YYYY-MM-DD" format. If not provided, the maximum date found in
        `dates` will be used.
    edgecolor : str, optional
        Color of the edges for each day's rectangle. Defaults to `"black"`.
    color_for_none : str, optional
        Color to use for days with no contributions (i.e., count zero). Defaults to
        `"#e8e8e8"`, a light gray color.
    cmap : {str, LinearSegmentedColormap}, optional
        A valid Matplotlib colormap name or a `LinearSegmentedColormap` instance.
        Defaults to `"Greens"`. The colormap is used to determine the fill color
        intensity of each day's cell based on its value.
    month_kws : dict, optional
        Additional keyword arguments passed to the matplotlib.axes.Axes.text function when
        labeling month names (outside of `x`, `y` and `s`).
    day_kws : dict, optional
        Additional keyword arguments passed to the matplotlib.axes.Axes.text function when
        labeling weekday names on the y-axis (outside of `x`, `y` and `s`).

    Returns
    -------
    fig : matplotlib.figure.Figure
        The Matplotlib figure object containing the heatmap.
    ax : matplotlib.axes.Axes
        The Matplotlib axes object on which the heatmap is plotted.

    Notes
    -----
    - The function aggregates multiple entries for the same date by summing their
      values.
    - The grid is laid out with weeks as columns and days of the week as rows, starting
      with Sunday at the top. The y-axis is inverted so that Sunday appears at the
      top of the chart.
    - Month labels are placed above the chart aligned with the start of each month.
    - Weekday labels are placed to the left of the chart.
    - The heatmap color intensity is scaled relative to the 90th percentile of all
      non-zero values to reduce the impact of outliers.

    Examples
    --------
    >>> import dayplot as dplot
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
    ...     'values': [5, 10, 3]
    ... })
    >>> fig, ax = dplot.github_chart(
    ...     df['date'],
    ...     df['values'],
    ...     start_date='2024-01-01',
    ...     end_date='2024-01-31'
    ...)
    >>> fig.show()
    """

    if len(dates) != len(values):
        raise ValueError("`dates` and `values` must have the same length.")

    date_counts = defaultdict(int)
    for d, v in zip(dates, values):
        if isinstance(d, datetime):
            d = d.date()
        elif isinstance(d, str):
            d = datetime.strptime(d, "%Y-%m-%d").date()

        date_counts[d] += v

    min_data_date = min(date_counts.keys())
    max_data_date = max(date_counts.keys())

    if start_date is None:
        start_date = min_data_date
    if end_date is None:
        end_date = max_data_date

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

    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_aspect("equal")

    valid_counts = [val for val in date_counts.values() if val > 0]
    if valid_counts:
        p90 = np.percentile(valid_counts, 90)
    else:
        p90 = 1  # fallback if no nonzero values

    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    elif isinstance(cmap, LinearSegmentedColormap):
        pass
    else:
        raise ValueError(
            "Invalid cmap input. It must be either a valid matplotlib colormap"
            "  (string) or a matplotlib.colors.LinearSegmentedColormap"
        )

    for week, weekday, count in data_for_plot:
        if count > 0:
            color = cmap((count + 1) / (p90 + 1))
        else:
            color = color_for_none
        rect = patches.Rectangle(
            xy=(week, weekday),
            width=1,
            height=1,
            linewidth=edgewidth,
            edgecolor=edgecolor,
            facecolor=color,
        )
        ax.add_patch(rect)

    month_text_style = dict(
        ha="center",
        va="center",
        size=9,
    )
    month_text_style.update(month_kws)
    month_starts = [d for d in full_range if d.day == 1]
    for m_start in month_starts:
        week_of_month = ((m_start - start_date).days + start_date.weekday()) // 7
        ax.text(
            week_of_month + 0.5,
            -month_y_margin,  # place label just outside the grid
            m_start.strftime("%b"),
            month_text_style,
        )

    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.set_xlim(-0.5, total_weeks + 0.5)
    ax.set_ylim(-0.5, 7.5)
    ax.set_xticks([])
    ax.set_yticks([])

    day_text_style = dict(
        transform=ax.get_yaxis_transform(),
        ha="left",
        va="center",
    )
    day_text_style.update(day_kws)
    ticks = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for y_tick, day in zip(ticks, labels):
        ax.text(
            -day_x_margin,
            y_tick,
            day,
            **day_text_style,
        )

    ax.tick_params(size=0)
    ax.invert_yaxis()  # so Sunday is at the top

    fig.tight_layout()
    return fig, ax


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("dayplot/data/sample.csv")
    df.loc[df["date"] == "2024-01-02", "values"] = 25

    fig, ax = github_chart(
        df["date"], df["values"], start_date="2024-01-01", end_date="2024-12-31"
    )
    fig.savefig("test.png", dpi=300, bbox_inches="tight")
    plt.show()
