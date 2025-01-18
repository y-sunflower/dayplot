import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

from collections import defaultdict
from datetime import datetime, timedelta


def github_chart(
    dates,
    values,
    start_date=None,
    end_date=None,
    edgecolor="black",
    color_for_none="#e8e8e8",
    cmap="Greens",
):
    """
    Create a GitHub-style heatmap (contribution chart) from input dates and values.

    Parameters
    ----------
    dates : list
        A list of date-like objects (date, datetime, or string in YYYY-MM-DD format).
        Must have the same length as 'values'.
    values : list of int or float
        Contribution (or count) values corresponding to each date.
        Must have the same length as 'dates'.
    start_date : date, datetime, or str, optional
        The earliest date to display on the chart. If not provided,
        the min date found in `dates` is used.
    end_date : date, datetime, or str, optional
        The latest date to display on the chart. If not provided,
        the max date found in `dates` is used.
    cmap : str, optional
        A valid matplotlib colormap name. Defaults to "Greens".

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object for the chart.
    ax : matplotlib.axes.Axes
        The axes object containing the heatmap.
    """

    if len(dates) != len(values):
        raise ValueError("`dates` and `values` must have the same length.")

    # 1) Build a dictionary that maps each date to a summed value
    date_counts = defaultdict(int)
    for d, v in zip(dates, values):
        # Convert datetime to date if needed
        if isinstance(d, datetime):
            d = d.date()
        # Convert string to date if needed
        elif isinstance(d, str):
            d = datetime.strptime(d, "%Y-%m-%d").date()

        date_counts[d] += v

    # 2) Determine the min and max date from the data if not supplied
    min_data_date = min(date_counts.keys())
    max_data_date = max(date_counts.keys())

    if start_date is None:
        start_date = min_data_date
    if end_date is None:
        end_date = max_data_date

    # Convert start_date and end_date to date objects if needed
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    elif isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    if isinstance(end_date, datetime):
        end_date = end_date.date()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # 3) Build the full date range
    delta_days = (end_date - start_date).days + 1
    full_range = [start_date + timedelta(days=i) for i in range(delta_days)]

    # 4) Prepare data for plotting
    #    We'll map each date to (week_index, day_of_week, count).
    #    day_of_week = Monday(0) ... Sunday(6)
    #    week_index is how many weeks from the start date.
    #    We'll center the date's "week index" around Monday(0).
    data_for_plot = []
    for d in full_range:
        days_from_start = (d - start_date).days
        start_date_sun = (start_date.weekday() + 1) % 7
        week_index = (days_from_start + start_date_sun) // 7
        day_of_week = (d.weekday() + 1) % 7
        count = date_counts.get(d, 0)
        data_for_plot.append((week_index, day_of_week, count))

    # Number of weeks in the entire range
    total_weeks = (end_date - start_date).days // 7 + 1

    # 5) Create the plot
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_aspect("equal")

    # If we have nonzero contributions, find the 90th percentile for color scaling
    valid_counts = [val for val in date_counts.values() if val > 0]
    if valid_counts:
        p90 = np.percentile(valid_counts, 90)
    else:
        p90 = 1  # fallback if no nonzero values

    for week, weekday, count in data_for_plot:
        if count > 0:
            color = plt.get_cmap(cmap)((count + 1) / (p90 + 1))
        else:
            color = color_for_none
        rect = patches.Rectangle(
            (week, weekday), 1, 1, linewidth=0.5, edgecolor=edgecolor, facecolor=color
        )
        ax.add_patch(rect)

    month_starts = [d for d in full_range if d.day == 1]
    for m_start in month_starts:
        week_of_month = ((m_start - start_date).days + start_date.weekday()) // 7
        ax.text(
            week_of_month + 0.5,
            -0.4,  # place label just outside the grid
            m_start.strftime("%b"),
            ha="center",
            va="center",
            fontsize=9,
        )

    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.set_xlim(-0.5, total_weeks + 0.5)
    ax.set_ylim(-0.5, 7.5)
    ax.set_xticks([])
    ax.set_yticks(
        ticks=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5],
        labels=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    )
    ax.tick_params(size=0)
    ax.invert_yaxis()  # so Sunday is at the top

    fig.tight_layout()
    return fig, ax


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("sample.csv")
    df.loc[df["date"] == "2024-01-02", "values"] = 25

    fig, ax = github_chart(
        df["date"], df["values"], start_date="2024-01-01", end_date="2024-12-31"
    )
    fig.savefig("test.png", dpi=300, bbox_inches="tight")
    plt.show()
