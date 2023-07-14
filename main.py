import pdf
import tables

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
