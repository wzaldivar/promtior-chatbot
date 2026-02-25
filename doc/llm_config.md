# llm_config.yml 

Both the ingestion process and the server use the environment variable 
`LLM_CONFIG_PATH` to load the LLM configuration.

The same configuration file can be shared between the ingestion process and the server. 

For Docker containers it is defined by default as:

```Dockerfile
ENV LLM_CONFIG_PATH=/config/llm_config.yml
```

```yaml
# llm configuration

model:
    model_provider: "ollama" # required
    model_name: "tinyllama"  # required
    base_url: null           # optional (default: null)
    ... # model specific configuration

vector_store:
    name: "faiss"            # required
    can_initialize: false    # optional (default: false)
    ... # vector store specific configuration
```

## model 

### model_provider 

> The LLM platform identifier *(ollama, openai, etc.).* 

***Currently supported model providers:***
- ollama 

### model_name

> The specific model to use *(tinyllama, llama3, etc.).* 

### base_url

> Custom API endpoint URL. Set to null to use the provider default endpoint.

```yaml
# ollama model configuration example

model:
    model_provider: "ollama"
    model_name: "tinyllama"
    base_url: "https://my.ollama.server:11434"
```

## vector_store

### name

> Type of vector store used *(faiss, chroma, etc.).* 

***Currently supported vector stores:***
- faiss

### can_initialize 

> Flag indicating whether the vector store can be initialized from scratch.
> 
> This is typically enabled for in-memory or first-time initialization scenarios.
>
> Default value: false

## faiss 

### path

> Vector store snapshot storage location. 
> 
> Default value: null (in-memory only)

```yaml
# faiss vector store configuration example

vector_store:
    name: "faiss"
    can_initialize: true # optional (default: true)
    path: "/data/faiss"  # optional (default: null)
```