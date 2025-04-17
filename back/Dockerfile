FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

# Poetry
ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' 


RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

ENV FLASK_APP=run.py
EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
