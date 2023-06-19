import importlib
import os
import json
import pandas as pd


class ParserGeneric:
    file_path_configuration = os.path.join(os.path.dirname(__file__), "plugins.json")
    df = None

    def __init__(self, file_path_configuration=None):
        self.file_path = file_path_configuration or self.file_path_configuration

    def parse(self, **kwargs):
        input_value = kwargs.get("input_value")
        type_input = kwargs.get("type_input")
        accepted_types = self.get_acepted_types()
        if type_input not in accepted_types:
            raise Exception("Type not acepted")

        path_plugin = self.get_path_plugin(type_input)
        return_from_plugin = self.call_plugin(path_plugin, input_value)

        if isinstance(return_from_plugin, pd.DataFrame):
            self.df = return_from_plugin
        else:
            self.df = self.get_df_from_parser(return_from_plugin)
        return self.transform_df_to_python_dict(self.df)

    def get_df_from_parser(self, dict_input: dict):
        df = pd.DataFrame(dict_input)
        df_pivot = df.pivot(index="metrics", columns="file_paths", values="values")
        return df_pivot

    def get_acepted_types(self):
        full_json = json.load(open(self.file_path, "r"))
        return full_json.keys()

    def get_path_plugin(self, type_input):
        full_json = json.load(open(self.file_path, "r"))
        return full_json.get(type_input)

    def call_plugin(self, path_plugin, file_input):
        plugin = importlib.import_module(path_plugin)
        object = plugin.main()
        return object.parser(**{"input_value": file_input})

    def transform_df_to_python_dict(self, pandas_dataframe: pd.DataFrame):
        returned_dict = {}
        for column in pandas_dataframe.columns:
            returned_dict[column] = []
            for index, value in pandas_dataframe[column].items():
                returned_dict[column].append({"metric": index, "value": value})
        return returned_dict
