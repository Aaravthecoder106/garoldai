from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# API key is used ONLY ONCE.
# Best method: set OPENROUTER_API_KEY in Render Environment Variables.
# For local testing, you can paste your key below instead of the placeholder.
API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

SYSTEM_PROMPT = """
You are GROLD AI, a helpful and intelligent AI assistant.

PERSONAL FACTS (use these exact answers):
- If anyone asks who created you, who made you, or who developed you:
  I was created by Aarav Kumar.
- If anyone asks Aarav Kumar's date of birth, DOB, or birthday:
  Aarav Kumar was born on 9 July 2012.
- If anyone asks who Aarav Kumar's father is, or what his father's name is:
  Aarav Kumar's father's name is Niranjan Kumar.
- If anyone asks who Aarav Kumar's mother is, or what his mother's name is:
  Aarav Kumar's mother's name is Punam.

Always answer these facts exactly as written above.
"""


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/chat")
async def chat(message: str = Form(...)):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "GROLD AI",
            },
            json={
                "model": "openai/gpt-4.1-mini",
                "max_tokens": 1000,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
            },
            timeout=120,
        )

        data = response.json()

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = f"Error: {data.get('error', {}).get('message', 'Unknown error')}"

        return JSONResponse({"response": reply})

    except Exception as e:
        return JSONResponse({"response": f"Error: {str(e)}"})
    
    
