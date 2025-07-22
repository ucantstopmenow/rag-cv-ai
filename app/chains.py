from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.loader import get_vectorstore
from app.schema import JobInput, AnalysisItem, AnalysisResponse

import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def build_prompt(requirements: list[str]) -> str:
    bullet_list = "\n".join(f"- {req}" for req in requirements)
    return (
        "Você é um assistente de recrutamento. Compare o currículo com os requisitos a seguir:\n\n"
        f"{bullet_list}\n\n"
        "Para cada requisito, indique se ele é atendido (✅ ou ❌) e explique em até 20 palavras.\n"
        "Responda em JSON estruturado como:\n"
        '{ "analysis": [{"requirement": "...", "isMet": true, "justification": "..."}] }'
    )

def analyze_job_requirements(input_data: JobInput) -> AnalysisResponse:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY não foi definida.")

    vectorstore = get_vectorstore()

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
    )

    prompt_template = PromptTemplate.from_template("{context}\n\n{question}")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt_template}
    )

    requirements_list = [r.strip() for r in input_data.requirements.split("\n") if r.strip()]
    prompt = build_prompt(requirements_list)

    result = qa_chain.run(prompt)

    try:
        parsed = eval(result)  # ❗ Substituir por `json.loads()` se a IA responder JSON puro
        return AnalysisResponse(analysis=[
            AnalysisItem(**item) for item in parsed.get("analysis", [])
        ])
    except Exception:
        # Fallback se não vier em JSON
        return AnalysisResponse(analysis=[
            AnalysisItem(requirement=req, isMet="✅" in result, justification=result[:80])
            for req in requirements_list
        ])
