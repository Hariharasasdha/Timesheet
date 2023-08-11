FROM python:3-slim-bullseye

RUN apt-get update && apt-get install -y git

RUN useradd -ms /bin/bash api
USER api
WORKDIR /home/api

ENV PATH="/home/api/.local/bin:${PATH}"

COPY --chown=api:api requirements.txt .
RUN pip install -r requirements.txt
RUN pip install git+https://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@github.com/ekalaiv/IpssApiUtils.git --upgrade
RUN pip install sentry-sdk --upgrade
RUN pip install blinker

COPY --chown=api:api . .