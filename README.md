# dayplot

## Quick start

```py
import dayplot as dp

df = dp.load_dataset()  # requires pandas to be installed

fig, ax = dp.github_chart(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

![](img/quickstart.png)

<br><br>

## Customization

- Change colormap

```py
import dayplot as dp

df = dp.load_dataset()

fig, ax = dp.github_chart(
    df["dates"],
    df["values"],
    cmap="Reds", # any matplotlib colormap
    start_date="2024-01-01",
    end_date="2024-12-31",
)
```

![](img/cmap.png)

<br>

- Change other colors

```py
import dayplot as dp

df = dp.load_dataset()

fig, ax = dp.github_chart(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    edgecolor="white",      # any matplotlib color
    color_for_none="black", # any matplotlib color
    edgewidth=1,
)
```

![](img/colors.png)

<br>

- Text styling

```py
import dayplot as dp

df = dp.load_dataset()

fig, ax = dp.github_chart(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    day_kws={"weight": "bold"},              # args passed to ax.text()
    month_kws={"size": 18, "color": "red"},  # args passed to ax.text()
    day_x_margin=0.03, # shift day labels to the left (default = 0.02)
    month_y_margin=0.7, # shift month labels to the top (default = 0.4)
)
```

![](img/text.png)

<br>

- Dark theme

```py
import dayplot as dp

df = dp.load_dataset()

fig, ax = dp.github_chart(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    color_for_none="black",
    edgecolor="white",
    edgewidth=1,
    day_kws={"color": "white"},
    month_kws={"color": "white"},
)
fig.set_facecolor("black")
ax.set_facecolor("black")
```

![](img/dark.png)

<br>

- Using your github contribs

> Find a github token here: https://github.com/settings/tokens

```py
from dotenv import load_dotenv
import os

import dayplot as dp

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# requires both pandas and requests to be installed
my_data = dp.fetch_github_contrib(
    username="JosephBARBIERDARNAL",
    github_token=token,
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-12-31T23:59:59Z",
)

fig, ax = dp.github_chart(
    my_data["dates"],
    my_data["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
)
```

![](img/github.png)

<br><br>

<!-- ## Upcoming feature

- padding between rectangles
- round borders
- change week of the day order -->
