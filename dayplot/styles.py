from matplotlib.colors import LinearSegmentedColormap

github_style = dict(
    boxstyle="round",
    cmap=LinearSegmentedColormap.from_list(
        name="github",
        colors=["#151b23", "#033a16", "#196c2e", "#2ea043", "#56d364"],
    ),
    day_kws={"color": "white", "size": 12},
    month_kws={"color": "white", "size": 12},
    color_for_none="#151b23",
    day_x_margin=0.03,
    month_y_margin=0.6,
    mutation_scale=0.85,
)

styles = {
    "github": github_style,
}
