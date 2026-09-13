import os
import json
import logging
import numpy as np
import torch
import mlflow
import mlflow.transformers
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    Trainer,
    TrainingArguments,
    DataCollatorForTokenClassification,
    pipeline,
)
from datasets import Dataset
from seqeval.metrics import f1_score, precision_score, recall_score, accuracy_score

LABEL_LIST = ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC"]
ID2LABEL = {i: label for i, label in enumerate(LABEL_LIST)}
LABEL2ID = {label: i for i, label in enumerate(LABEL_LIST)}

def run_training(
    dataset_path: str,
    base_model_name: str,
    output_dir: str,
    logger: logging.Logger,
    num_epochs: int = 1,
    batch_size: int = 8,
    learning_rate: float = 5e-5,
    experiment_name: str = None,
    registered_model_name: str = None,
) -> dict:
    """
    Run Hugging Face NER token classification training with MLflow tracking & model registry.
    """
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    experiment_name = experiment_name or os.getenv("MLFLOW_EXPERIMENT_NAME", "bert-ner-training")
    registered_model_name = registered_model_name or os.getenv("MLFLOW_MODEL_NAME", "bert-ner")

    logger.info(f"Connecting to MLflow Tracking Server at: {tracking_uri}")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    logger.info(f"MLflow Experiment set to '{experiment_name}'")

    logger.info("Loading dataset from local JSON...")
    with open(dataset_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # Reconstruct Hugging Face Dataset
    ds = Dataset.from_dict(raw_data)
    total_len = len(ds)
    subset_size = min(100, total_len)
    logger.info(f"Loaded dataset with {total_len} samples. Selecting subset of {subset_size} samples.")
    small_ds = ds.select(range(subset_size))

    # Split into train and evaluation sets
    if subset_size >= 10:
        split_ds = small_ds.train_test_split(test_size=0.2, seed=42)
        train_data = split_ds["train"]
        eval_data = split_ds["test"]
    else:
        train_data = small_ds
        eval_data = small_ds
    logger.info(f"Train samples: {len(train_data)}, Eval samples: {len(eval_data)}")

    logger.info(f"Initializing Tokenizer and Model from '{base_model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    model = AutoModelForTokenClassification.from_pretrained(
        base_model_name,
        num_labels=len(LABEL_LIST),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )

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

    logger.info("Tokenizing datasets...")
    tokenized_train = train_data.map(tokenize_and_align_labels, batched=True)
    tokenized_eval = eval_data.map(tokenize_and_align_labels, batched=True)

    def compute_metrics(p):
        predictions, labels = p
        predictions = np.argmax(predictions, axis=2)

        true_predictions = [
            [LABEL_LIST[p_idx] for (p_idx, l_idx) in zip(prediction, label) if l_idx != -100]
            for prediction, label in zip(predictions, labels)
        ]
        true_labels = [
            [LABEL_LIST[l_idx] for (p_idx, l_idx) in zip(prediction, label) if l_idx != -100]
            for prediction, label in zip(predictions, labels)
        ]

        try:
            return {
                "precision": float(precision_score(true_labels, true_predictions, zero_division=0)),
                "recall": float(recall_score(true_labels, true_predictions, zero_division=0)),
                "f1": float(f1_score(true_labels, true_predictions, zero_division=0)),
                "accuracy": float(accuracy_score(true_labels, true_predictions)),
            }
        except Exception as e:
            logger.warning(f"Error computing seqeval metrics: {e}")
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "accuracy": 0.0}

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        learning_rate=learning_rate,
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="no",
        report_to="none",
    )

    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    with mlflow.start_run() as run:
        run_id = run.info.run_id
        logger.info(f"== MLflow Run Started (Run ID: {run_id}) ==")

        # 1. Log Hyperparameters
        params = {
            "base_model": base_model_name,
            "num_epochs": num_epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "train_samples": len(train_data),
            "eval_samples": len(eval_data),
            "registered_model_name": registered_model_name,
        }
        mlflow.log_params(params)
        logger.info(f"Logged parameters: {params}")

        # 2. Train Model
        logger.info("Starting PyTorch/Transformers training loop...")
        train_result = trainer.train()

        # 3. Evaluate Model
        logger.info("Evaluating trained model...")
        eval_metrics = trainer.evaluate()
        logger.info(f"Evaluation metrics: {eval_metrics}")

        # 4. Log Metrics to MLflow
        train_loss = getattr(train_result, "training_loss", None)
        if train_loss is None:
            train_loss = train_result.metrics.get("train_loss", 0.0)

        metrics_to_log = {
            "train_loss": float(train_loss),
            "eval_loss": float(eval_metrics.get("eval_loss", 0.0)),
            "eval_f1": float(eval_metrics.get("eval_f1", 0.0)),
            "eval_precision": float(eval_metrics.get("eval_precision", 0.0)),
            "eval_recall": float(eval_metrics.get("eval_recall", 0.0)),
            "eval_accuracy": float(eval_metrics.get("eval_accuracy", 0.0)),
        }
        mlflow.log_metrics(metrics_to_log)
        logger.info(f"Logged metrics to MLflow: {metrics_to_log}")

        # 5. Save Model Locally
        logger.info(f"Saving model artifacts locally to {output_dir}...")
        trainer.save_model(output_dir)
        tokenizer.save_pretrained(output_dir)

        # 6. Log & Register Model in MLflow
        logger.info(f"Registering model in MLflow under '{registered_model_name}'...")
        try:
            ner_pipe = pipeline(
                "token-classification",
                model=trainer.model,
                tokenizer=tokenizer,
                aggregation_strategy="simple",
            )
            model_to_log = ner_pipe
        except Exception as pipe_err:
            logger.warning(f"Could not wrap model into pipeline: {pipe_err}. Falling back to dict.")
            model_to_log = {"model": trainer.model, "tokenizer": tokenizer}

        mlflow.transformers.log_model(
            transformers_model=model_to_log,
            artifact_path="model",
            registered_model_name=registered_model_name,
        )
        logger.info(f"Model successfully logged and registered as '{registered_model_name}' in MLflow.")

        model_uri = f"runs:/{run_id}/model"
        return {
            "run_id": run_id,
            "model_uri": model_uri,
            "registered_model_name": registered_model_name,
            "metrics": {**metrics_to_log, **train_result.metrics, **eval_metrics},
        }
