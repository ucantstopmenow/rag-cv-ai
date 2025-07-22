import os
import json
from dotenv import load_dotenv
from app.loader import get_vectorstore
from app.schema import JobInput, AnalysisItem, AnalysisResponse

import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def build_prompt(requirements: str, curriculum_chunks: list[str]) -> str:
    curriculum_text = "\n".join(curriculum_chunks)

    return f"""
Você é um assistente de recrutamento. Compare o currículo abaixo com os requisitos da vaga.

Contexto (currículo):
{curriculum_text}

Requisitos da vaga:
{requirements}

Para cada requisito, indique:
- Se ele é atendido (✅ ou ❌)
- Explique em até 20 palavras o motivo

Responda no seguinte formato JSON:
{{ "analysis": [ {{ "requirement": "...", "isMet": true, "justification": "..." }} ] }}
"""

def analyze_job_requirements(input_data: JobInput) -> AnalysisResponse:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY não foi definida.")

    # 1. Inicializar Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    # 2. Recuperar chunks relevantes do currículo
    retriever = get_vectorstore().as_retriever()
    docs = retriever.get_relevant_documents(input_data.requirements)
    curriculum_chunks = [doc.page_content for doc in docs]

    # 3. Montar o prompt manualmente
    prompt = build_prompt(input_data.requirements, curriculum_chunks)

    # 4. Enviar para Gemini
    response = model.generate_content(prompt)
    output = response.text.strip()

    # 5. Extrair JSON da resposta
    try:
        start = output.index("{")
        end = output.rindex("}") + 1
        json_data = json.loads(output[start:end])
        items = [AnalysisItem(**item) for item in json_data.get("analysis", [])]
    except Exception as e:
        # fallback simples
        reqs = [r.strip() for r in input_data.requirements.split("\n") if r.strip()]
        items = [
            AnalysisItem(
                requirement=req,
                isMet=("✅" in output),
                justification=output[:80]
            )
            for req in reqs
        ]

    return AnalysisResponse(analysis=items)
