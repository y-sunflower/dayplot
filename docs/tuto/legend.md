## Add the default legend

You can add a very simple legend by using `legend=True`:

```py hl_lines="12"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    legend=True,
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
```

## Control the number of bins in legend

By default, it draws 4 bins, but it can be any positive number you want thanks to `legend_bins`:

```py hl_lines="12 13"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    legend=True,
    legend_bins=8,             # 8 bins
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
```

## Add labels of the values

To add labels below the legend, you can either use the "auto" option, or use your own list.

=== "`legend_labels="auto"`"

    ```py hl_lines="12 13"
    # mkdocs: render
    import matplotlib.pyplot as plt
    import dayplot as dp
    from dayplot import load_dataset

    df = load_dataset()

    fig, ax = plt.subplots(figsize=(16, 4))
    dp.calendar(
        dates=df["dates"],
        values=df["values"],
        legend=True,
        legend_labels="auto",      # calculate the value for each color
        start_date="2024-01-01",
        end_date="2024-12-31",
        ax=ax,
    )
    ```

=== "`legend_labels=["a", "b", "c", "d"]`"

    ```py hl_lines="12 13"
    # mkdocs: render
    import matplotlib.pyplot as plt
    import dayplot as dp
    from dayplot import load_dataset

    df = load_dataset()

    fig, ax = plt.subplots(figsize=(16, 4))
    dp.calendar(
        dates=df["dates"],
        values=df["values"],
        legend=True,
        legend_labels=["a", "b", "c", "d"],
        start_date="2024-01-01",
        end_date="2024-12-31",
        ax=ax,
    )
    ```

=== "`legend_labels_precision=1`"

    ```py hl_lines="12 13 14"
    # mkdocs: render
    import matplotlib.pyplot as plt
    import dayplot as dp
    from dayplot import load_dataset

    df = load_dataset()

    fig, ax = plt.subplots(figsize=(16, 4))
    dp.calendar(
        dates=df["dates"],
        values=df["values"],
        legend=True,
        legend_labels="auto",
        legend_labels_precision=1,  # accuracy when rounding
        start_date="2024-01-01",
        end_date="2024-12-31",
        ax=ax,
    )
    ```

## Advanced customization

You can use the `legend_labels_kws` argument to control exactly how the labels are supposed to look like:

```py hl_lines="12 13 14"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    legend=True,
    legend_labels="auto",
    legend_labels_kws=dict(color="red", size=10, weight="bold"),
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
```

## Negative values

It works well with negative values too:

```py hl_lines="17 18 19 20"
# mkdocs: render
import matplotlib.pyplot as plt
import dayplot as dp
from dayplot import load_dataset

df = load_dataset()

# add negative values at some random dates
df.loc[df.sample(n=40, replace=False).index, "values"] *= -1

fig, ax = plt.subplots(figsize=(15, 5))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    cmap="RdBu",
    legend=True,
    legend_bins=5,
    legend_labels="auto",
    ax=ax,
)
```

<br><br>
