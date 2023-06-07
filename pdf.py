from pdf2docx import Converter
from docx import Document
import PyPDF2

t1 = {}
def convert(pdf_name, docx_name):
    cv = Converter(pdf_name)
    new = cv.convert(docx_name)      # all pages by default
    cv.close()

def get_tables(docx):
    data = []
    doc = Document(docx)
    table = doc.tables[0]
    keys = None
    for i, row in enumerate(table.rows):
        text = (cell.text.replace('\n', ' ')for cell in row.cells)
        if i == 0:
            keys = tuple(text)
            continue
        row_data = dict(zip(keys, text))
        data.append(row_data)
        print (data)
get_tables('335.docx')
