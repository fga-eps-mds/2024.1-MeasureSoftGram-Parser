import pytest
from genericparser.plugins.dinamic.github import ParserGithub
from tests.mockfiles.expected_return_values import (
    EXPECT_EXTRACT_METRICS,
)
import json


# @pytest.mark.parametrize()
BASE_URL = "https://api.github.com/repos/fga-eps-mds/2023-1-MeasureSoftGram-DOC"


def mock_requests(url, token=None):
    if url == BASE_URL:
        return_file = open("tests/mockfiles/response_api_github_general.json")
        return json.loads(return_file.read())
    if url == f"{BASE_URL}/actions/runs":
        return_file = open("tests/mockfiles/response_api_github_ci_feedback_times.json")
        return json.loads(return_file.read())
    if url == f"{BASE_URL}/issues?state=all&labels=US":
        return_file = open("tests/mockfiles/response_api_github_throughput.json")
        return json.loads(return_file.read())


def get_object():
    parser = ParserGithub()
    parser._make_request = mock_requests
    return parser


def test_extract_method():
    parserObject = get_object()
    assert (
        parserObject.extract(**{
            "input_file": "fga-eps-mds/2023-1-MeasureSoftGram-DOC",
            "filters": { "labels": "US" },
        })
        == EXPECT_EXTRACT_METRICS
    )
