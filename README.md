# dayplot

<img src="https://github.com/JosephBARBIERDARNAL/static/blob/main/python-libs/dayplot/image.png?raw=true" alt="dayplot logo" align="right" width="150px"/>

A simple-to-use Python library to build **calendar heatmaps** with ease.

It's built on top of **matplotlib** and leverages it to access high customization possibilities.

[![PyPI Downloads](https://static.pepy.tech/badge/dayplot)](https://pepy.tech/projects/dayplot)
![Coverage](coverage-badge.svg)

<br>

## Quick start

```py
import matplotlib.pyplot as plt
import dayplot as dp

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
```

![](https://raw.githubusercontent.com/y-sunflower/dayplot/refs/heads/main/docs/img/quickstart.png)

More examples in the [documentation](https://y-sunflower.github.io/dayplot/).

<br>

## Installation

```bash
pip install dayplot
```

<br>

## Related projects

- [calplot](https://github.com/tomkwok/calplot)
- [july](https://github.com/e-hulten/july)
- [calendarplot](https://github.com/dhowland/calendarplot)

<br><br>
