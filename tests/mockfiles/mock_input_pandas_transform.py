import pandas as pd

columns = ["Column 1", "Column 2", "Column 3", "Column 4", "Column 5"]
rows = ["Row 1", "Row 2", "Row 3", "Row 4", "Row 5"]
data = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25],
]

dataframe_input = pd.DataFrame(data=data, index=rows, columns=columns)
