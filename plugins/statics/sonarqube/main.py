import os

import requests

from staticfiles import SONARQUBE_AVAILABLE_METRICS, SONARQUBE_SUPPORTED_MEASURES


class Sonarqube:
    def __init__(self):
        self.endpoint = os.getenv(
            "SONAR_URL", "https://sonarcloud.io/api/metrics/search"
        )

    def parser_data(self, input_file):
        parsed_values = [input_file.get("baseComponent",[]),input_file.get("components",[])]
        return self.__extract_sonarqube_supported_metrics(parsed_values)


    def extract_supported_metrics(self, metrics, first_request=False):
        data = SONARQUBE_AVAILABLE_METRICS

        if not first_request:
            return self.__extract_sonarqube_supported_metrics(metrics, data)

        try:
            request = requests.get(self.endpoint)
            data = request.json() if request.ok else SONARQUBE_AVAILABLE_METRICS

        except Exception:
            data = SONARQUBE_AVAILABLE_METRICS

        finally:
            return self.__extract_sonarqube_supported_metrics(metrics, data)

    def __extract_sonarqube_supported_metrics(self, metrics):
        collected_metrics = {}
        supported_metrics = []

        # NOTE: list comprehension que preenche o supported_metrics apenas
        #       com os valores das "metrics" do dicionário de SUPPORTEDs
        [
            supported_metrics.extend(list(measure.values())[0]["metrics"])
            for measure in SONARQUBE_SUPPORTED_MEASURES
        ]

        for component in metrics:
            qualifier = component["qualifier"]
            path = component["path" if qualifier != "TRK" else "name"]
            collected_metrics[path] = {"qualifier": qualifier, "measures": []}

            for obj in component["measures"]:
                metric_key = obj["metric"]
                if metric_key not in supported_metrics:
                    continue

                collected_metrics[path]["measures"].append(
                    {"metric": metric_key, "value": float(obj["value"])}
                )

        return collected_metrics


def parser(input_file):
    return Sonarqube().parser_data(input_file)