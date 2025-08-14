# Fetch Github contributions

`dayplot` provides a simple function to fetch Github contributions data from a given Github username.

<br>

::: dayplot.fetch_github_contrib

## Examples

```python
import dayplot as dp
from dotenv import load_dotenv
import os

# generate a token: https://github.com/settings/tokens
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

start_date_iso = "2024-01-01T00:00:00Z"
end_date_iso = "2024-12-31T23:59:59Z"

my_data = fetch_github_contrib(
   username="y-sunflower",
   github_token=token,
   start_date=start_date_iso,
   end_date=end_date_iso,
   backend="pandas"
)

my_data.head() # it's a pandas dataframe
```
