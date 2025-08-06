from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

router = APIRouter(tags=["TinyLLaMA"])

# Load model & tokenizer once at startup
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

class SuggestionRequest(BaseModel):
    topic: str
    max_new_tokens: int = 128
    temperature: float = 0.7

@router.post("/mlmod")
async def generate_course_suggestion(request: SuggestionRequest):
    try:
        #topic = request.topic
        # Chat-style prompt
        chat_prompt = [
            {"role": "system", "content": "You are a helpful assistant that suggests learning paths for any topic."},
            {"role": "user", "content": f"Suggest learning topics and resources for becoming a {request.topic}."}
        ]

        inputs = tokenizer.apply_chat_template(
            chat_prompt,
            return_tensors="pt"
        ).to(device)

        outputs = model.generate(
            input_ids=inputs,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

        full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = full_output.split(chat_prompt[-1]["content"])[-1].strip()
        return {"suggestion": response}

    except Exception as e:
        return {"error": str(e)}
