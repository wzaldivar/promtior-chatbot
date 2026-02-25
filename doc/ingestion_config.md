# ingestion_config.yml

Ingestion process uses the environment variable `INGESTION_CONFIG_PATH` 
to load the ingestion configuration.

For Docker containers it is defined by default as:

```Dockerfile
ENV INGESTION_CONFIG_PATH=/config/ingestion_config.yml
```

```yaml
# ingestion configuration

pdf_sources:                        # optional
  - path: "/path/to/some.pdf"       # required
    pages: [1, 3, 4]                # optional (default: null) 
    chunk_size: 250                 # optional (default: 250)
    chunk_overlap: 20               # optional (default: 20)

web_sources:                        # optional
  - url: "https://my.website.com"   # required
    follow_links: true              # optional (default: false)
    max_depth: 2                    # optional (default: 2)
    chunk_size: 250                 # optional (default: 250)
    chunk_overlap: 20               # optional (default: 20)
```

## pdf_sources

> The list of PDF files to ingest.

### path

> The path to the PDF file.

### pages

> List of pages to import from the PDF file.
>
> Default value: null (all pages)

## web_sources

> The list of web pages to ingest.

### url

> The URL of the web page

### follow_links

> Flag indicating whether links found on the page should also be ingested.
>
> Only same-domain links are followed.
>
> Default value: false

### max_depth

> Maximum depth to follow links.
>
> Default value: 2

## shared configuration

### chunk_size

> Chunk size for the splitter
>
> Default value: 250

### chunk_overlap

> Chunk overlap for the splitter
>
> Default value: 20
