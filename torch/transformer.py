from datasets import load_dataset
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
import nltk
import numpy as np
import torch

dataset = load_dataset("xsum")
metric = evaluate.load("rouge")

tokenizer = AutoTokenizer.from_pretrained('t5-small')
device = 'mps' if torch.backends.mps.is_available() else "cpu"
model = AutoModelForSeq2SeqLM.from_pretrained('t5-small')
model = model.to(device)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

def preprocess(examples):
    inputs = []
    for doc in examples['document']:
        inputs.append('Summarize: ' + doc)

    model_inputs = tokenizer(inputs, max_length=1024, truncation=True)
    labels = tokenizer(text_target=examples["summary"], max_length=256, truncation=True)

    model_inputs["labels"] = labels["input_ids"]

    return model_inputs

def compute_metrics(model_preds: tuple) ->float:
    # (input_ids, labels) tokenized
    predictions, labels = model_preds
    decode_predictions = tokenizer.batch_decode(predictions, skip_special_tokens=True)

    # replace non decodable tokens with -100
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decode_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    # join scentences
    decoded_preds = ["\n".join(nltk.sent_tokenize(pred.strip())) for pred in decode_predictions]
    decoded_labels = ["\n".join(nltk.sent_tokenize(label.strip())) for label in decode_labels]

    # compute similarity 
    result = metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True, use_aggregator=True)

    # get a some results
    result = {key: value * 100 for key, value in result.items()}
    
    # Add mean generated length
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in predictions]
    result["gen_len"] = np.mean(prediction_lens)
    
    return {k: round(v, 4) for k, v in result.items()}

def train() -> None:
    tokenized_datasets = dataset.map(preprocess, batched=True)
    small_train_dataset, small_eval_dataset = {}, {}

    #train with sets of 800 
    small_train_dataset['document'] = tokenized_datasets['train']['document'][800:1600]
    small_train_dataset['summary'] = tokenized_datasets['train']['summary'][800:1600]

    small_eval_dataset['document'] = tokenized_datasets['validation']['document'][800:1600]
    small_eval_dataset['summary'] = tokenized_datasets['validation']['summary'][800:1600]

    args = Seq2SeqTrainingArguments(
        output_dir = 'model-tests',
        evaluation_strategy = "epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        weight_decay=0.01,
        save_total_limit=3,
        predict_with_generate=True,
        num_train_epochs=1,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )
    trainer.train()
    trainer.save_model('T5-Summarizer-Model')
train()
