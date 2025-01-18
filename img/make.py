from dotenv import load_dotenv
import os

import dayplot as dp

df = dp.load_dataset()  # requires pandas to be installed

########################################################################

fig, ax = dp.github_chart(
    df["dates"], df["values"], start_date="2024-01-01", end_date="2024-12-31"
)

fig.savefig("img/quickstart.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = dp.github_chart(
    df["dates"],
    df["values"],
    cmap="Reds",
    start_date="2024-01-01",
    end_date="2024-12-31",
)

fig.savefig("img/cmap.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = dp.github_chart(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    color_for_none="black",
    edgecolor="white",
    edgewidth=1,
)

fig.savefig("img/colors.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = dp.github_chart(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    day_kws={"weight": "bold"},
    month_kws={"size": 18, "color": "red"},
    day_x_margin=0.03,
    month_y_margin=0.7,
)

fig.savefig("img/text.png", bbox_inches="tight", dpi=300)

########################################################################

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

fig.savefig("img/dark.png", bbox_inches="tight", dpi=300)

########################################################################

# get your token: https://github.com/settings/tokens
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

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

fig.savefig("img/github.png", bbox_inches="tight", dpi=300)
