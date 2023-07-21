import parseDoc
import numpy as np
import spacy
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")

headers = parseDoc.get_headers('335.docx')
texts = parseDoc.get_text('335.docx', headers)

def remove_tabs(sections: list) -> list:
    redact = ['-', '\n', '\t●', '\r']
    for i in range(len(sections)):
        text = sections[i]
        for r in redact:
            if r in text:
                text = text.replace(r, ' ')
        sections[i] = text
    return sections

def remove_punct(sections: list) -> list:
    for i in range(len(sections)):
        text = sections[i]
        tokens = nlp(text)
        for token in tokens:
            if token.is_punct:
            # if token.is_punct and token.text != '%':
                text = text.replace(token.text, '')
        sections[i] = text.strip()
    return sections

def remove_stopwords(sections: list) -> list:
    for i in range(len(sections)):
        s = ''
        text = sections[i]
        tokens = nlp(text)
        for token in tokens:
            if not token.is_stop:
                s += token.text + ' '
        sections[i] = s
    return sections

def lemmatize(sections: list) -> list:
    for i in range(len(sections)):
        s = ''
        text = sections[i]
        tokens = nlp(text)
        for token in tokens:
            if len(token.text.strip()) != 0:
                s += token.lemma_ + ' '
        sections[i] = s
    return sections

def tokenize(sections: list) -> list:
    for i in range(len(sections)):
        text = sections[i]
        sections[i] = word_tokenize(text)
    return sections

