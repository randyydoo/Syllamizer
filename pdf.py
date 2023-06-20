from pdf2docx import Converter

def convert(pdf_name: str, docx_name: str):
    cv = Converter(pdf_name)
    new = cv.convert(docx_name)      
    cv.close()

