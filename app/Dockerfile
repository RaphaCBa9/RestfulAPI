# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Defina o diretório de trabalho na imagem
WORKDIR /app

# Copie os arquivos de requisitos para a imagem
COPY requirements.txt .

# Atualize os pacotes e instale dependências
RUN apt-get update && apt-get install -y net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Atualize o pip e instale as dependências do Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para a imagem
COPY . /app

# Exponha a porta usada pela aplicação
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["fastapi", "run", "app/app.py", "--host", "0.0.0.0", "--port", "8000"]
