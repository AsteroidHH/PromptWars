import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

os.environ["GEMINI_API_KEY"] = "dummy_test_key"

from app.main import app
from app.schemas import (
    SanjeevaniTriageResponse, 
    TriageCategory, 
    BystanderActionPlan, 
    SceneHazards, 
    ClinicalSummary
)

client = TestClient(app)

def mock_triage_response():
    return SanjeevaniTriageResponse(
        triage_tag=TriageCategory.RED,
        extracted_location="Main St and 4th Ave",
        verification_confidence=0.95,
        verification_notes="Clear visual of bleeding.",
        bystander_actions=BystanderActionPlan(
            immediate_steps=["Apply direct pressure to the wound."],
            critical_warnings=["Do not move the patient unless in immediate danger."]
        ),
        scene_hazards=SceneHazards(
            active_hazards=["Traffic"],
            bystander_safety_advice="Stay on the sidewalk."
        ),
        clinical_summary=ClinicalSummary(
            patient_status="Conscious but bleeding heavily.",
            suspected_injuries=["Laceration on right leg."],
            recommended_trauma_level="Level 1 Trauma Center"
        ),
        google_maps_emergency_url="https://www.google.com/maps/search/?api=1&query=emergency+trauma+center+hospital+near+Main%20St%20and%204th%20Ave"
    )

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "Sanjeevani Triage"}

def test_static_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Sanjeevani | Emergency Triage AI" in response.text


@patch("app.main.analyze_emergency")
def test_triage_endpoint_text_only(mock_analyze):
    mock_analyze.return_value = mock_triage_response()
    
    response = client.post(
        "/triage",
        data={"text_input": "Car crash at Main St and 4th Ave. Driver is bleeding heavily."}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["triage_tag"] == "RED - Immediate (Life-threatening)"
    assert data["extracted_location"] == "Main St and 4th Ave"
    assert "bystander_actions" in data
    
    mock_analyze.assert_called_once_with(
        text_input="Car crash at Main St and 4th Ave. Driver is bleeding heavily.",
        media_bytes=None,
        media_mime_type=None
    )

@patch("app.main.analyze_emergency")
def test_triage_endpoint_with_invalid_media(mock_analyze):
    response = client.post(
        "/triage",
        data={"text_input": "Help!"},
        files={"media": ("test.txt", b"not an image", "text/plain")}
    )
    
    assert response.status_code == 400
    assert "Unsupported media type" in response.json()["detail"]
    mock_analyze.assert_not_called()
