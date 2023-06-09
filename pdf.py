from pdf2docx import Converter
from docx.shared import Pt, Cm
from docx import Document
import PyPDF2

t1 = {}
def convert(pdf_name, docx_name):
    cv = Converter(pdf_name)
    new = cv.convert(docx_name)      # all pages by default
    cv.close()
    doc = Document(docx_name) 
    for table in doc.tables:
        table.autofit = False
        for row in table.rows:
            row.height //= 3
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if run.font.size is not None:
                            run.font.size //= 3
    doc.save(docx_name)

        # table.autofit = False
        # for row in table.rows:
        #     row.height = 130000
    # doc.save(docx_name)

def get_tables(docx):
    data = []
    doc = Document(docx)
    for table in doc.tables:
        keys = None
        for i, row in enumerate(table.rows):
            text = (cell.text.replace('\n', ' ')for cell in row.cells)
            if i == 0:
                keys = text
                continue
            row_data = dict(zip(keys, text))
            data.append(row_data)
    print(data)
convert('335.pdf', '335.docx')
