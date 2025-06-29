### Change colormap

Use the `cmap` argument to use any other colormap from matplotlib. This argument can either be a string or a `matplotlib.colors.LinearSegmentedColormap` (the object behind colormaps in matplotlib).

**Pro tips**: you can find great colormaps using [pypalettes](https://python-graph-gallery.com/color-palette-finder/){target=\_blank}.

```py
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    cmap="Reds", # any matplotlib colormap
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
```

### Change other colors

You can change the color between squares with the `edgecolor` argument and the color for "none" (aka 0) with the `color_for_none` argument.

Also, use `edgewidth` to moderate the width of the edge between squares.

```py
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    color_for_none="#bcbcbc",
    edgecolor="white",
    edgewidth=0.4,
    cmap="OrRd",
    day_kws={"color": "white"},
    month_kws={"color": "white"},
    ax=ax,
)
fig.set_facecolor("#2a2929")
ax.set_facecolor("#2a2929")
```

<br>

### Text styling

In order to customize the text (days and months), you have to, respectively, use the `day_kws` and `month_kws` arguments. All arguments passed to them will then be forwarded to `ax.text()`.

Pro tip: when changing font size, the label positioning might get worse. In order to control that, use the `day_x_margin` argument (shift day labels to the left) and the `month_y_margin` argument (shift month labels to the top).

```py
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    day_kws={"weight": "bold"},
    month_kws={"size": 20, "color": "red"},
    day_x_margin=0.03, # default = 0.02
    month_y_margin=0.7, # default = 0.4
    ax=ax,
)
```

<br><br>
