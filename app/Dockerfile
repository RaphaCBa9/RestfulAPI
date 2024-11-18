# Use a imagem oficial do Python como base
FROM ubuntu:22.04
FROM python:3.11-slim

# Defina o diretório de trabalho na imagem
WORKDIR /app

# Copie os arquivos de requisitos para a imagem
COPY requirements.txt .

# Instale as dependências
RUN apt-get update
RUN apt-get install net-tools -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para a imagem
COPY . /app

# Exponha a porta que a aplicação usará
EXPOSE 8000
# uvicorn app:app --host "localhost" --port 8000 --reload
CMD ["uvicorn", "app:app", "--host", "localhost", "--port", "8000", "--reload"]