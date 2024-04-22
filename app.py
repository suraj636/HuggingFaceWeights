from fastapi import FastAPI, Form, HTTPException
from transformers import pipeline

app = FastAPI()

# Function to load models and tokenizers
def load_model(lang):
  model_name = model_names.get(lang)
  if not model_name:
    raise HTTPException(status_code=400, detail=f"Language '{lang}' not supported")  
  return pipeline("translation", model=model_name)

# Supported languages and models
model_names = {
    "hi": "Helsinki-NLP/opus-mt-en-hi",
    "ar": "Helsinki-NLP/opus-mt-en-ar",
    "ur": "Helsinki-NLP/opus-mt-en-ur",
    "tl": "Helsinki-NLP/opus-mt-en-tl"
}

# Translate route
@app.post("/translate/")
async def translate_text_api(text: str = Form(...), language: str = Form(...)):
  # Validate input
  if not text:
    raise HTTPException(status_code=400, detail="Text input cannot be empty")
  if len(text) > 512:
    raise HTTPException(status_code=400, detail="Text input is too long, maximum length is 512 characters")

  try:
    # Load model and tokenizer using dependency injection
    translator = load_model(language)
    translated_text = translator(text)[0]["translation_text"]
    return {"translated_text": translated_text}
  except Exception as e:
    logging.exception("Translation failed")
    raise HTTPException(status_code=500, detail="Translation failed")

# Root route
@app.get("/")
async def root():
  return {"message": "Welcome to the translation API for Indian Languages"}
