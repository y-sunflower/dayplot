import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.path import Path
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm
from matplotlib.axes import Axes
from matplotlib.colors import Colormap
import numpy as np
from calendar import Calendar, day_name, day_abbr

from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import date, datetime, timedelta
from itertools import chain
from numbers import Real
from typing import List, Union, Optional, Dict, Any, Literal, cast
import warnings

from dayplot.utils import _parse_date, date_range, relative_date_add


IMPLEMENTED_BOXSTYLE = [
    "square",
    "circle",
    "round",
    "round4",
    "sawtooth",
    "roundtooth",
]

NOT_IMPLEMENTED_BOXSTYLE = [
    "ellipse",
    "larrow",
    "rarrow",
    "darrow",
]

_MISSING = object()


class _DefaultArg:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)


_DEFAULT_CMAP = _DefaultArg("Greens")
_DEFAULT_VMIN = _DefaultArg(None)
_DEFAULT_VMAX = _DefaultArg(None)
_DEFAULT_VCENTER = _DefaultArg(None)
_DEFAULT_LEGEND_BINS = _DefaultArg(4)
_DEFAULT_LESS_LABEL = _DefaultArg("Less")
_DEFAULT_MORE_LABEL = _DefaultArg("More")


def _is_numeric_value(value: Any) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool)


def _is_numeric_values(values) -> bool:
    return all(_is_numeric_value(value) for value in values)


def _unique_values_in_order(values) -> list[Any]:
    unique_values = []
    seen = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            unique_values.append(value)
    return unique_values


def _validate_categorical_arguments(
    cmap: Any,
    vmin: Any,
    vmax: Any,
    vcenter: Any,
    legend_bins: Any,
    less_label: Any,
    more_label: Any,
) -> None:
    invalid_args = []
    if cmap is not _DEFAULT_CMAP:
        invalid_args.append("cmap")
    if vmin is not _DEFAULT_VMIN:
        invalid_args.append("vmin")
    if vmax is not _DEFAULT_VMAX:
        invalid_args.append("vmax")
    if vcenter is not _DEFAULT_VCENTER:
        invalid_args.append("vcenter")
    if legend_bins is not _DEFAULT_LEGEND_BINS:
        invalid_args.append("legend_bins")
    if less_label is not _DEFAULT_LESS_LABEL:
        invalid_args.append("less_label")
    if more_label is not _DEFAULT_MORE_LABEL:
        invalid_args.append("more_label")

    if invalid_args:
        invalid_args_text = ", ".join(f"`{arg}`" for arg in invalid_args)
        raise ValueError(
            f"{invalid_args_text} cannot be used when `values` contains categorical data."
        )


def _validate_colors(colors: Any, categories: list[Any]) -> dict[Any, Any]:
    if colors is None:
        tab10 = plt.get_cmap("tab10")
        colors = [tab10(i) for i in range(10)]

    if isinstance(colors, Mapping):
        missing_categories = [
            category for category in categories if category not in colors
        ]
        if missing_categories:
            missing_text = ", ".join(repr(category) for category in missing_categories)
            raise ValueError(
                "`colors` is missing colors for the following categories: "
                f"{missing_text}."
            )

        color_map = {category: colors[category] for category in categories}
    elif isinstance(colors, Sequence) and not isinstance(colors, str):
        if len(colors) < len(categories):
            raise ValueError(
                "`colors` must contain at least as many colors as observed categories."
            )

        color_map = dict(zip(categories, colors))
    else:
        raise ValueError(
            "`colors` must be a mapping of category to color or a sequence of colors."
        )

    for category, color in color_map.items():
        try:
            mcolors.to_rgba(color)
        except ValueError as exc:
            raise ValueError(
                f"Invalid color {color!r} for category {category!r}."
            ) from exc

    return color_map


