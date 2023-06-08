import pandas as pd
import json

def processar_json(data):
    metrics = []
    keys = []
    values = []

# Iterar sobre os dados e extrair as informações
    for entry in data:
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

# Pivotar o DataFrame
    df_pivot = df.pivot(index="metric", columns="key", values="value")

# Imprimir o DataFrame pivotado
    print(df_pivot)