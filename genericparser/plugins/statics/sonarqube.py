from genericparser.plugins.domain.generic_class import GenericStaticABC


class ParserSonarQube(GenericStaticABC):
    def extract(self, input_file):
        metrics = []
        keys = []
        values = []
        for entry in input_file:
            key = entry.get("key", {})
            measures = entry.get("measures", [])
            for measure in measures:
                metric = measure.get("metric", None)
                value = measure.get("value", None)
                metrics.append(metric)
                keys.append(key)
                values.append(value)
        return {"file_paths": keys, "metrics": metrics, "values": values}


def main():
    return ParserSonarQube()
