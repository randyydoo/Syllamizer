from pdf2docx import Converter

def convert(pdf_name: str, docx_name: str):
    cv = Converter(pdf_name)
    new = cv.convert(docx_name)      
    cv.close()


convert('335.pdf', '335.docx')
convert('240.pdf', '240.docx')
def get_file_name():
    user_file_type = input("Is you syllabus a docx file? (y/n): ")

    if user_file_type == 'y' or user_file_type == 'Y':
        docx_name = input('Please input the docx name (without .docx) and make sure it is in the same directory: ')
        docx = f'{docx_name}.docx'
    else:
        pdf_name = input('Please input the pdf file name and make sure it is in the same directory: ')
        convert_file = f'{pdf_name}.pdf'
        docx = f'{pdf_name}.docx' 
        pdf.convert(f'{pdf_name}.pdf', docx)
