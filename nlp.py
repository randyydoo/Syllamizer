import parseDoc
import numpy as np
import spacy
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance
nltk.download('punkt')

nlp = spacy.load("en_core_web_sm")
stop_words = list(spacy.lang.en.stop_words.STOP_WORDS)

headers = parseDoc.get_headers('335.docx')
texts = parseDoc.get_text('335.docx', headers)


def clean_text(s: str) -> str:
    redact = ['\n', '\t●', '\r']
    for r in redact:
        if r in s:
            s = s.replace(r, '')
    return s

def clean_stopwords(sections: list) -> list:
    print(sections[0])
    lst = []
    cleared = []
    for section in sections:
        s = ''
        tokens = nlp(section)
        for token in tokens:
            if not token.is_stop:
                s += token.text + ' '
        lst.append(s)
    print(lst[0])
    # return lst

def get_new_text(texts: list) -> list:
    lst = []
    for text in texts:
        cleaned = clean_text(text)
        lst.append(cleaned)
    return lst

temp = get_new_text(texts)
clean_stopwords(temp)
