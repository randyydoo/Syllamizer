import torch
from transformers import T5Tokenizer, TFT5ForConditionalGeneration, pipeline


def generate_summary(text: str) -> str:
    model_name = './SumModel'
    
    pipe = pipeline('summarization', model=model_name, min_length=100)
    summ = pipe(text) 

    text = summ[0]['summary_text'] + '.'
    text = text.strip()

    return summ
