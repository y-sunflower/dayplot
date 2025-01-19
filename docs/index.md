# dayplot

A simple-to-use Python library to build **calendar heatmaps** with ease. It's built on top of **matplotlib** and leverages it to access high customization possibilities.

## Quick start

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

![](img/quickstart.png)

<br>

## Installation

```bash
pip install git+https://github.com/JosephBARBIERDARNAL/dayplot.git
```

<br>

## Guide

- [Customise the charts](tuto/basic-styling)
- [Work with negative values](tuto/negative-values)
- [Cell style](tuto/boxstyle)
- [Combining charts](tuto/combine-charts)
- [Fetch (and plot) Github contributions](tuto/fetch-github-contribs)

<br>

## Related projects

- [calplot](https://github.com/tomkwok/calplot){target=\_blank}
- [july](https://github.com/e-hulten/july){target=\_blank}
- [calendarplot](https://github.com/dhowland/calendarplot){target=\_blank}

<br><br>
