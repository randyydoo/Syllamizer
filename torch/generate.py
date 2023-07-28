import torch
from transformers import T5Tokenizer, TFT5ForConditionalGeneration


def generate_summary(text: str) -> str:
    model_name = 'T5-Summarizer-Model'
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = TFT5ForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer.encode('Summarize: 'text, return_tensors='pt', truncation=True)
    outputs = model.generate(inputs, decoder_input_ids=inputs)

    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary

