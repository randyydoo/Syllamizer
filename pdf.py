from pdf2docx import Converter

def convert(pdf_name, docx_name):
    cv = Converter(pdf_name)
    new = cv.convert(docx_name)      # all pages by default
    cv.close()
