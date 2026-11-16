# syntax=docker/dockerfile:1

# Main image build for this repo. The devcontainer does not use this file;
# it boots a published image. Build with:
#   docker build --secret id=MY_TOKEN,env=MY_TOKEN -t swe-agent .
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/swe-agent

# Repo source must be present before private deps and the package install.
COPY . .

RUN --mount=type=secret,id=MY_TOKEN,env=MY_TOKEN,required=true \
    ./scripts/install-private-deps.sh

RUN pip install --no-cache-dir .

CMD ["sweagent", "--help"]
