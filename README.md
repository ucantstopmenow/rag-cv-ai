# 🤖 CV Compatibility Analyzer

> API inteligente com RAG + Gemini para comparar seu currículo com requisitos de vagas — ideal para portfólios ou aplicações de carreira.

---

## 📌 Descrição

Este projeto é uma API backend desenvolvida com **FastAPI**, **LangChain** e **Gemini 1.5 Pro**. Utiliza **RAG (Retrieval-Augmented Generation)** para comparar o conteúdo de um currículo com os requisitos de uma vaga de emprego.

A IA responde com uma análise estruturada em JSON, indicando se cada requisito é atendido ou não, junto com uma justificativa.

---

## 🧠 Tecnologias Principais

- 🧪 **FastAPI** — Framework leve e rápido para APIs
- 🧠 **LangChain + FAISS** — Recuperação semântica do conteúdo do currículo
- 🌐 **Google Gemini 1.5 Pro** — Modelo LLM da Google via SDK oficial
- 📦 **Docker + Railway** — Deploy automatizado e escalável
- 🧩 **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`

---

## 🗂️ Estrutura do Projeto

```
├── app/
│   ├── main.py         # FastAPI app + endpoints
│   ├── chains.py       # Lógica de RAG + análise
│   ├── loader.py       # Indexação de currículos (PDFs)
│   ├── schema.py       # Pydantic models
├── knowledge_base/     # Currículos em PDF (fixos)
├── vectorstore/        # Índice FAISS persistido
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## 🚀 Como executar localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/cv-analyzer-api.git
   cd cv-analyzer-api
   ```

2. **Crie o arquivo `.env`** com sua chave Gemini:
   ```env
   GEMINI_API_KEY=your-google-api-key-here
   ```

3. **Execute via Docker:**
   ```bash
   docker build -t cv-analyzer .
   docker run -p 8000:8000 --env-file .env cv-analyzer
   ```

4. **Acesse a API:**
   - Documentação Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

5. **Exemplo de requisição:**
   ```json
   {
     "requirements": "Experiência com Python\nConhecimento em Docker"
   }
   ```

---

## 🌐 Deploy na Railway (automático)

1. Suba o projeto para o GitHub
2. Crie um projeto na Railway
3. Selecione “Deploy from GitHub”
4. Configure a variável de ambiente `GEMINI_API_KEY`
5. Após o deploy, use o endpoint público no seu frontend

---

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.


