# Usando a imagem do Python slim
FROM python:3.11-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Não gerar arquivos .pyc e não usar buffer no stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar os requisitos
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta
EXPOSE 5000

# Comando para rodar a aplicação com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
