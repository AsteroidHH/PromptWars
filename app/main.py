from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
import urllib.parse
import os

from .schemas import SanjeevaniTriageResponse
from .gemini_client import analyze_emergency

app = FastAPI(
    title="Sanjeevani Triage API",
    description="Emergency triage bridge converting real-world inputs into structured life-saving actions.",
    version="1.0.0"
)

# Ensure static directory exists
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("app/static/index.html")

@app.post("/triage", response_model=SanjeevaniTriageResponse)
async def triage_endpoint(
    text_input: str = Form(..., description="Text description of the emergency"),
    media: Optional[UploadFile] = File(None, description="Optional image or audio file of the scene")
):
    """
    Submit an emergency situation for immediate triage.
    Accepts text and an optional media file (image/audio).
    Returns a verified, structured action plan with Google Maps routing.
    """
    media_bytes = None
    media_mime_type = None
    
    if media and media.filename:
        media_bytes = await media.read()
        media_mime_type = media.content_type
        
        # Basic validation for allowed mime types
        allowed_types = ["image/jpeg", "image/png", "audio/mpeg", "audio/wav", "audio/ogg", "audio/webm", "video/webm"]
        if media_mime_type not in allowed_types and not media_mime_type.startswith("audio/") and not media_mime_type.startswith("image/"):
             # Fallback just in case browser uses slightly different mime types (like audio/webm;codecs=opus)
             if not any(media_mime_type.startswith(prefix) for prefix in ["audio/", "image/"]):
                raise HTTPException(status_code=400, detail=f"Unsupported media type: {media_mime_type}. Please upload audio or image.")

    try:
        # Call the Gemini client
        triage_result = analyze_emergency(
            text_input=text_input,
            media_bytes=media_bytes,
            media_mime_type=media_mime_type
        )
        
        # Enhance response with Google Maps routing
        if triage_result.extracted_location:
            encoded_location = urllib.parse.quote(triage_result.extracted_location)
            triage_result.google_maps_emergency_url = f"https://www.google.com/maps/search/?api=1&query=emergency+trauma+center+hospital+near+{encoded_location}"
        else:
            triage_result.google_maps_emergency_url = "https://www.google.com/maps/search/?api=1&query=nearest+emergency+trauma+center+hospital"
            
        return triage_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage processing failed: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Sanjeevani Triage"}
