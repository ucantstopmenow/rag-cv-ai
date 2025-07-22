from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schema import JobInput, AnalysisResponse
from app.chains import analyze_job_requirements
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Henrique CV Analyzer",
    description="Backend RAG para análise de compatibilidade com vaga",
    version="1.0.0",
    debug=True
)

# CORS para frontend estático (ex: seu portfólio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {"status": "API Currículo AI está funcionando!"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(input_data: JobInput):
    try:
        result = analyze_job_requirements(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
