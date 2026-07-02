### Plot categorical values

`dayplot` automatically switches to categorical colors when `values` contains non-numeric data.

In this mode, each category gets its own color instead of being mapped through a colormap.

```py
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

dates = [
    "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
    "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12",
    "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19",
]
values = [
    "office", "office", "remote", "remote", "off",
    "office", "remote", "office", "remote", "off",
    "remote", "office", "office", "remote", "off",
]

fig, ax = plt.subplots(figsize=(10, 3))
dp.calendar(
    dates=dates,
    values=values,
    start_date="2024-01-01",
    end_date="2024-01-21",
    legend=True,
    ax=ax,
)
```

### Use your own colors

Use the `colors` argument to control the color for each category.

The safest option is to pass a dictionary, where each category is explicitly associated with a color.

```py hl_lines="24 25 26 27 28"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

dates = [
    "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
    "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12",
    "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19",
]
values = [
    "office", "office", "remote", "remote", "off",
    "office", "remote", "office", "remote", "off",
    "remote", "office", "office", "remote", "off",
]

fig, ax = plt.subplots(figsize=(10, 3))
dp.calendar(
    dates=dates,
    values=values,
    start_date="2024-01-01",
    end_date="2024-01-21",
    colors={
        "office": "#2563eb",
        "remote": "#16a34a",
        "off": "#f97316",
    },
    legend=True,
    ax=ax,
)
```

You can also pass a list of colors. Colors are assigned in the order categories first appear in `values`.

```py hl_lines="21"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

dates = [
    "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
    "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12",
    "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19",
]
values = [
    "office", "office", "remote", "remote", "off",
    "office", "remote", "office", "remote", "off",
    "remote", "office", "office", "remote", "off",
]

fig, ax = plt.subplots(figsize=(10, 3))
dp.calendar(
    dates=dates,
    values=values,
    colors=["#2563eb", "#16a34a", "#f97316"],
    start_date="2024-01-01",
    end_date="2024-01-21",
    legend=True,
    ax=ax,
)
```

### Customize the legend labels

For categorical data, `legend=True` displays one box per category.

By default, the labels are the category names. You can override them with `legend_labels`.

```py hl_lines="30"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

dates = [
    "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
    "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12",
    "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19",
]
values = [
    "office", "office", "remote", "remote", "off",
    "office", "remote", "office", "remote", "off",
    "remote", "office", "office", "remote", "off",
]

fig, ax = plt.subplots(figsize=(10, 3))
dp.calendar(
    dates=dates,
    values=values,
    start_date="2024-01-01",
    end_date="2024-01-21",
    colors={
        "office": "#2563eb",
        "remote": "#16a34a",
        "off": "#f97316",
    },
    legend=True,
    legend_labels=["Office", "Remote", "Day off"],
    ax=ax,
)
```

<br><br>
