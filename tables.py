import pandas as pd
import parseTables

def get_xlsx(fileName):
    dFrames = []
    keys = parseTables.get_keys(fileName)
    contents = parseTables.get_contents(fileName)
    for i, table in enumerate(keys):
        dict = {}
        for key in table:
            dict[key] = []

        for row in contents[i]:
            for j, content in enumerate(row):
                key = keys[i][j]
                dict[key].append(content)
        dFrames.append(dict)



    writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')

    for i, frame in enumerate(dFrames):
        df = pd.DataFrame(frame)
        df.to_excel(writer, sheet_name = f'Sheet {i + 1}', index = False)



get_xlsx('335.docx')
