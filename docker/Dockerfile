FROM python:3.12-slim

LABEL org.opencontainers.image.title="promptsentinel"
LABEL org.opencontainers.image.description="LLM prompt security scanner — PII, secrets, injection, jailbreaks"
LABEL org.opencontainers.image.source="https://github.com/sandeepmothukuri/PromptSentinel"
LABEL org.opencontainers.image.licenses="MIT"
LABEL maintainer="Sandeep Mothukuri <sandeep.mothukuris@gmail.com>"

WORKDIR /app

COPY pyproject.toml .
COPY promptsentinel/ ./promptsentinel/
COPY api/ ./api/
COPY integrations/ ./integrations/
COPY models/ ./models/

RUN pip install --no-cache-dir -e ".[api]"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
