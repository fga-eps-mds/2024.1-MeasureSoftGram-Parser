from genericparser.plugins.domain.generic_class import GenericStaticABC


class ParserSonarQube(GenericStaticABC):
    def extract(self, input_file):
        metrics = []
        keys = []
        values = []

        input_interable = []
        for entry in input_file:
            if type(input_file[entry]) == list:
                input_interable.extend(input_file[entry])
            else:
                input_interable.append(input_file[entry])

        for entry in input_interable:
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
