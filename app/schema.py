from pydantic import BaseModel
from typing import List

class JobInput(BaseModel):
    requirements: str  # Requisitos da vaga em texto

class AnalysisItem(BaseModel):
    requirement: str
    isMet: bool
    justification: str

class AnalysisResponse(BaseModel):
    analysis: List[AnalysisItem]
