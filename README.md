> `dayplot` is supported by [Matplotlib Journey](https://www.matplotlib-journey.com/), an interactive online course designed to make you a master of Matplotlib. If you want to **support `dayplot`** and **become a Matplotlib expert**, consider purchasing the course!

<br><br>

# dayplot

A simple-to-use Python library to build **calendar heatmaps** with ease.

It's built on top of **matplotlib** and leverages it to access high customization possibilities.

<br>

## Quick start

```py
import matplotlib.pyplot as plt

import dayplot as dp
from dayplot.data import load_dataset

df = load_dataset()

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
```

![](https://raw.githubusercontent.com/JosephBARBIERDARNAL/dayplot/refs/heads/main/docs/img/quickstart.png)

More examples in the [documentation](https://josephbarbierdarnal.github.io/dayplot/).

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

> `dayplot` is supported by [Matplotlib Journey](https://www.matplotlib-journey.com/), an interactive online course designed to make you a master of Matplotlib. If you want to **support `dayplot`** and **become a Matplotlib expert**, consider purchasing the course!
