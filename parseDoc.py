from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as rt

links = ['@fullerton.edu', 'zoom.us']
headers = [
    'catalog description',
    'course description',
    'course goal',
    'course purpose',
    'required textbook',
    'grading standards and criteria',
    'description of assessed work',
    'late',
    'attendance policy',
    'attendance',
    'important dates'
]
def first_run_bold(paragraph: object) -> bool:
    for i, run in enumerate(paragraph.runs):
        if i == 0 and run.bold:
            return False
        else:
            return True

def get_links(file_name: str) -> dict:
    dict = {} # {rel_id: link} 
    doc = Document(file_name)
    rels = doc.part.rels

    for link in links:
        for rel in rels:
            link_url = rels[rel]._target 
            if rels[rel].reltype == rt.HYPERLINK and link in link_url and 'dsservices' not in link_url and 'StudentITHelpDesk' not in link_url:
                if link == '@fullerton.edu':
                    link_url = link_url[7:]
                dict[rel] = link_url
    return dict

def get_runs(file_name: str) -> dict:
    dict = {} # {'header': text}
    doc = Document(file_name)

    
    for header in headers:
        for paragraph in doc.paragraphs:
            for i, run in enumerate(paragraph.runs):
                if header in run.text.lower() and run.bold:
                    print(run.text)

get_runs('240.do')
