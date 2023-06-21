from docx import Document
import PyPDF2

def is_bold(cell: 'class') -> bool:
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            if not run.bold:
                return False
    return True
def get_keys_tables(docx: str) -> list[list[str]]:
    redact = ['Grade', 'Percentage']
    keys = []  
    contents = [] 
    doc = Document(docx)

    for table in doc.tables:
        contentTemp, keyTemp = [], []
        bold, skip= True, False
        for i, row in enumerate(table.rows):
            temp = []
            for cell in row.cells:
                if cell.text in redact:
                    skip = True
                if is_bold(cell) and i == 0:
                    keyTemp.append(cell.text)
                elif len(keyTemp) != 0:
                    if cell.text == '':
                        temp.append('None')
                    else:
                        temp.append(cell.text)
            if len(temp) != 0:
                contentTemp.append(temp)
        if len(contentTemp) != 0 and not skip:
            contents.append(contentTemp)
        if len(keyTemp) != 0 and not skip:
            keys.append(keyTemp)
    print(keys)
    print(len(contents))
    print(contents)

# def get_content_tables(docx: str) -> list[list[str]]:


def get_text(docx: str) -> None:
    # read text starting from bold and end when new bold word
    doc = Document(docx)
    count = 0
    for paragraph in doc.paragraphs:
        print(paragraph.text)
        count += 1
        if count == 3:
            return
get_keys_tables('362.docx')
