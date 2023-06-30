from docx import Document
import PyPDF2

redact = ['Grade', 'Grades','Percentage', 'A:', 'A-']
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
        newTable, extendTable = False, False
        bold, skip= True, False

        for i, row in enumerate(table.rows):
            tempRow = []

            for j, cell in enumerate(row.cells):
                if j + i == 0:
                    try:
                        prev = int(contents[-1][-1][0])
                        curr = int(cell.text)
                        if curr - prev == 1:
                            extendTable = True
                    except:

                        try:
                            curr = int(cell.text)
                            if curr <= 20:
                                newTaable = True
                        except:
                            continue

                if cell.text in redact:
                    skip = True
                if is_bold(cell) and i == 0:
                    keyTemp.append(cell.text)
                elif len(keyTemp) != 0 or newTable is True or extendTable is True:
                    if cell.text == '':
                        tempRow.append('None')
                    else:
                        tempRow.append(cell.text)
            if extendTable is True and len(tempRow) > 0:
                contents[-1].append(tempRow)
            elif len(tempRow) != 0:
                contentTemp.append(tempRow)
        if len(contentTemp) != 0 and not skip:
            contents.append(contentTemp)
        if len(keyTemp) != 0 and not skip:
            keys.append(keyTemp)


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
