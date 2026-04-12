FROM python:3.11-slim

ARG COVFEE_PIP_SPEC=git+https://github.com/josedvq/covfee.git

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir "${COVFEE_PIP_SPEC}"

WORKDIR /workspace

COPY docker/entrypoint.sh /usr/local/bin/covfee-entrypoint
RUN chmod +x /usr/local/bin/covfee-entrypoint

ENTRYPOINT ["covfee-entrypoint"]
