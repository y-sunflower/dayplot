import dayplot as dplot

df = dplot.load_sample()  # requires pandas to be installed

########################################################################

fig, ax = dplot.github_chart(
    df["date"], df["values"], start_date="2024-01-01", end_date="2024-12-31"
)

fig.savefig("img/quickstart.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = dplot.github_chart(
    df["date"],
    df["values"],
    cmap="Reds",
    start_date="2024-01-01",
    end_date="2024-12-31",
)

fig.savefig("img/cmap.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = dplot.github_chart(
    df["date"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    color_for_none="black",
    edgecolor="white",
    edgewidth=1,
)

fig.savefig("img/colors.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = dplot.github_chart(
    df["date"],
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

fig, ax = dplot.github_chart(
    df["date"],
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
