from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from typing import Dict
import uvicorn
import requests
from symspellpy import SymSpell, Verbosity
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary("frequency_dictionary_en.txt", term_index=0, count_index=1)

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

def autocomplete_text(text: str) -> str:
    return text + " (auto-completed)"  # 示例占位，可接 Hugging Face API

@app.post("/process_text")
async def process_text(
    text: str = Form(...),
    mode: str = Form(...)
) -> Dict[str, str]:
    result = {}

    if mode == "grammar":
        result["grammar_corrected"] = correct_grammar(text)
    elif mode == "spelling":
        result["spelling_corrected"] = correct_spelling(text)
    elif mode == "completion":
        result["auto_completed"] = autocomplete_text(text)

    return result

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
