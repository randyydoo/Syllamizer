import parseDoc
import nltk
import evaluate
import numpy as np
from datasets import load_dataset
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq


tokenizer = AutoTokenizer.from_pretrained('t5-small')
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
data = load_dataset('xsum')   # {splits = 'train', 'validation', 'test'}
metric = evaluate.load('rouge')
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

def get_accuracy(prediction: tuple) -> float:
    # prediction = (model output, label)
    outputs, labels = prediction
    decoded_outs = tokenizer.batch_decode(output, skip_special_tokens=True) 

    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    decoded_outs = ["\n".join(nltk.sent_tokenize(pred.strip())) for out in decoded_outs]
    decoded_labels = ["\n".join(nltk.sent_tokenize(label.strip())) for label in decoded_label]
    
    result = metric.compute(predictions=decoded_outs, references=decoded_labels, use_stemmer=True, use_aggregator=True)
    result = {key: value * 100 for key, value in result.items()}
    
    # Add mean generated length
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for out in outputs]
    result["gen_len"] = np.mean(prediction_lens)
    
    return {k: round(v, 4) for k, v in result.items()}


def preprocess(data_set: dict) -> dict: #{input_ids: target_ids}
    # {'document':  , 'summary':  , 'id': }
    # inputs = []
    prefix = 'Summarize: '
    # for doc in data_set['document']:
    inputs = [prefix + doc for doc in data_set['document']]
    #     inputs.append(f'Summarize: {doc}')

    model_inputs = tokenizer(inputs, max_length=1024, truncation=True)
    
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(data_set['summary'], max_length=128, truncation=True)

    model_inputs['decode_input_ids'] = labels['input_ids']

    return model_inputs

tokenized_dataset = data.map(preprocess, batched=True)
print(tokenized_dataset.keys())


training_args = Seq2SeqTrainingArguments(
    output_dir='model_tests',
    num_train_epochs=3,     
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    save_steps=1000,            
    save_total_limit=2,        
    logging_steps=100,        
    evaluation_strategy="epoch",
    eval_steps=1000,        
)
trainer = Seq2SeqTrainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset['train'],
            eval_dataset=tokenized_dataset['validation'],
            compute_metrics=get_accuracy,
            data_collator=data_collator,
            tokenizer=tokenizer
            )
trainer.train()
