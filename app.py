import httpx
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from typing import Dict
import uvicorn
from symspellpy import SymSpell, Verbosity
import os
import json
from fastapi.staticfiles import StaticFiles
import requests
import uuid
from fastapi.responses import HTMLResponse

API_KEY = "mu7S5LaQrgyizTY6C1gr1oVR9yVeVKrL"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL_NAME = "mistral-medium"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary("frequency_dictionary_en.txt", term_index=0, count_index=1)

DB_FILE = "history.json"

def initialize_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

initialize_db()

def save_to_history(id_text: str, text: str, mode: str, corrected_text: str):
    record = {
        "id_text": id_text,
        "original_text": text,
        "mode": mode,
        "corrected_text": corrected_text
    }
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    data.append(record)
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

async def call_mistral(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You're a helpful text assistant. Could you please help me to complete the text?"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(MISTRAL_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

def correct_grammar(text: str) -> str:
    url = "https://api.languagetool.org/v2/check"
    payload = {"text": text, "language": "en-US"}
    response = requests.post(url, data=payload)
    data = response.json()
    matches = sorted(data["matches"], key=lambda x: x["offset"], reverse=True)
    for match in matches:
        if match["replacements"]:
            replacement = match["replacements"][0]["value"]
            start = match["offset"]
            end = start + match["length"]
            text = text[:start] + replacement + text[end:]
    return text

def correct_spelling(text: str) -> str:
    corrected_words = []
    for word in text.split():
        suggestions = sym_spell.lookup(word.lower(), Verbosity.CLOSEST, max_edit_distance=2)
        if suggestions:
            corrected_word = suggestions[0].term
            if word[0].isupper():
                corrected_word = corrected_word.capitalize()
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)
    return " ".join(corrected_words)

async def autocomplete_text(text: str) -> str:
    prompt = f"Continue this sentence:\n\n{text}"
    return await call_mistral(prompt)

@app.post("/process_text")
async def process_text(
    text: str = Form(...),
    mode: str = Form(...)
) -> Dict[str, str]:
    result = {}
    id_text = str(uuid.uuid4())  

    if mode == "grammar":
        corrected = correct_grammar(text)
        result["grammar_corrected"] = corrected
        save_to_history(id_text, text, mode, corrected)
    elif mode == "spelling":
        corrected = correct_spelling(text)
        result["spelling_corrected"] = corrected
        save_to_history(id_text, text, mode, corrected)
    elif mode == "completion":
        corrected = await autocomplete_text(text)
        result["auto_completed"] = corrected
        save_to_history(id_text, text, mode, corrected)
    else:
        return {"error": "Invalid mode selected."}

    return result

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_text_by_id")
async def get_text_by_id(id_text: str = Form(...)):
    if not os.path.exists(DB_FILE):
        return {"error": "Database not found."}

    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    for record in data:
        if record.get("id_text") == id_text:
            return {"original_text": record.get("original_text"), "corrected_text": record.get("corrected_text")}

    return {"error": "Record not found."}