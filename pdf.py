import pdfplumber

pdf_name = 'insert/pdf/name/here'

def get_table():
    table = {}
    pdf = pdfplumber.open(f'{pdf_name}.pdf')
    first = pdf.pages[0]
    lists = first.extract_table()
    print(lists)
    for i in range(len(lists) - 1):
        for j in range(len(lists[i])):
            title = lists[i][j]
            text = lists[i + 1][j]
            table[title] = text
    return table
