import pandas as pd
import parseTables


dFrames = []


keys = parseTables.get_keys('335.docx')
contents = parseTables.get_contents('335.docx')

for i, table in enumerate(keys):
    dict = {}
    for key in table:
        dict[key] = []
    for row in contents[i]:
        for j, content in enumerate(row):
            key = keys[i][j]
            dict[key].append(content)
    dFrames.append(dict)


