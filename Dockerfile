FROM python:3.11-slim-bullseye

WORKDIR /usr/app

EXPOSE 8000

RUN apt-get update -y

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY . .

RUN uv sync --frozen --no-dev

ENV PATH="/usr/app/.venv/bin:$PATH"

CMD ["gunicorn", "app:server", "--timeout", "90", "--log-level", "DEBUG", "--log-file", "-"]
