import parseDoc
import numpy as np
import spacy
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")


def remove_tabs(sections: list) -> list:
    redact = ['-', '\n', '\t●', '\r']
    for i in range(len(sections)):
        text = sections[i]
        text = text.replace('%', ' percent')
        for r in redact:
            if r in text:
                text = text.replace(r, ' ')
        sections[i] = text
    return sections

def remove_punct(sections: list) -> list:
    for i in range(len(sections)):
        text = sections[i].strip()
        tokens = nlp(text)
        for token in tokens:
            if token.is_punct:
                text = text.replace(token.text, ' ')
        sections[i] = text
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
        text = sections[i].strip()
        tokens = nlp(text)
        for token in tokens:
            length = len(token.text.strip())
            if length > 0:
                s += token.lemma_ + ' '
        sections[i] = s
    return sections

def tokenize(sections: list) -> list:
    for i in range(len(sections)):
        text = sections[i].strip()
        sections[i] = word_tokenize(text)
    return sections

def get_cleaned_text(sections: list) -> list:
    tabs = remove_tabs(sections)
    punctuation = remove_punct(tabs)
    stop = remove_stopwords(punctuation)
    lem =  lemmatize(stop)
    return lem

def get_keywords(sections: list) -> list[list]:
    pos = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    keywords = []
    for text in sections:
        temp = []
        tokens = nlp(text)
        for token in tokens:
            if token.pos_ in pos or not token.is_alpha:
                temp.append(token.text)
        keywords.append(temp)
    return keywords

def get_frequency(sections: list[list]) -> list[dict]:
    list = []
    for section in sections:
        temp = {}
        for text in section:
            if text in temp.keys():
                temp[text] += 1
            else:
                temp[text] = 1
        temp = sorted(temp.items(), key = lambda item: item[1], reverse = True)
        temp = dict(temp)
        print(temp)
        list.append(temp)
    # return list 




headers = parseDoc.get_headers('335.docx')
texts = parseDoc.get_text('335.docx', headers)
clean = get_cleaned_text(texts)
key = get_keywords(clean)
print(get_frequency(key))
