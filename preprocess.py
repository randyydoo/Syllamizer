import parseDoc
import numpy as np
import spacy
import nltk
import string
from nltk import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance
from collections import Counter

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")


def remove_tabs(sections: list) -> list:
    redact = ['-', '\n', '\t●', '\r']
    for i in range(len(sections)):
        text = sections[i]
        text = text.replace('  ', ' ')
        # dont replace if using textrank for overall summary
        # text = text.replace('%', ' percent')
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

# preprocessing text done
def get_cleaned_text(sections: list) -> list:
    tabs = remove_tabs(sections)
    punctuation = remove_punct(tabs)
    stop = remove_stopwords(punctuation)
    lem =  lemmatize(stop)
    return lem

#start TextRank for overall summary
def get_keywords(cleaned_text: list) -> list:
    pos = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    keywords = []
    for text in cleaned_text:
        tokens = nlp(text)
        for token in tokens:
            if token.pos_ in pos or not token.is_alpha:
                keywords.append(token.text)
    return keywords

def normalize_frequency(keywords: list) -> list:
    dictonary = Counter(keywords)
    highest = Counter(keywords).most_common(1)[0][1]
    for word in dictonary.keys():
        dictonary[word] = dictonary[word]/highest
    return dictonary

def combine_text(texts: list) -> str:
    texts = remove_tabs(texts)
    for i in range(len(texts)):
        text = texts[i]
        if text[-1] != ".":
            text += '.'
        texts[i] = text

    collapsed = " ".join(texts)
    return collapsed 

# get similarity of each scetence from OG text
def scentence_similarities(keywords: dict, texts: list) -> dict:
    similarities = {}
    temp = ""
    # must remove tabs before
    # combine to one string to extract top freqencies
    for text in texts:
        temp += text + "."
     
    paragraph = nlp(temp)
    for scentence in paragraph.sents:
        for word in scentence:
            if word.text in keywords.keys():
                freq = keywords[word.text]
                if scentence in similarities.keys():
                    similarities[scentence] += freq
                else:
                    similarities[scentence] = freq
    print(similarities)

headers = parseDoc.get_headers('335.docx')
texts = parseDoc.get_text('335.docx', headers)
print(combine_text(texts))
# cleaned = get_cleaned_text(texts)
# key = get_keywords(cleaned)
# d = normalize_frequency(key)
# scentence_similarities(d, tabs)
