import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

def train_lm_model(data_file, output_dir):
    # Load and tokenize data
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    train_data = TextDataset(tokenizer=tokenizer, file_path=data_file, block_size=128)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Define model
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_data,
    )

    # Train the model
    trainer.train()

    # Save the trained model and tokenizer
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

def load_lm_model(model_dir):
    # Load the trained model and tokenizer
    model = GPT2LMHeadModel.from_pretrained(model_dir)
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    return model, tokenizer

def generate_response(model, tokenizer, prompt, max_length=50):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    # Train the language model
    train_lm_model(data_file="country_etiquette_data.csv", output_dir="./lm_model")

    # Load the trained model
    model, tokenizer = load_lm_model(model_dir="./lm_model")

    # Example usage: Generate response to a prompt
    prompt = "What is the cultural etiquette for greeting in Argentina?"
    response = generate_response(model, tokenizer, prompt)
    print("Response:", response)
