```bash
docker compose --profile tinyllama up --abort-on-container-exit
```

```bash
docker compose --profile ingestion up --abort-on-container-exit
```

```bash
docker compose --profile chatbot-server up -d
```

```yaml
# llm configuration

model:
    model_provider: str
    model_name: str
    base_url: str # default None

vector_store:
    name: str
    can_initialize: bool # default False
```

```yaml
# ingestion configuration

pdf_sources:
    - path: "/some/path/to/pdf/file.pdf" 
      pages: [int] # default None 
      chunk_size: int # default 250
      chunk_overlap: int # default 20

web_sources:
    - url: "https://my.domain.com/about" 
      follow_links: bool # default False
      max_depth: int # default 2
      chunk_size: int # default 250
      chunk_overlap: int # default 20
```