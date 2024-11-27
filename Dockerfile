# Usamos uma imagem base do Python
FROM python:3.11.0

# Definimos o diretório de trabalho
WORKDIR /app

# Copiamos o arquivo de requisitos
COPY requirements.txt .

# Instalamos as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos o restante do código-fonte
COPY . .

# Expondo a porta que o Django irá usar
EXPOSE 8000

# Definimos o comando para iniciar a aplicação
CMD ["python", "meu_projeto/manage.py", "runserver", "0.0.0.0:8000"]