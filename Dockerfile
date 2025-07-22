# ---- BASE ----
FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório da aplicação
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Porta usada pela API
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
