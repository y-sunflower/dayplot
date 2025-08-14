# Calendar heatmaps

<br>

::: dayplot.calendar

<br>

## Examples

#### Basic usage

```py
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 5))
dp.calendar(
   df["dates"],
   df["values"],
   start_date="2024-01-01",
   end_date="2024-12-31"
)
```

#### Change colormap

```py hl_lines="11"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 5))
dp.calendar(
   df["dates"],
   df["values"],
   cmap="Reds",
   start_date="2024-01-01",
   end_date="2024-12-31"
)
```

#### Change other colors

```py hl_lines="13 14 15 16 17 20 21"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 5))
dp.calendar(
   df["dates"],
   df["values"],
   start_date="2024-01-01",
   end_date="2024-12-31",
   color_for_none="pink",
   edgecolor="white",
   edgewidth=0.4,
   day_kws={"color": "skyblue"},
   month_kws={"color": "red"},
   ax=ax,
)
fig.set_facecolor("black")
ax.set_facecolor("black")
```

#### Boxstyle

```py hl_lines="13"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 5))
dp.calendar(
   dates=df["dates"],
   values=df["values"],
   start_date="2024-01-01",
   end_date="2024-12-31",
   boxstyle="circle",
   ax=ax,
)
```

#### Fill the gap

```py hl_lines="13"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 5))
dp.calendar(
   dates=df["dates"],
   values=df["values"],
   start_date="2024-01-01",
   end_date="2024-12-31",
   mutation_scale=1.22, # 22% bigger boxes
   ax=ax,
)
```

#### Label style

```py hl_lines="13 14 15 16"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 5))
dp.calendar(
   dates=df["dates"],
   values=df["values"],
   start_date="2024-01-01",
   end_date="2024-12-31",
   day_kws={"weight": "bold", "size": 12},
   month_kws={"size": 20, "color": "red"},
   day_x_margin=0.05,  # default = 0.02
   month_y_margin=0.8,  # default = 0.4
   ax=ax,
)
```

#### Combine calendars

```py hl_lines="8 17 25 28 29 30"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()

fig, (ax1, ax2) = plt.subplots(
   nrows=2,
   figsize=(16, 4)
)

dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2025-01-01",
    end_date="2025-12-31",
    ax=ax1, # top axes
)

dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax2, # bottom axes
)

text_args = dict(x=-4, y=3.5, size=30, rotation=90, color="#aaa", va="center")
ax1.text(s="2024", **text_args)
ax2.text(s="2025", **text_args)
```

#### Advanced

See advanced usage [**here**](../tuto/advanced.md).
