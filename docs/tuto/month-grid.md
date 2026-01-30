### Visually Separate Months

Set `month_grid=True` to create a visual bounding box around the days within a given month.

```py hl_lines="14"
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
    month_grid=True,
    ax=ax,
)
```

### Style Your Month Grid

To further customize your monthly boxes, you should use the `month_grid_kws` argument which forwards an argument Mapping to [matplotlib.patches.PathPatch](https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.PathPatch.html). Note that this argument is ignored if `month_grid=False`.

```py hl_lines="14 15 16 17 18 19"
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
    month_grid=True,
    month_grid_kws={
        'linestyle': '--',
        'linewidth': 5,
        'edgecolor': 'orange'
    },
    ax=ax,
)
```
