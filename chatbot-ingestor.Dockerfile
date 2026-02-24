FROM alpine AS base

WORKDIR /src

COPY . /src

FROM python:3.11

WORKDIR /app

COPY --from=base /src/chatbot/requirements/base.txt /app/requirements/base.txt
COPY --from=base /src/chatbot/requirements/ingestion.txt  /app/requirements/ingestion.txt

RUN pip install -r /app/requirements/base.txt
RUN pip install -r /app/requirements/ingestion.txt

COPY --from=base /src/chatbot/chatbot/common /app/chatbot/common
COPY --from=base /src/chatbot/chatbot/ingestion    /app/chatbot/ingestion

ENV LLM_CONFIG_PATH=/config/llm_config.yml
ENV INGESTION_CONFIG_PATH=/config/ingestion_config.yml

VOLUME /data

VOLUME /config

ENTRYPOINT ["python", "-m", "chatbot.ingestion.main"]