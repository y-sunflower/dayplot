### Interactive heatmaps

You can combine `dayplot` with [plotjs](https://y-sunflower.github.io/plotjs/) to make them interactive:

```py
import matplotlib.pyplot as plt
import dayplot as dp
from plotjs import PlotJS

df = dp.load_dataset()

fig, ax = plt.subplots(figsize=(15, 6))
dp.calendar(
    dates=df["dates"],
    values=df["values"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    ax=ax,
)
PlotJS(fig).add_tooltip(labels=df["values"]).save("docs/img/interactive.html")
```

<div style="position:relative; width:100%; padding-top:40%;">
  <iframe
    src="../../img/interactive.html"
    style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;">
  </iframe>
</div>
