from docx import Document
import PyPDF2

redact = ['Grade', 'Percentage' 'A:', 'A-']
def is_bold(cell: 'class') -> bool:
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            if not run.bold:
                return False
    return True

def get_keys_tables(docx: str) -> list[list[str]]:
    keys = []  
    contents = [] 
    doc = Document(docx)    
    for table in doc.tables:
        contentTemp, keyTemp = [], []
        new, extend = False, False
        bold, skip= True, False
        for i, row in enumerate(table.rows):
            temp = []
            for j, cell in enumerate(row.cells):
                if j + i == 0:
                    try:
                        prev = int(contents[-1][-1][0])
                        curr = int(cell.text)
                        if curr - prev == 1:
                            extend = True
                    except:
                        try:
                            curr = int(cell.text)
                            if curr <= 20:
                                new = True
                        except:
                            continue
                if cell.text in redact:
                    skip = True
                if is_bold(cell) and i == 0:
                    keyTemp.append(cell.text)
                elif len(keyTemp) != 0 or new is True or extend is True:
                    if cell.text == '':
                        temp.append('None')
                    else:
                        temp.append(cell.text)
            if extend is True and len(temp) > 0:
                contents[-1].append(temp)
            elif len(temp) != 0:
                contentTemp.append(temp)
        if len(contentTemp) != 0 and not skip:
            contents.append(contentTemp)
        if len(keyTemp) != 0 and not skip:
            keys.append(keyTemp)
    print(len(keys))
    print(len(contents))



def get_content_tables(docx: str) -> list[list[str]]:
    contents = []
    doc = Document(docx)
    for table in doc.tables:
        contentTemp = []
        skip = False
        for i, row in enumerate(table.rows):
            temp = []
            for cell in row.cells:
                if i == 0 and cell.text in redact:
                    skip = True
                elif cell.text == '' or len(cell.text) == 0:
                    temp.append('None')
                else:
                    temp.append(cell.text)
            if len(temp) > 0 and skip is False:
                contentTemp.append(temp)
        if len(contentTemp) > 0 and skip is False:
            contents.append(contentTemp)
    # print(contents)
    # print(len(contents))


def get_text(docx: str) -> None:
    # read text starting from bold and end when new bold word
    doc = Document(docx)
    count = 0
    for paragraph in doc.paragraphs:
        print(paragraph.text)
        count += 1
        if count == 3:
            return
get_content_tables('335.docx')
get_keys_tables('240.docx')
