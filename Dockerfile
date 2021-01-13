ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}-slim

WORKDIR /vulnpy
COPY . .

RUN apt-get update && apt-get install -y build-essential autoconf
RUN pip install -U contrast-agent
RUN pip install -e .[all]

ENV PORT="3010"
ENV FRAMEWORK="wsgi"
ENV HOST="0.0.0.0"
ENV VULNPY_USE_CONTRAST="true"

ENTRYPOINT make ${FRAMEWORK}
