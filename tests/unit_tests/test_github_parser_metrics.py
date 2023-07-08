import pytest
from genericparser.plugins.dinamic.github import ParserGithub
from tests.mockfiles.expected_return_values import (
    EXPECT_EXTRACT_METRICS,
    EXPECTED_ALL_PULL_METRICS,
    EXPECTED_COMMIT_FREQUENCY_METRICS,
    EXPECTED_COMMUNITY_RETURN_METRICS,
    EXPECTED_PULL_METRICS,
)
import json


# @pytest.mark.parametrize()
BASE_URL = "https://api.github.com/repos/fga-eps-mds/2023-1-MeasureSoftGram-Parser"


def mock_requests(url, token=None):
    if url == BASE_URL:
        print("url is Base_url")
        return_file = open("tests/mockfiles/response_api_github_general.json")
        return json.loads(return_file.read())
    if url == f"{BASE_URL}/community/profile":
        return_file = open("tests/mockfiles/response_api_github_community_profile.json")
        return json.loads(return_file.read())
    if url == f"{BASE_URL}/stats/punch_card":
        return_file = open("tests/mockfiles/response_api_github_puch_card.json")
        return json.loads(return_file.read())
    if url == f"{BASE_URL}/pulls":
        return_file = open("tests/mockfiles/response_api_github_pull_request.json")
        return json.loads(return_file.read())
    if url == f"{BASE_URL}/pulls?state=all":
        return_file = open("tests/mockfiles/response_api_github_all_pull_metrics.json")
        return json.loads(return_file.read())


def get_object():
    parser = ParserGithub()
    parser._make_request = mock_requests
    return parser


def test_get_statistics_weekly_code_frequency():
    parserObject = get_object()
    assert (
        parserObject._get_statistics_weekly_code_frequency(BASE_URL)
        == EXPECTED_COMMIT_FREQUENCY_METRICS
    )


def test_return_community():
    parserObject = get_object()
    assert (
        parserObject._get_comunity_metrics(BASE_URL)
        == EXPECTED_COMMUNITY_RETURN_METRICS
    )


def test_pull_requests_metrics():
    parserObject = get_object()
    assert parserObject._get_pull_metrics(BASE_URL) == EXPECTED_PULL_METRICS


def test_all_pull_metrics():
    parserObject = get_object()
    assert parserObject._get_all_pull_metrics(BASE_URL) == EXPECTED_ALL_PULL_METRICS


def test_extract_method():
    parserObject = get_object()
    assert (
        parserObject.extract("fga-eps-mds/2023-1-MeasureSoftGram-Parser")
        == EXPECT_EXTRACT_METRICS
    )