def _validate_inputs(boxstyle, dates, values):
    if isinstance(boxstyle, str):
        if boxstyle not in IMPLEMENTED_BOXSTYLE:
            if boxstyle in NOT_IMPLEMENTED_BOXSTYLE:
                return NotImplementedError
            else:
                raise ValueError(
                    f"Invalid `boxstyle` value. Must be in {IMPLEMENTED_BOXSTYLE}"
                )
    elif not isinstance(boxstyle, patches.BoxStyle):
        raise ValueError(
            f"`boxstyle` must either be a string or a `matplotlib.patches.BoxStyle`, not {boxstyle}"
        )

    if len(dates) != len(values):
        raise ValueError("`dates` and `values` must have the same length.")

    if len(dates) == 0 or len(values) == 0:
        raise ValueError("`dates` and `values` cannot be empty.")


def _validate_cmap(cmap: Union[str, LinearSegmentedColormap]) -> Colormap:
    if isinstance(cmap, str):
        return plt.get_cmap(cmap)
    elif not isinstance(cmap, LinearSegmentedColormap):
        raise ValueError(
            "Invalid `cmap` input. It must be either a valid matplotlib colormap string "
            f"or a matplotlib.colors.LinearSegmentedColormap instance, not {cmap}"
        )

    return cmap


def _get_start_and_end_dates(
    date_counts: dict[date, Any],
    start_date: Union[datetime, str, date, None],
    end_date: Union[datetime, str, date, None],
) -> tuple[date, date]:
    min_data_date = min(date_counts.keys())
    max_data_date = max(date_counts.keys())

    if start_date is None:
        start_date = min_data_date
    else:
        start_date = _parse_date(start_date)

    if end_date is None:
        end_date = max_data_date
    else:
        end_date = _parse_date(end_date)

    if isinstance(start_date, datetime):
        start_date = start_date.date()
    elif isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    if isinstance(end_date, datetime):
        end_date = end_date.date()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    return start_date, end_date


def calendar_week(cal: Calendar, date: date) -> list[date]:
    """
    Return the list of dates representing the calendar week containing `date`.

    The week is determined using the provided `calendar.Calendar` instance,
    meaning the first day of the week and week boundaries follow the calendar's
    configuration. The returned list always contains seven `datetime.date`
    objects and may include dates from adjacent months.

    Parameters
    ----------
    cal : calendar.Calendar
        A configured calendar instance that defines week structure.
    date : datetime.date
        The date whose containing calendar week should be returned.

    Returns
    -------
    list[datetime.date]
        A list of seven dates representing the week that contains `date`.

    Raises
    ------
    ValueError
        If no week in the calendar month contains `date`. This should not
        occur for valid `date` and `calendar.Calendar` inputs.
    """
    for wk in cal.monthdatescalendar(date.year, date.month):
        if wk[0] <= date <= wk[-1]:
            return wk
    msg = f"Date {date!r} was not found in any calendar week for {date.year:04d}-{date.month:02d}"
    raise ValueError(msg)


