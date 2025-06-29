import narwhals as nw


def fetch_github_contrib(
    username: str,
    github_token: str,
    start_date: str,
    end_date: str,
    backend: str = "pandas",
):
    """
    Fetches GitHub contributions for a given user and date range. It requires
    `requests` and `pandas` to be installed.

    Args:
      username: GitHub username.
      github_token: Personal access token for GitHub API. Find yours
        [here](https://github.com/settings/tokens).
      start_date: Start date in ISO 8601 format (e.g. "2024-01-01T00:00:00Z").
      end_date: End date in ISO 8601 format (e.g. "2024-12-31T23:59:59Z").
      backend: The output format of the dataframe. Note that, for example,
        if you set `backend="polars"`, you must have polars installed. Must
        be one of the following: "pandas", "polars", "pyarrow", "modin",
        "cudf". Default to "pandas".

    Returns:
      A DataFrame with dates and contribution counts.
    """
    import requests

    if not github_token:
        raise EnvironmentError("invalid github_token")
    headers = {"Authorization": f"Bearer {github_token}"}

    url = "https://api.github.com/graphql"

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    variables = {
        "login": username,
        "from": start_date,
        "to": end_date,
    }

    response = requests.post(
        url, json={"query": query, "variables": variables}, headers=headers
    )
    response.raise_for_status()
    data = response.json()

    calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = calendar["weeks"]

    records = [
        {"dates": day["date"], "values": day["contributionCount"]}
        for week in weeks
        for day in week["contributionDays"]
    ]

    dict_records = {
        "dates": [entry["dates"] for entry in records],
        "values": [entry["values"] for entry in records],
    }

    df = nw.from_dict(dict_records, backend=backend)
    return df.to_native()
