### Handling negative values

`dayplot` makes it straightforward to plot negative values.

Under the hood, it automatically checks for them. If no negative values are found, all days with 0 or missing data are displayed in light gray (using the `color_for_none` argument). In this case, it's recommended to use a [sequential colormap](https://matplotlib.org/stable/users/explain/colors/colormaps.html#sequential){target=\_blank}.

Otherwise, `color_for_none` is ignored and all cells are colored according to their values. Any missing data is treated as 0 by default, so if you need a different approach, fill in the data before plotting.

```py
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

# add negative values at some random dates
df.loc[df.sample(n=40, replace=False).index, "values"] *= -1

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    cmap="RdBu", # use a diverging colormap (red -> white -> blue)
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
```

Red days are the ones with negative values.

<br>

### Control colormap scaling

You can set custom boundaries for the colormap using the `vmin`, `vcenter` and `vmax` arguments. In this example, any cell with a value at or below -3 displays in the deepest red hue, 0 is shown in a neutral color (white), and any cell at or above 10 appears in the most intense blue.

This can be used as a convenient way of controlling color mapping when there are outliers.

```py
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

# add negative values at some random dates
df.loc[df.sample(n=40, replace=False).index, "values"] *= -1

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    cmap="RdBu", # use a diverging colormap (red -> white -> blue)
    start_date="2024-01-01",
    end_date="2024-12-31",
    vmin=-3,
    vcenter=0,
    vmax=10,
    ax=ax,
)
```

<br><br>
