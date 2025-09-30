# Usar imagem base Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY . .

# Criar diretório para banco
RUN mkdir -p banco

# Expor porta
EXPOSE 8000

# Comando para executar
CMD ["python", "main/main.py"]
