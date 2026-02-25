# Docker compose

For easy deployment the included `docker-compose.yml` file provides different profiles:

Profiles can be executed independently depending on the deployment stage or workflow.

It assumes using `Ollama` without GPU support.

**Typical workflow**
1. Initialize and pull the model (`init-model`)
2. Run ingestion (`chatbot-ingestion`)
3. Start the server (`chatbot-server`)

## init-model

Ensures `Ollama` is initialized and pulls the desired model before running the application.

Use the environment variable `LLM_MODEL` to select the model.

Default value: `tinyllama`

*This profile can optionally be launched using the `--abort-on-container-exit`
parameter to stop execution once the model initialization completes.*

```bash
export LLM_MODEL="qwen2.5:0.5b"

docker compose --profile init-model up --abort-on-container-exit \
&& docker compose --profile init-model down
```

## chatbot-ingestion

Runs the ingestion process and stops automatically once ingestion is complete.

```bash
docker compose --profile chatbot-ingestion up --abort-on-container-exit \
&& docker compose --profile chatbot-ingestion down
```

## chatbot-server

Runs the chatbot server in detached mode.

```bash
docker compose --profile chatbot-server up -d
```
