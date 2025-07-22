import os
from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

KB_PATH = Path("knowledge_base")
INDEX_PATH = Path("vectorstore/index.faiss")

def load_documents():
    docs = []
    for file in KB_PATH.glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        docs.extend(loader.load())
    return docs

def get_vectorstore():
    if INDEX_PATH.exists():
        return FAISS.load_local("vectorstore", HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), allow_dangerous_deserialization=True)

    print("🔄 Indexando documentos...")
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    vectorstore.save_local("vectorstore")
    return vectorstore
