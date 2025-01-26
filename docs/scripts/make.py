import matplotlib.pyplot as plt
from pypalettes import load_cmap
from pyfonts import load_font
import os
import pandas as pd
from dotenv import load_dotenv

import dayplot as dp

df = dp.load_dataset()

########################################################################

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    df["dates"], df["values"], start_date="2024-01-01", end_date="2024-12-31", ax=ax
)
fig.savefig("docs/img/quickstart.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    df["dates"],
    df["values"],
    cmap="Reds",
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
fig.savefig("docs/img/basic-styling/cmap.png", bbox_inches="tight", dpi=300)

########################################################################

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
fig.savefig("docs/img/basic-styling/colors.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    day_kws={"weight": "bold"},
    month_kws={"size": 20, "color": "red"},
    day_x_margin=0.03,  # default = 0.02
    month_y_margin=0.7,  # default = 0.4
    ax=ax,
)
fig.savefig("docs/img/basic-styling/text.png", bbox_inches="tight", dpi=300)

########################################################################

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
my_data = dp.fetch_github_contrib(
    username="JosephBARBIERDARNAL",
    github_token=token,
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-12-31T23:59:59Z",
)
fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    my_data["dates"],
    my_data["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
fig.savefig("docs/img/github/github.png", bbox_inches="tight", dpi=300)

########################################################################

df = dp.load_dataset()
fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2025-01-01",
    end_date="2025-12-31",
    ax=ax1,  # top axes
)
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax2,  # bottom axes
)

fig.savefig(
    "docs/img/combine-charts/combine-charts-1.png", bbox_inches="tight", dpi=300
)

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2025-01-01",
    end_date="2025-12-31",
    ax=ax1,  # top axes
)
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax2,  # bottom axes
)
text_args = dict(x=-4, y=3.5, size=30, rotation=90, color="#afafaf", va="center")
ax1.text(s="2025", **text_args)
ax2.text(s="2024", **text_args)
fig.savefig(
    "docs/img/combine-charts/combine-charts-2.png", bbox_inches="tight", dpi=300
)

########################################################################

df = dp.load_dataset()

df.loc[df.sample(n=40, replace=False).index, "values"] *= -1
fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    cmap="RdBu",  # use a diverging colormap
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
fig.savefig(
    "docs/img/negative-values/negative-values-1.png", bbox_inches="tight", dpi=300
)

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    cmap="RdBu",  # use a diverging colormap
    start_date="2024-01-01",
    end_date="2024-12-31",
    vmin=-3,
    vcenter=0,
    vmax=10,
    ax=ax,
)
fig.savefig(
    "docs/img/negative-values/negative-values-2.png", bbox_inches="tight", dpi=300
)

########################################################################

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    boxstyle="circle",
    ax=ax,
)
fig.savefig("docs/img/boxstyle/boxstyle-1.png", bbox_inches="tight", dpi=300)

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    boxstyle="round",
    ax=ax,
)
fig.savefig("docs/img/boxstyle/boxstyle-2.png", bbox_inches="tight", dpi=300)

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    boxstyle="sawtooth",
    ax=ax,
)
fig.savefig("docs/img/boxstyle/boxstyle-3.png", bbox_inches="tight", dpi=300)

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    boxstyle="roundtooth",
    ax=ax,
)
fig.savefig("docs/img/boxstyle/boxstyle-4.png", bbox_inches="tight", dpi=300)

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    alpha=0.5,
    ax=ax,
)
fig.savefig("docs/img/boxstyle/boxstyle-5.png", bbox_inches="tight", dpi=300)

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    mutation_scale=1.15,
    ax=ax,
)
fig.savefig("docs/img/boxstyle/boxstyle-6.png", bbox_inches="tight", dpi=300)

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    hatch="*",
    ax=ax,
)
fig.savefig("docs/img/boxstyle/boxstyle-7.png", bbox_inches="tight", dpi=300)

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    linestyle="--",
    edgewidth=1,
    ax=ax,
)
fig.savefig("docs/img/boxstyle/boxstyle-8.png", bbox_inches="tight", dpi=300)

########################################################################

df = pd.read_csv("city_temperature.csv", low_memory=False)
df = df[df["City"] == "Tunis"]
df = df[df["Year"].isin([2017, 2018, 2019])]
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
df = df[df["AvgTemperature"] != -99.0]

cmap = load_cmap("jazz_city", cmap_type="continuous", reverse=True)
font_url = "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf"
fontlight = load_font(f"{font_url}/Urbanist-Light.ttf?raw=true")
fontmedium = load_font(f"{font_url}/Urbanist-Medium.ttf?raw=true")

style_args = dict(
    cmap=cmap,
    day_kws={"font": fontlight},
    month_kws={"font": fontlight},
    day_x_margin=0.03,
    month_y_margin=0.5,
)

fig, axs = plt.subplots(nrows=3, figsize=(15, 5))
dp.calendar(
    df["Date"],
    df["AvgTemperature"],
    start_date="2019-01-01",
    end_date="2019-12-31",
    ax=axs[0],
    **style_args,
)
dp.calendar(
    df["Date"],
    df["AvgTemperature"],
    start_date="2018-01-01",
    end_date="2018-12-31",
    ax=axs[1],
    **style_args,
)
dp.calendar(
    df["Date"],
    df["AvgTemperature"],
    start_date="2017-01-01",
    end_date="2017-12-31",
    ax=axs[2],
    **style_args,
)
fig.text(
    x=0.5,
    y=0.94,
    s="Average temperature in Tunis, Tunisia",
    size=20,
    ha="center",
    font=fontmedium,
)
fig.text(
    x=0.75,
    y=0.08,
    s="made with dayplot",
    size=7,
    ha="right",
    font=fontmedium,
)
text_args = dict(
    x=-6, y=3.5, size=30, rotation=90, color="#aaa", va="center", font=fontlight
)
axs[0].text(s="2019", **text_args)
axs[1].text(s="2018", **text_args)
axs[2].text(s="2017", **text_args)

fig.savefig("docs/img/advanced/advanced-1.png", bbox_inches="tight", dpi=300)

########################################################################

plt.close("all")
