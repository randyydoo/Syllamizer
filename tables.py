import pandas as pd
from openpyxl import Workbook
import parseTables

def get_longest_str(d: dict) -> list:
    lengths = []
    for lst in d.values():
        max = 0 
        for text in lst:
            if len(text) > max:
                max = len(text)
        lengths.append(max)
    return lengths


def get_file(file_name: str) -> None:

    wb = Workbook() 

    keys = parseTables.get_keys(file_name)
    contents = parseTables.get_contents(file_name)
    dict = {letter: [0] for letter in string.ascii_uppercase} 

    for i, lst in enumerate(keys):
        temp_max = get_longest_str(lst)
        temp_sheet = wb.create_sheet(f'Sheet {i + 1}', i)
        temp_sheet.append(lst)

        for row in contents[i]:
            for j, text in enumerate(row):

            temp_sheet.append(row)
            max_len_str = get_longest_str(row)
            if max_len_str > temp_max:
                temp_max = max_len_str
            
    wb.save('ran.xlsx')







def get_xlsx(file_name: str) -> None:
    data_frames = []
    max_width = []    

    keys = parseTables.get_keys(file_name)
    contents = parseTables.get_contents(file_name)

    #create list of data frames
    for i, table in enumerate(keys):
        dict = {}
        for key in table:
            dict[key] = []

        for row in contents[i]:
            for j, content in enumerate(row):
                key = keys[i][j]
                dict[key].append(content)
        data_frames.append(dict)

    #get string len max to change cell width 
    for d in data_frames:
        widths = get_longest_str(d)
        max_width.append(widths)




    # need to figure out how to get cell wider

    # df = pd.DataFrame(data = data_frames[1])
    # pd.set_option('display.max_columns', None)
    # df.to_excel('kdakdk.xlsx', index=False)


get_file('335.docx')