def calendar(
    dates: List[Union[date, datetime, str]],
    values: List[Any],
    start_date: Optional[Union[date, datetime, str]] = None,
    end_date: Optional[Union[date, datetime, str]] = None,
    color_for_none: Optional[str] = None,
    edgecolor: str = "black",
    edgewidth: float = 0.0,
    colors: Optional[Union[Dict[Any, Any], List[Any]]] = None,
    cmap: Any = _DEFAULT_CMAP,
    week_starts_on: str = "Sunday",
    month_kws: Optional[Dict] = None,
    day_kws: Optional[Dict] = None,
    day_x_margin: float = 0.02,
    month_y_margin: float = 0.4,
    vmin: Any = _DEFAULT_VMIN,
    vmax: Any = _DEFAULT_VMAX,
    vcenter: Any = _DEFAULT_VCENTER,
    boxstyle: Union[str, patches.BoxStyle] = "square",
    legend: bool = False,
    legend_bins: Any = _DEFAULT_LEGEND_BINS,
    legend_labels: Optional[Union[List, Literal["auto"]]] = None,
    legend_labels_precision: Optional[int] = None,
    legend_labels_kws: Optional[Dict] = None,
    legend_kws: Optional[Dict] = None,
    less_label: Any = _DEFAULT_LESS_LABEL,
    more_label: Any = _DEFAULT_MORE_LABEL,
    month_grid: bool = False,
    month_grid_kws: Dict = {},
    clip_on: bool = False,
    ax: Optional[Axes] = None,
    **kwargs: Any,
) -> List[patches.FancyBboxPatch]:
    """
    Create a calendar heatmap (GitHub-style) from input dates and values,
    supporting both positive and negative values via a suitable colormap scale.

    This function generates a calendar heatmap similar to GitHub's contribution graph, where
    each cell represents a day colored according to the corresponding value. The chart is
    organized by weeks (columns) and days of the week (rows), starting from a specified
    start date to an end date.

    When `vmin`, `vmax`, and `vcenter` are not specified, they default to the data's
    minimum, maximum, and zero (if data spans negative and positive values),
    respectively. Providing any of `vmin`, `vmax`, or `vcenter` manually will override
    the automatic calculation for that parameter.

    Args:
        dates: A list of date-like objects (e.g., datetime.date, datetime.datetime,
            or strings in "YYYY-MM-DD" format). Must have the same length as values.
        values: A list of numeric or categorical values corresponding to each date in
            dates. Numeric values are aggregated by summing duplicate dates. Categorical
            values use the last value for duplicate dates.
        start_date: The earliest date to display on the chart. Can be a date, datetime,
            or a string in "YYYY-MM-DD" format. If not provided, the minimum date found in
            `dates` will be used.
        end_date: The latest date to display on the chart. Can be a date, datetime, or a
            string in "YYYY-MM-DD" format. If not provided, the maximum date found in `dates`
            will be used.
        color_for_none: Color to use for days with no contributions (i.e., count zero).
            Defaults to "#e8e8e8", a light gray color. This parameter is ignored when `values`
            has negative values.
        edgecolor: Color of the edges for each day's rectangle.
        edgewidth: Line width for the edges of each day's rectangle.
        colors: Colors to use when `values` contains categorical data. Can be a mapping
            of category to color or a list of colors assigned in first-appearance order.
            If None, categorical data uses the Matplotlib "tab10" palette.
        cmap: A valid Matplotlib colormap name or a LinearSegmentedColormap instance. The
            colormap is used to determine the fill color intensity of each day's
            cell based on its value. This only applies to numeric values.
        week_starts_on: The starting day of the week, which can be specified as a string
            ("Sunday", "Monday", ..., "Saturday").
        month_kws: Additional keyword arguments passed to the matplotlib.axes.Axes.text function
            when labeling month names (outside of x, y and s).
        day_kws: Additional keyword arguments passed to the matplotlib.axes.Axes.text function
            when labeling weekday names on the y-axis (outside of x, y and s).
        day_x_margin: Distance between the day labels (Monday, Tuesday, etc.) and the graph. The
            greater the distance, the further to the left the text will be.
        month_y_margin: Distance between the month labels (January, February, etc.) and the graph.
            The greater the distance, the more text will appear at the top.
        vmin: The lower bound for the color scale. If None, it is determined automatically from the
            data. If data contains both positive and negative values and `vcenter` is not provided, `vmin` will
            default to the data's minimum. Providing `vmin` overrides the automatic calculation.
        vmax: The upper bound for the color scale. If None, it is determined automatically from the
            data. If data contains both positive and negative values and `vcenter` is not provided, `vmax`
            will default to the data's maximum. Providing `vmax` overrides the automatic calculation.
        vcenter: The midpoint for the color scale, typically used with diverging colormaps (e.g.,
            "RdBu") to position a central reference (e.g., zero). If None and the data spans negative and
            positive values, `vcenter` will default to 0. Providing vcenter overrides this automatic setting.
        boxstyle: The style of each box. This will be passed to `matplotlib.patches.FancyBboxPatch`.
            Available values are: "square", "circle", "ellipse", "larrow"
        legend: Whether to display a legend for the color scale.
        legend_bins: Number of boxes/steps to display in the numeric legend.
        legend_labels: Labels for the legend boxes. Can be a list of strings or "auto"
            to generate labels from the data values. For categorical legends, None and
            "auto" display category labels, and a list overrides them in category order.
        legend_labels_precision: Number of decimal places to round legend labels when
            `legend_labels="auto"`.
        legend_labels_kws: Additional keyword arguments passed to Axes.annotate function when
            rendering legend labels.
        legend_kws: Additional keyword arguments passed to Axes.legend when rendering
            categorical legends.
        less_label: Left label used for the legend.
        more_label: Right label used for the legend.
        month_grid: Whether to draw bounding boxes around each month.
        month_grid_kws: Additional keyword arguments passed to the matplotlib.path.Path used to draw
            visible bounding boxes around each month.
        clip_on: Whether the artist (e.g., squares) is clipped to the axes boundaries (True) or allowed to extend
            beyond them (False).
        ax: A matplotlib axes. If None, plt.gca() will be used. It is advisable to make this explicit
            to avoid unexpected behaviour, particularly when manipulating a figure with several axes.
        kwargs: Any additional arguments that will be passed to `matplotlib.patches.FancyBboxPatch`.
            For example, you can set `alpha`, `hatch`, `linestyle`, etc. You can find them all
            [here](https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.FancyBboxPatch.html).

    Returns:
        A list of `matplotlib.patches.FancyBboxPatch` (one for each cell).

    Notes:
        The function aggregates multiple numeric entries for the same date by summing
        their values. For categorical data, the last entry for a date is used.
    """
    _validate_inputs(boxstyle, dates, values)
    is_categorical = not _is_numeric_values(values)

    if is_categorical:
        _validate_categorical_arguments(
            cmap, vmin, vmax, vcenter, legend_bins, less_label, more_label
        )
        validated_cmap = _validate_cmap(_DEFAULT_CMAP.value)
    else:
        cmap = _DEFAULT_CMAP.value if cmap is _DEFAULT_CMAP else cmap
        vmin = _DEFAULT_VMIN.value if vmin is _DEFAULT_VMIN else vmin
        vmax = _DEFAULT_VMAX.value if vmax is _DEFAULT_VMAX else vmax
        vcenter = _DEFAULT_VCENTER.value if vcenter is _DEFAULT_VCENTER else vcenter
        legend_bins = (
            _DEFAULT_LEGEND_BINS.value
            if legend_bins is _DEFAULT_LEGEND_BINS
            else legend_bins
        )
        less_label = (
            _DEFAULT_LESS_LABEL.value
            if less_label is _DEFAULT_LESS_LABEL
            else less_label
        )
        more_label = (
            _DEFAULT_MORE_LABEL.value
            if more_label is _DEFAULT_MORE_LABEL
            else more_label
        )
        validated_cmap = _validate_cmap(cmap)

    cal = Calendar([*day_name].index(week_starts_on))

    month_kws = month_kws or {}
    day_kws = day_kws or {}
    legend_labels_kws = legend_labels_kws or {}
    legend_kws = legend_kws or {}
    ax = ax or plt.gca()

    category_order: list[Any] = []
    categories: list[Any] = []
    color_map: dict[Any, Any] = {}
    is_diverging = False
    norm: Any = None

    if is_categorical:
        date_counts = {}
        category_order = _unique_values_in_order(values)
        for d, v in zip(dates, values):
            date_counts[_parse_date(d)] = v
    else:
        date_counts = defaultdict(float)
        for d, v in zip(dates, values):
            date_counts[_parse_date(d)] += cast(float, v)

    start_date, end_date = _get_start_and_end_dates(date_counts, start_date, end_date)
    cal_start_date = calendar_week(cal, start_date)[0]
    cal_end_date = calendar_week(cal, end_date)[-1]

    delta_days = (end_date - start_date).days + 1
    full_range = [start_date + timedelta(days=i) for i in range(delta_days)]

    data_for_plot = []
    for d in full_range:
        week_index = (d - cal_start_date).days // 7
        day_of_week = (d.weekday() - cal.firstweekday) % 7
        count = date_counts.get(d, _MISSING if is_categorical else 0)
        data_for_plot.append((week_index, day_of_week, count))

    total_weeks = (cal_end_date - cal_start_date).days // 7 + 1

    if is_categorical:
        observed_categories = {
            count for _, _, count in data_for_plot if count is not _MISSING
        }
        categories = [
            category for category in category_order if category in observed_categories
        ]
        color_map = _validate_colors(colors, categories)
    else:
        all_counts = np.array(list(date_counts.values()))
        min_count, max_count = all_counts.min(), all_counts.max()

        if vmin is None:
            vmin = min_count
        if vmax is None:
            vmax = max_count if max_count != 0 else 1

        if vcenter is not None:
            is_diverging = True
            norm = TwoSlopeNorm(
                vmin=cast(float, vmin),
                vcenter=cast(float, vcenter),
                vmax=cast(float, vmax),
            )
        else:
            # If we have both negative and positive values, use a diverging
            # scale with a center of 0. Otherwise, use a simple Normalize.
            if min_count < 0 < max_count:
                is_diverging = True
                norm = TwoSlopeNorm(
                    vmin=cast(float, vmin), vcenter=0, vmax=cast(float, vmax)
                )
            else:
                is_diverging = False
                norm = Normalize(vmin=cast(float, vmin), vmax=cast(float, vmax))

    rect_patches = []
    for week, weekday, count in data_for_plot:
        if is_categorical:
            if count is _MISSING:
                if color_for_none is None:
                    color_for_none = "#e8e8e8"
                face_color = color_for_none
            else:
                face_color = color_map[count]
        elif is_diverging:
            if color_for_none is not None:
                warnings.warn(
                    "`color_for_none` argument is ignored when `values` "
                    "argument contains negative values.",
                    UserWarning,
                )
            face_color = validated_cmap(norm(cast(float, count)))
        elif not is_diverging:
            if count == 0:
                if color_for_none is None:
                    color_for_none = "#e8e8e8"
                face_color = color_for_none
            else:
                face_color = validated_cmap(norm(cast(float, count)))

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

    month_text_style: dict[str, Any] = dict(ha="left", va="top", size=10)
    month_text_style.update(month_kws)

    month_starts = [
        *date_range(start_date.replace(day=1), end_date.replace(day=1), months=1)
    ]
    for m_start in month_starts:
        week_of_month = (m_start - cal_start_date).days // 7
        ax.text(
            week_of_month + 0.1,
            7 + month_y_margin,
            m_start.strftime("%b"),
            **month_text_style,
        )

    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.set_xlim(-0.5, total_weeks + 0.5)
    ax.set_ylim(-0.5, 7.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_aspect("equal")

    day_text_style: dict[str, Any] = dict(
        transform=ax.get_yaxis_transform(), ha="left", va="center", size=10
    )
    day_text_style.update(day_kws)

    ticks = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    # Create labels in the adjusted order based on week_starts_on
    labels = [day_abbr[(cal.firstweekday + i) % 7] for i in range(7)]

    for y_tick, day_label in zip(ticks, labels):
        ax.text(-day_x_margin, y_tick, day_label, **day_text_style)

    if month_grid:
        # vertical grid around data within each months
        verts, codes = [], []
        last_month = relative_date_add(month_starts[-1], months=1)
        horizontal_gaps = []  # track horizontal lines that appear on the chart top
        for m_start in chain(month_starts, [last_month]):
            week_of_month = (m_start - cal_start_date).days // 7
            day_of_week = (m_start.weekday() - cal.firstweekday) % 7
            if day_of_week == 0:
                horizontal_gaps.append((week_of_month, week_of_month + 1))
            verts.extend(
                [
                    (week_of_month, 7),
                    (week_of_month, day_of_week),
                    (week_of_month + 1, day_of_week),
                    (week_of_month + 1, 0),
                ]
            )

            codes.extend([Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO])

        # horizontal grid above/below data, ensuring they do not overlap with any lines drawn in the previous step.
        last_week_of_month = (last_month - cal_start_date).days // 7
        verts.extend(
            [
                # bottom line
                (0, 7),
                (last_week_of_month, 7),
                # top line
                (1, 0),
                *((wk, 0) for gap in horizontal_gaps for wk in gap),
                (last_week_of_month + 1, 0),
            ]
        )
        codes.extend(
            [
                # bottom line
                *[Path.MOVETO, Path.LINETO],
                # top line
                *[
                    Path.MOVETO,
                    *([Path.LINETO, Path.MOVETO] * len(horizontal_gaps)),
                    Path.LINETO,
                ],
            ]
        )

        path = Path(verts, codes, closed=False)
        default_month_grid_kws = dict(facecolor="none", clip_on=clip_on)
        default_month_grid_kws.update(month_grid_kws)

        patch = patches.PathPatch(path, **default_month_grid_kws)
        ax.add_patch(patch)

    if legend:
        if is_categorical:
            legend_handles = []
            legend_label_values = []
            for i, category in enumerate(categories):
                if legend_labels in (None, "auto"):
                    legend_label = str(category)
                else:
                    legend_label = str(cast(List, legend_labels)[i])

                legend_handles.append(
                    patches.Patch(
                        facecolor=color_map[category],
                        edgecolor=edgecolor,
                        label=legend_label,
                    )
                )
                legend_label_values.append(legend_label)

            if legend_handles:
                legend_text_props = {
                    key: value
                    for key, value in legend_labels_kws.items()
                    if key
                    not in {
                        "color",
                        "ha",
                        "horizontalalignment",
                        "va",
                        "verticalalignment",
                    }
                }
                categorical_legend_kws: dict[str, Any] = dict(
                    loc="upper center",
                    bbox_to_anchor=(0.5, -0.08),
                    ncol=min(len(categories), 3),
                    frameon=False,
                    handlelength=1,
                    handletextpad=0.5,
                    columnspacing=1.2,
                    prop=legend_text_props or None,
                )
                categorical_legend_kws.update(legend_kws)
                legend_artist = ax.legend(
                    handles=legend_handles,
                    labels=legend_label_values,
                    **categorical_legend_kws,
                )
                if "color" in legend_labels_kws:
                    for text in legend_artist.get_texts():
                        text.set_color(legend_labels_kws["color"])
            return rect_patches

        legend_rects = []
        legend_values = np.linspace(
            cast(float, vmin), cast(float, vmax), cast(int, legend_bins)
        )

        for i, val in enumerate(legend_values):
            if is_diverging:
                color = validated_cmap(norm(cast(float, val)))
            else:
                color = (
                    color_for_none
                    if val == 0
                    else validated_cmap(norm(cast(float, val)))
                )

            legend_xloc = total_weeks - len(legend_values) + i
            rect = patches.FancyBboxPatch(
                xy=(legend_xloc + 0.35, -1.2),
                width=0.3,
                height=0.3,
                linewidth=edgewidth,
                edgecolor=edgecolor,
                facecolor=color,
                boxstyle=boxstyle,
                clip_on=False,
                **kwargs,
            )
            ax.add_patch(rect)
            legend_rects.append(rect)

            if legend_labels is not None:
                if legend_labels == "auto":
                    legend_label = round(val, ndigits=legend_labels_precision)
                else:
                    legend_label = str(cast(List, legend_labels)[i])

                legend_labels_style: dict[str, Any] = dict(
                    size=7, ha="center", va="bottom"
                )
                legend_labels_style.update(legend_labels_kws)
                ax.annotate(
                    legend_label,
                    xy=(0.5, 1),
                    xycoords=rect,
                    xytext=(0, 1),
                    textcoords="offset points",
                    **legend_labels_style,
                )

        ax.annotate(
            less_label,
            xy=(0, 0.5),
            xycoords=legend_rects[0],
            xytext=(-5, 0),
            textcoords="offset points",
            va="center",
            ha="right",
            size=8,
        )
        ax.annotate(
            more_label,
            xy=(1, 0.5),
            xycoords=legend_rects[-1],
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            size=8,
        )

    return rect_patches
