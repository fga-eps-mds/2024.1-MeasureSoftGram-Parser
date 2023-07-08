import os
import pytest
from genericparser.genericparser import GenericParser
from genericparser.accept_plugins import ACCEPT_PLUGINS

@pytest.fixture
def parser():
    token = "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"
    return ParserGithub(token)

def test_parser_extract(parser):
    repository = "fga-eps-mds/2023-1-MeasureSoftGram-Parser"

    result = parser.extract(repository)

    assert isinstance(result, dict)
    assert "metrics" in result
    assert "values" in result
    assert "file_paths" in result