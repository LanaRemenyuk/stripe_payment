FROM python:3.11

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

ENV PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]