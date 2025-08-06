from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

router = APIRouter(tags=["ML Suggestions"])

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

class PromptRequest(BaseModel):
    topic: str
@router.post("/suggest")
async def generate_suggestions(request: PromptRequest):
    # Improved prompt
    prompt = f"What are the topics and resources needed to learn {request.topic}? Provide a list."

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=128,
        temperature=0.7,
        do_sample=True,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"suggestion": response.strip()}

