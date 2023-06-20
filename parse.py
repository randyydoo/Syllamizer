from docx import Document
import PyPDF2

def is_bold(cell: 'class') -> bool:
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            if not run.bold:
                return False
    return True
def get_tables(docx: str) -> None:
    keys = []  #list of lists list of tables and contents
    contents = []
    doc = Document(docx)

    for table in doc.tables:
        firstRow = table.rows[0] 
        temp = []
        bold = True
        for cell in firstRow.cells:
            if is_bold(cell):
                temp.append(cell.text)
        if len(temp) != 0:
            keys.append(temp)
    print(keys)

def get_title(docx: str) -> str:

def get_text(docx: str) -> None:
    # read text starting from bold and end when new bold word
    doc = Document(docx)
    count = 0
    for paragraph in doc.paragraphs:
        print(paragraph.text)
        count += 1
        if count == 3:
            return
get_tables('240.docx')
