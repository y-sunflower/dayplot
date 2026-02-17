# dayplot

<img src="https://github.com/JosephBARBIERDARNAL/static/blob/main/python-libs/dayplot/image.png?raw=true" alt="dayplot logo" align="right" width="150px"/>

A simple-to-use Python library to build **calendar heatmaps** with ease. It's built on top of **matplotlib** and leverages it to access high customization possibilities. They can even be interactive!

## Examples

=== "Quick start"

    ![](img/quickstart.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset("pandas") # can also be "polars", "pyarrow", etc

    fig, ax = plt.subplots(figsize=(15, 6))
    dp.calendar(
        dates=df["dates"],
        values=df["values"],
        start_date="2024-01-01",
        end_date="2024-12-31",
        ax=ax,
    )
    ```

=== "Colormap"

    ![](img/quickstart-cmap.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset("pandas")

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

=== "Fill the gap"

    ![](img/quickstart-gap.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset("pandas")

    fig, ax = plt.subplots(figsize=(16, 4))
    dp.calendar(
        dates=df["dates"],
        values=df["values"],
        start_date="2024-01-01",
        end_date="2024-12-31",
        mutation_scale=1.22,
        ax=ax,
    )
    ```

=== "Dark theme"

    ![](img/quickstart-dark.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset("pandas")

    fig, ax = plt.subplots(figsize=(15, 6))
    dp.calendar(
        dates=df["dates"],
        values=df["values"],
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

=== "Round boxes"

    ![](img/quickstart-boxstyle.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset("pandas")

    fig, ax = plt.subplots(figsize=(16, 4))
    dp.calendar(
        dates=df["dates"],
        values=df["values"],
        start_date="2024-01-01",
        end_date="2024-12-31",
        boxstyle="circle",
        ax=ax,
    )
    ```

=== "Github style"

    ![](img/quickstart-github.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset("pandas")

    fig, ax = plt.subplots(figsize=(16, 4))
    dp.calendar(
        dates=df["dates"],
        values=df["values"],
        start_date="2024-01-01",
        end_date="2024-12-31",
        ax=ax,
        **dp.styles["github"]
    )
    fig.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")
    ```

=== "Month Grid"

    ![](img/quickstart-monthgrid.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset("pandas")

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

You can also make `dayplot` **interactive** thanks to [plotjs](https://y-sunflower.github.io/plotjs/):

```py hl_lines="3 15"
import matplotlib.pyplot as plt
import dayplot as dp
from plotjs import PlotJS

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
PlotJS(fig).add_tooltip(labels=df["values"]).save("docs/img/interactive.html")
```

<div style="position:relative; width:100%; padding-top:40%;">
  <iframe
    src="img/interactive.html"
    style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;">
  </iframe>
</div>

<span style="font-size: 1rem; font-weight: bold;">[See more examples](./tuto/basic-styling.md)</span>

## Installation

=== "stable"

    ```bash
    pip install dayplot
    ```

=== "dev"

    ```bash
    pip install git+https://github.com/y-sunflower/dayplot.git@main
    ```

## Related projects

- [calplot](https://github.com/tomkwok/calplot){target=\_blank}
- [july](https://github.com/e-hulten/july){target=\_blank}
- [calendarplot](https://github.com/dhowland/calendarplot){target=\_blank}

<br><br>
