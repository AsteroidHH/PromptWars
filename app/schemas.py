from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class TriageCategory(str, Enum):
    RED = "RED - Immediate (Life-threatening)"
    YELLOW = "YELLOW - Urgent (Serious but not immediately fatal)"
    GREEN = "GREEN - Minor (Walking wounded / non-urgent)"
    BLACK = "BLACK - Expectant (Deceased or unsalvageable)"

class BystanderActionPlan(BaseModel):
    immediate_steps: List[str] = Field(
        description="Numbered, plain-language first-aid instructions for non-medical bystanders on the scene (e.g., direct pressure, recovery position)."
    )
    critical_warnings: List[str] = Field(
        description="Explicit actions to avoid (e.g., do not move spine/neck, do not give water to unconscious patient)."
    )

class SceneHazards(BaseModel):
    active_hazards: List[str] = Field(
        description="Environmental dangers identified from the scene (e.g., live electrical wires, heavy traffic, fire, chemical spill)."
    )
    bystander_safety_advice: str = Field(
        description="Guidance to keep the reporter and bystanders safe before medical help arrives."
    )

class ClinicalSummary(BaseModel):
    patient_status: str = Field(
        description="Observed state of consciousness, breathing regularity, and active bleeding."
    )
    suspected_injuries: List[str] = Field(
        description="List of probable trauma or medical conditions identified from the input."
    )
    recommended_trauma_level: str = Field(
        description="Suggested hospital care capability needed (e.g., Level 1 Trauma Center, Burn Unit, General ER)."
    )

class SanjeevaniTriageResponse(BaseModel):
    triage_tag: TriageCategory = Field(
        description="Standard triage classification based on patient severity."
    )
    extracted_location: Optional[str] = Field(
        default=None,
        description="Any landmarks, street names, or location details parsed from the messy input."
    )
    verification_confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score (0.0 to 1.0) evaluating clarity and consistency of the input data."
    )
    verification_notes: str = Field(
        description="Any conflicting information, missing critical details, or ambiguity flagged by the model."
    )
    bystander_actions: BystanderActionPlan
    scene_hazards: SceneHazards
    clinical_summary: ClinicalSummary
    google_maps_emergency_url: Optional[str] = Field(
        default=None,
        description="Generated Google Maps URL for nearest trauma center/hospital based on extracted location."
    )

