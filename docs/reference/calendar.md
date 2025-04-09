# calendar

::: dayplot.calendar

<br>

## Examples

```python
import dayplot as dp

df = dp.load_dataset()

dp.calendar(
   df["date"],
   df["values"],
   start_date="2024-01-01",
   end_date="2024-01-31"
)
```