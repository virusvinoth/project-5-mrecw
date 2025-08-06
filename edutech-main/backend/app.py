from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Load your fine-tuned model and tokenizer
model_path = "./finetuned-llm"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Create text generation pipeline
generator = pipeline("text-generation", 
                     model=model, tokenizer=tokenizer)

# Generate output
prompt = "Explain artificial intelligence:"
result = generator(prompt, max_length=100, 
                   do_sample=True)[0]['generated_text']
print("Generated Response:\n", result)
