# Imagem base do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para o container
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o script Python para o diretório de trabalho no container
COPY extrator_noticias_g1_v2.py .

# Comando padrão ao rodar o container
# Exemplo: Executar o arquivo Python 'extrator_noticias_g1_v2.py'
CMD ["python", "extrator_noticias_g1_v2.py"]
