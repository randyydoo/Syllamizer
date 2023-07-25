import parseDoc
import string
from collections import Counter
import openai
import os
import numpy as np
import spacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
openai.api_key = "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"


def rewrite_text(text: str) -> str:
    max_tokens = len(word_tokenize(text))
    prompt = "Given this text from a syllabus, can you perform a sentence-level rewrite for each sentence while maintaining grammatical correctness and context. You can also remove any paragraph names if applicable and scentences that are incomplete due to missing contact informaiton. Please provide the output in sentence form. The text is as follows:"  + text
    response = openai.Completion.create(
    engine= "text-davinci-003",  
    prompt= prompt,
    max_tokens=max_tokens,)

    output = response['choices'][0]['text']
    return output

def clean_whitespace(sections: list) -> list:
    redact = [' ', '-', '\n\n', '\n', '\t', '\r', '●', '•'] 
    for i in range(len(sections)):
        text = sections[i]
        for r in redact:
            text = text.replace(r, '')

        sections[i] = text

    return sections

def remove_lists(cleaned: list) -> list:
    redact = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', 'a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'g.', 'h.', '●', '•']
    for i in range(len(cleaned)):
        text = cleaned[i]
        for r in redact:
            if r in text:
                text = rewrite_text(text)
        cleaned[i] = text

    return cleaned

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

# preprocessing text done
def get_cleaned_text(full_text: list) -> list:
    cleaned_whitespace = clean_whitespace(full_text)
    removed_lists = remove_lists(cleaned_whitespace)
    cleaned_punct = remove_punct(removed_lists)
    cleaned_stop = remove_stopwords(cleaned_punct)
    lem = lemmatize(cleaned_stop)
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

# get similarity of each scetence from OG text
def scentence_similarities(keywords: dict, text: str) -> dict:
    scores = {}
    doc = nlp(text)

    for scentence in doc.sents:
        for token in scentence:
            if token.text in keywords.keys():
                freq = keywords[scentence]
                if scentence in scores.keys():
                    scores[scentence] += freq
                else:
                    scores[scentence] = freq

    sort = sorted(scores, key = scores.get, reverse = True)
    return sort

def get_string(text: list) ->str:
    s = ''
    for scentence in text:
        scentence = scentence.capitalize()
        if scentence[-1] not in string.punctuation and len(scentence.strip()) > 20:
            s += f'{scentence.strip()}.'
        elif len(scentence.strip()) > 20:
            s += scentence
    return s

def get_top_scentences(file_name: str) -> str:
    top_sents = []
    whole_text = parseDoc.get_full_text(file_name)
    c = get_cleaned_text(whole_text)
    keys = get_keywords(c)
    freq = normalize_frequency(keys)

    white = clean_whitespace(whole_text)
    txt = remove_lists(white)
    txt_string = get_string(txt)
    similarity = scentence_similarities(freq,txt_string) 
    
    for i in range(5):
        top_sents.append(similarity[i].text)

    summary = " ".join(top_sents)
    return rewrite_text(summary)



