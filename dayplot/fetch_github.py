import requests
import pandas as pd


def fetch_github_contrib(
    username: str, github_token: str, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Fetches GitHub contributions for a given user and date range.

    Parameters
    ----------
    username : str
        GitHub username.
    github_token : str
        Personal access token for GitHub API. Find yours here: https://github.com/settings/tokens.
    start_date : str
        Start date in ISO 8601 format (e.g. "2024-01-01T00:00:00Z").
    end_date : str
        End date in ISO 8601 format (e.g. "2024-12-31T23:59:59Z").

    Returns
    -------
    Pandas DataFrame with dates and contribution counts.
    """
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

    records = []
    for week in weeks:
        for day in week["contributionDays"]:
            records.append({"dates": day["date"], "values": day["contributionCount"]})

    df = pd.DataFrame(records)
    df["dates"] = pd.to_datetime(df["dates"], format="%Y-%m-%d")
    df["values"] = df["values"].astype(int)
    return df


if __name__ == "__main__":
    import dayplot as dp
    from dotenv import load_dotenv
    import os

    # generate a token: https://github.com/settings/tokens
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    start_date_iso = "2024-01-01T00:00:00Z"
    end_date_iso = "2024-12-31T23:59:59Z"

    my_data = fetch_github_contrib(
        username="JosephBARBIERDARNAL",
        github_token=token,
        start_date=start_date_iso,
        end_date=end_date_iso,
    )

    fig, ax = dp.calendar(
        my_data["dates"],
        my_data["values"],
        start_date="2024-01-01",
        end_date="2024-12-31",
    )
