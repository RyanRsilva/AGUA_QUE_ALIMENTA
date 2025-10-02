# Usar imagem oficial Python slim
FROM python:3.11-slim

# Diretório de trabalho no container
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código para o container
COPY . .

# Expor portas para backend e dashboard
EXPOSE 8000 8501

# Comando padrão para rodar backend e dashboard em background e main.py
# Usaremos um script para rodar os 3 processos simultaneamente
CMD ["./start_all.sh"]
