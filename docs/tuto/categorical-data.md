### Plot categorical values

`dayplot` automatically switches to categorical colors when `values` contains non-numeric data.

In this mode, each category gets its own color instead of being mapped through a colormap.

```py
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()
df["activity"] = df["values"].map({
    1: "Focus",
    2: "Meeting",
    3: "Writing",
    4: "Review",
    5: "Admin",
})

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["activity"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    legend=True,
    ax=ax,
)
```

### Use your own colors

Use the `colors` argument to control the color for each category.

The safest option is to pass a dictionary, where each category is explicitly associated with a color.

```py hl_lines="18 19 20 21 22 23 24"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()
df["activity"] = df["values"].map({
    1: "Focus",
    2: "Meeting",
    3: "Writing",
    4: "Review",
    5: "Admin",
})

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["activity"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    colors={
        "Focus": "#2563eb",
        "Meeting": "#f97316",
        "Writing": "#16a34a",
        "Review": "#9333ea",
        "Admin": "#dc2626",
    },
    legend=True,
    ax=ax,
)
```

You can also pass a list of colors. Colors are assigned in the order categories first appear in `values`.

```py hl_lines="18"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()
df["activity"] = df["values"].map({
    1: "Focus",
    2: "Meeting",
    3: "Writing",
    4: "Review",
    5: "Admin",
})

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["activity"],
    colors=["#16a34a", "#9333ea", "#2563eb", "#dc2626", "#f97316"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    legend=True,
    ax=ax,
)
```

### Customize the legend labels

For categorical data, `legend=True` displays one box per category.

By default, the labels are the category names. You can override them with `legend_labels`.

```py hl_lines="27"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()
df["activity"] = df["values"].map({
    1: "Focus",
    2: "Meeting",
    3: "Writing",
    4: "Review",
    5: "Admin",
})

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["activity"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    colors={
        "Focus": "#2563eb",
        "Meeting": "#f97316",
        "Writing": "#16a34a",
        "Review": "#9333ea",
        "Admin": "#dc2626",
    },
    legend=True,
    legend_labels=["Writing day", "Review day", "Focus day", "Admin day", "Meeting day"],
    ax=ax,
)
```

<br><br>
