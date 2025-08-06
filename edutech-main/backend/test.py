from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load model and tokenizer
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Set device (use GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Create a prompt
course_keyword = "java full stack"
prompt = f"Give learning suggestions for a course on: {course_keyword}"

# Tokenize input
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Generate output
outputs = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=100,
    temperature=0.7,
    do_sample=True
)

# Decode and print result
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Suggested Content:", response.strip())
