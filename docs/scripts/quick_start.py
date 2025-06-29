########################################################################
# Generate quick start example images
########################################################################

import matplotlib.pyplot as plt

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
    start_date="2024-01-01",
    end_date="2024-12-31",
    cmap="Reds",
    ax=ax,
)
fig.savefig("docs/img/quickstart-cmap.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    mutation_scale=1.22,
    ax=ax,
)
fig.savefig("docs/img/quickstart-gap.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    color_for_none="#5d5d5d",
    edgecolor="#2a2929",
    edgewidth=0.4,
    cmap="cividis_r",
    day_kws={"color": "white"},
    month_kws={"color": "white"},
    ax=ax,
)
fig.set_facecolor("#2a2929")
ax.set_facecolor("#2a2929")
fig.savefig("docs/img/quickstart-dark.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    df["dates"],
    df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    boxstyle="circle",
    ax=ax,
)
fig.savefig("docs/img/quickstart-boxstyle.png", bbox_inches="tight", dpi=300)

########################################################################

fig, ax = plt.subplots(figsize=(16, 4))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
    **dp.styles["github"],
)
fig.set_facecolor("#0d1117")
ax.set_facecolor("#0d1117")
fig.savefig("docs/img/quickstart-github.png", bbox_inches="tight", dpi=300)

########################################################################

plt.close("all")
