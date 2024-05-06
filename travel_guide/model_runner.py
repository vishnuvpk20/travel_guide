import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

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


# Load the trained model
model, tokenizer = load_lm_model(model_dir="./lm_model")

# Example usage: Generate response to a prompt
prompt = "what is the gift culture in france?"
response = generate_response(model, tokenizer, prompt)
print("Response:", response)
