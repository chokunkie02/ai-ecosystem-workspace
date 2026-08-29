import json
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification
from datasets import Dataset

def run_training(dataset_path, base_model_name, output_dir, logger):
    logger.info("Loading dataset from local JSON...")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # Reconstruct Hugging Face Dataset
    ds = Dataset.from_dict(raw_data)
    # Take a subset for fast training
    small_ds = ds.select(range(min(100, len(ds))))
    
    logger.info("Initializing Tokenizer and Model...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    # CoNLL-2003 has 9 NER tags
    model = AutoModelForTokenClassification.from_pretrained(base_model_name, num_labels=9)
    
    def tokenize_and_align_labels(examples):
        tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
        labels = []
        for i, label in enumerate(examples["ner_tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != previous_word_idx:
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(-100)
                previous_word_idx = word_idx
            labels.append(label_ids)
        tokenized_inputs["labels"] = labels
        return tokenized_inputs

    logger.info("Tokenizing dataset...")
    tokenized_ds = small_ds.map(tokenize_and_align_labels, batched=True)
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=1,
        per_device_train_batch_size=8,
        logging_steps=10,
        save_strategy="no",
        report_to="none"
    )
    
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_ds,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )
    
    logger.info("Starting PyTorch/Transformers training loop...")
    train_result = trainer.train()
    logger.info(f"Training completed. Metrics: {train_result.metrics}")
    
    logger.info(f"Saving model artifacts to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
