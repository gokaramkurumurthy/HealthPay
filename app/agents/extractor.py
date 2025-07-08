import os
import logging
from itertools import cycle
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

def extract(doc_type: str, text: str) -> dict:
    prompt = f"""
Extract structured data from the following {doc_type} content.
Return as JSON with relevant fields.

Document type: {doc_type}
Text:
{text[:1500]}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return eval(response.text.strip())
    except Exception as e:
        logger.warning(f"Error extracting content: {e}")
        try:
            configure_genai()
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            return eval(response.text.strip())
        except Exception as retry_error:
            logger.error(f"Fallback failed: {retry_error}")
            return {"type": doc_type, "content": text[:500]}
