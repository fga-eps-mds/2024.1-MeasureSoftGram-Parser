import os

import requests
import pandas as pd
from plugins.statics.sonarqube.staticfiles import (
    SONARQUBE_AVAILABLE_METRICS,
    SONARQUBE_SUPPORTED_MEASURES,
)


class Sonarqube:
    def __init__(self):
        self.endpoint = os.getenv(
            "SONAR_URL", "https://sonarcloud.io/api/metrics/search"
        )

    def get_available_metrics(self):
        data = SONARQUBE_AVAILABLE_METRICS

        try:
            request = requests.get(self.endpoint)
            data = request.json() if request.ok else SONARQUBE_AVAILABLE_METRICS

        except Exception:
            data = SONARQUBE_AVAILABLE_METRICS

        return data

    def parser_data(self, input_file):
        metrics = []
        keys = []
        values = []

        # Iterar sobre os dados e extrair as informações
        for entry in input_file:
            key = entry["key"]
            measures = entry["measures"]
            for measure in measures:
                metric = measure["metric"]
                value = measure["value"]
                metrics.append(metric)
                keys.append(key)
                values.append(value)

        # Criar o DataFrame
        df = pd.DataFrame({"key": keys, "metric": metrics, "value": values})
        df_pivot = df.pivot(index="metric", columns="key", values="value")

        return df_pivot


def parser(input_file):
    return Sonarqube().parser_data(input_file)
