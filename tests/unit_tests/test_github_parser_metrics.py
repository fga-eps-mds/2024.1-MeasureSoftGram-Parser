import pytest
from genericparser.plugins.dinamic.github import ParserGithub
import json


#@pytest.mark.parametrize()
BASE_URL="https://api.github.com/repos/fga-eps-mds/2023-1-MeasureSoftGram-Parser"


def mock_requests(self,url,token):
    if url is BASE_URL:
        return_file = open("tests/mockfiles/response_api_general.json")
        return json(return_file)
    if url is f"{BASE_URL}/community/profile":
        return_file = open("tests/mockfiles/response_api_community_profile.json")
        return json(return_file)
        

# def get_object():

#     return parser


# def test_get_statistics_weekly_code_frequency(url, token):
#     parserObject = get_test_object()
#     assert parserObject._get_statistics_weekly_code_frequency(url, token) == param

def test_return_community():
    value = ParserGithub()
    print(value)
    # value._make_request = mock_requests
    # print(value._get_comunity_metrics(BASE_URL))
    assert False
    