from main import ParserGeneric
from tests.mockfiles.mock_input_pandas_transform import dataframe_input
from tests.mockfiles.mock_output_pandas_transform import dict_output


def test_df_to_dict_test():
    assert ParserGeneric().transform_df_to_python_dict(dataframe_input) == dict_output
