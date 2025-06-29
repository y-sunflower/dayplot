import pytest
import requests
import pandas as pd
from unittest.mock import patch, MagicMock

from dayplot import fetch_github_contrib


@pytest.mark.parametrize("backend", ["pandas", "polars"])
def test_fetch_github_contrib_missing_token(backend):
    """
    Test that the function raises an EnvironmentError if no GitHub token is provided.
    """
    with pytest.raises(EnvironmentError, match="invalid github_token"):
        fetch_github_contrib(
            username="testuser",
            github_token="",
            start_date="2024-01-01T00:00:00Z",
            end_date="2024-12-31T23:59:59Z",
            backend=backend,
        )


@patch("requests.post")
def test_fetch_github_contrib_request_error(mock_post):
    """
    Test that the function correctly handles HTTP errors (e.g., GitHub returning a non-200).
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("Test HTTP Error")
    mock_post.return_value = mock_response

    with pytest.raises(requests.HTTPError, match="Test HTTP Error"):
        fetch_github_contrib(
            username="testuser",
            github_token="fake_token",
            start_date="2024-01-01T00:00:00Z",
            end_date="2024-12-31T23:59:59Z",
        )


@patch("requests.post")
def test_fetch_github_contrib_valid_response(mock_post):
    """
    Test that a valid response from GitHub's API is parsed correctly into a DataFrame.
    """
    mock_json_response = {
        "data": {
            "user": {
                "contributionsCollection": {
                    "contributionCalendar": {
                        "totalContributions": 42,
                        "weeks": [
                            {
                                "contributionDays": [
                                    {"date": "2024-01-01", "contributionCount": 1},
                                    {"date": "2024-01-02", "contributionCount": 2},
                                ]
                            },
                            {
                                "contributionDays": [
                                    {"date": "2024-01-03", "contributionCount": 3},
                                    {"date": "2024-01-04", "contributionCount": 4},
                                ]
                            },
                        ],
                    }
                }
            }
        }
    }

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = mock_json_response
    mock_post.return_value = mock_response

    df = fetch_github_contrib(
        username="testuser",
        github_token="fake_token",
        start_date="2024-01-01T00:00:00Z",
        end_date="2024-12-31T23:59:59Z",
    )

    assert isinstance(df, pd.DataFrame), "Should return a DataFrame"
    assert list(df.columns) == ["dates", "values"], (
        "Columns should be ['dates', 'values']"
    )

    assert len(df) == 4
    assert df["values"].tolist() == [1, 2, 3, 4]
