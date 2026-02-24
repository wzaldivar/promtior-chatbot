FROM alpine AS base

WORKDIR /src

COPY . /src

FROM node:lts-alpine AS ui_builder

WORKDIR /src

COPY --from=base /src/ui /src

RUN npm ci && npm run build

FROM python:3.11

WORKDIR /app

COPY --from=ui_builder /src/dist /app/ui

COPY --from=base /src/chatbot/requirements/base.txt /app/requirements/base.txt
COPY --from=base /src/chatbot/requirements/api.txt  /app/requirements/api.txt

RUN pip install -r /app/requirements/base.txt
RUN pip install -r /app/requirements/api.txt

COPY --from=base /src/chatbot/chatbot/common /app/chatbot/common
COPY --from=base /src/chatbot/chatbot/api    /app/chatbot/api

ENV LLM_CONFIG_PATH=/config/llm_config.yml

VOLUME /data

VOLUME /config

EXPOSE 8000

ENTRYPOINT ["python", "-m", "uvicorn", "chatbot.api.main:app", "--host", "0.0.0.0"]