ARG PYTHON_IMAGE=python:3.11.1-slim

FROM ${PYTHON_IMAGE} AS builder

WORKDIR /app
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv "$POETRY_VENV" \
	&& "$POETRY_VENV"/bin/pip install -U pip setuptools \
	&& "$POETRY_VENV"/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . /app

ENTRYPOINT ["python", "bin/evaluate.py"]
CMD [""]
