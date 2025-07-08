import os
import logging
from itertools import cycle
from fastapi import HTTPException
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEYS = os.getenv("GOOGLE_API_KEYS", "").split(",")
API_KEYS = [key.strip() for key in API_KEYS if key.strip()]
API_KEY_CYCLE = cycle(API_KEYS)

def configure_genai(api_key=None):
    genai.configure(api_key=api_key or next(API_KEY_CYCLE))

configure_genai()

def classify(text: str, filename: str) -> str:
    try:
        if not text.strip():
            raise HTTPException(status_code=422, detail="No text could be extracted from the PDF")

        prompt = f"""
You are a medical document classifier.
Given the content of a PDF document below, classify it as either:
- bill
- discharge_summary
- id_proof

Text:
{text[:1500]}
Filename: {filename}

Respond with only the type.
"""
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip().lower()
    except Exception as e:
        logger.warning(f"Gemini API error or quota exceeded: {e}")
        logger.warning("Using fallback classification based on keywords")
        lowered = filename.lower()
        if "bill" in lowered:
            return "bill"
        elif "discharge" in lowered:
            return "discharge_summary"
        elif "id" in lowered or "aadhar" in lowered or "pan" in lowered:
            return "id_proof"
        return "unknown"
