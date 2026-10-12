from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

WHAT_IF_DISCLAIMER = (
    "Disclaimer: Scenario simulations are mathematical projections based on historical learning curves, "
    "market demand benchmarks, and pacing models. These outcomes are educational estimates and do NOT "
    "guarantee job offers, placement timelines, or starting salaries."
)

class ScenarioParameters(BaseModel):
    name: str = "Scenario A"
    daily_hours: float = Field(1.5, ge=0.5, le=12.0)
    additional_skills: List[str] = Field(default_factory=list)  # e.g. ["SQL", "FastAPI"]
    projects_to_complete: int = Field(1, ge=0, le=10)
    months_until_placement: int = Field(6, ge=1, le=48)
    target_role: Optional[str] = None


class ScenarioResult(BaseModel):
    name: str
    projected_skill_coverage_pct: float
    projected_readiness_pct: float
    total_study_hours: float
    estimated_weekly_pace: float
    milestone_timeline: List[Dict[str, Any]]
    key_advantages: List[str]
    tradeoffs_and_risks: List[str]


class WhatIfSimulateRequest(BaseModel):
    scenario_a: ScenarioParameters
    scenario_b: Optional[ScenarioParameters] = None


class WhatIfSimulateResponse(BaseModel):
    disclaimer: str
    scenario_a_result: ScenarioResult
    scenario_b_result: Optional[ScenarioResult] = None
    comparative_summary: str
