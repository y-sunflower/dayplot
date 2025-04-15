# dayplot

A simple-to-use Python library to build **calendar heatmaps** with ease. It's built on top of **matplotlib** and leverages it to access high customization possibilities.

## Examples

=== "Quick start"

    ![](img/quickstart.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset()  # requires pandas to be installed

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

    df = dp.load_dataset()

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

    df = dp.load_dataset()

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

    df = dp.load_dataset()

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

=== "Round boxes"

    ![](img/quickstart-boxstyle.png)

    ```py
    import matplotlib.pyplot as plt
    import dayplot as dp

    df = dp.load_dataset()

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

You can find more examples in the [Gallery](gallery).

## Installation

```bash
pip install dayplot
```

## Related projects

- [calplot](https://github.com/tomkwok/calplot){target=\_blank}
- [july](https://github.com/e-hulten/july){target=\_blank}
- [calendarplot](https://github.com/dhowland/calendarplot){target=\_blank}

<br><br>
