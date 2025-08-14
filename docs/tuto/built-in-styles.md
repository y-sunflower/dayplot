`dayplot` ships a few built-in styles so that you can style your heatmap super quickly.

> Currently, there is only the "Github" style. But I'm planning to add more, and if you have suggestions it's more than welcome! You can just [open an issue](https://github.com/y-sunflower/dayplot/issues){target="\_blank"}

### Use pre-defined styles

=== "Github"

      ```python hl_lines="8 17"
      # mkdocs: render
      import matplotlib.pyplot as plt
      import dayplot as dp
      from dayplot import load_dataset

      df = load_dataset()

      style = dp.styles["github"]

      fig, ax = plt.subplots(figsize=(15, 6))
      dp.calendar(
         dates=df["dates"],
         values=df["values"],
         start_date="2024-01-01",
         end_date="2024-12-31",
         ax=ax,
         **style,
      )
      fig.set_facecolor("#0d1117")
      ax.set_facecolor("#0d1117")
      ```
