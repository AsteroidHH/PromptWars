import os
from google import genai
from google.genai import types
from .schemas import SanjeevaniTriageResponse

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
    
    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=contents,
        config=config
    )
    
    return response.parsed
