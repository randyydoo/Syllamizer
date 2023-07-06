import pandas as pd
import tables

dict = {}


keys = tables.get_keys('335.docx')
contents = tables.get_contents('335.docx')

for table in keys:
    for key in table:
        dict[key] = []

for i, table in enumerate(contents): 
    for row in table:
        for j,content in enumerate(row):
            key = keys[i][j]
            dict[key].append(content)
df = pd.DataFrame(dict)
print(df)
