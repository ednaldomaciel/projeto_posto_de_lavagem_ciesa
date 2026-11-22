# Imagem base oficial Python leve
FROM python:3.11-slim

# Variáveis de ambiente para Python em contêiner
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

# Diretório de trabalho
WORKDIR /app

# Instalação de dependências de sistema para PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalação das dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Cópia do código-fonte do projeto
COPY . /app/

# Coleta de arquivos estáticos via WhiteNoise
RUN python manage.py collectstatic --noinput

# Porta exposta padrão
EXPOSE 8000

# Execução automática de migrações e inicialização com Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn --chdir backend config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
