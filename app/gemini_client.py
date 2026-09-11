import os
import time
import logging
from google import genai
from google.genai import types
from google.genai import errors
from .schemas import SanjeevaniTriageResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Gemini client
# The client automatically picks up GEMINI_API_KEY from the environment
client = genai.Client()

def analyze_emergency(
    text_input: str,
    media_bytes: bytes = None,
    media_mime_type: str = None
) -> SanjeevaniTriageResponse:
    """
    Analyzes emergency inputs (text + optional media) using Gemini
    and returns a structured SanjeevaniTriageResponse.
    Includes multi-model fallback and retry logic for high demand (503s).
    """
    
    # Base prompt to instruct the model on its persona and task
    system_prompt = (
        "You are 'Sanjeevani', an expert emergency triage AI. "
        "Your job is to analyze messy real-world inputs from bystanders, "
        "including text descriptions, audio transcripts, or photos. "
        "Assess the situation, identify the triage category, locate hazards, "
        "and provide actionable, life-saving advice for non-medical bystanders. "
        "Be extremely accurate and prioritize safety."
    )
    
    contents = [
        types.Part.from_text(text=system_prompt),
        types.Part.from_text(text=f"Emergency Input: {text_input}")
    ]
    
    if media_bytes and media_mime_type:
        contents.append(
            types.Part.from_bytes(data=media_bytes, mime_type=media_mime_type)
        )
        
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=SanjeevaniTriageResponse,
        temperature=0.2, # Low temperature for more deterministic triage
    )
    
    # Fallback list of modern models to handle high demand
    models_to_try = [
        "gemini-3.7-flash",        # Primary fast multimodal model
        "gemini-3.5-flash-lite",   # Fallback 1: High-throughput lite model
        "gemini-3.1-pro-preview"   # Fallback 2: Pro model
    ]
    
    last_error = None
    
    for i, model in enumerate(models_to_try):
        try:
            logger.info(f"Attempting inference with model: {model}")
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
            return response.parsed
            
        except errors.APIError as e:
            last_error = e
            # Log the error and backoff before trying the next model
            logger.warning(f"Model {model} failed with APIError: {e.message}. HTTP Code: {e.code}")
            if i < len(models_to_try) - 1:
                logger.info(f"Retrying in 2 seconds with next fallback model...")
                time.sleep(2)
            else:
                logger.error("All fallback models exhausted.")
                
        except Exception as e:
            last_error = e
            logger.warning(f"Model {model} encountered an unexpected error: {str(e)}")
            if i < len(models_to_try) - 1:
                logger.info(f"Retrying in 2 seconds with next fallback model...")
                time.sleep(2)
            else:
                logger.error("All fallback models exhausted.")
                
    # If we exhaust all models, raise the last exception
    raise last_error
