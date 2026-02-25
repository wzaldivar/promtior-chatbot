Being my first experience developing a 
[RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation), 
the project is built around some ideas

- Independent components able to be executed on the same machine
or distributed across different environments and cloud providers

- Incremental development, the project was built on different stages
that represented milestones on the functionality or integration

- Avoid vendor locking, from inception required to be easy to be reconfigured
allowing LLM providers, vector stores, or models to be replaced with minimal
implementation effort. 

## Development approach

### Web UI

The first module to be implemented was a simple Web UI

Requirements:
- Minimum footprint without a lot of extra features
- Easy to deploy
- Able to execute REST API calls
- Quick prototyping that can be reused later

Vite + React was the selection, the simple UI didn't require more 
than being able to call backend and render the responses.
No session handling or keeping history as part of the implementation.

Using react components with simple CSS allows to reuse the same components
later on a framework with batteries included like Next.js

### Rest API

Next step, use a `REST` capable Python library/framework

FastAPI was the selection, minimun setup required to get a simple POST
endpoint working.

FastAPI integration with Pydantic, later became core for the extensibility
thanks to `Discriminated Union`

Allowed to tune the integration with the UI via static responses

### LLM integration

On this step the important part was to be sure the backend was able to
communicate with the selected LLM Provider and model, being able
to pass questions from the UI to the LLM and return a response to the UI

### Ingestion service

For the ingestion service two alternatives were considered

1. Made it a REST endpoint in the same backend
2. Made it an independent service that can be executed from a different instance

The decision was to follow the principle independent execution, then decided 
to move the LLM configuration and initializations to a common module

See [llm_config.yml](llm_config.md)

The ingestion of the PDF file led to the realization there should be some method
to avoid ingesting all the information from a PDF because part of it can be considered
sensitive information for the evaluation.

1. Manual extraction of the text to a new document (extra manual step)
2. Document edition to remove sensitive information (tool required)
3. Configurable page selection

Decided to follow the flexible configuration, that also allowed fast iteration
over the provided data

See [ingestion_config.yml](ingestion_config.md)

### Agent and context integration

Refinement of the prompt and the similarity search via prompt updating and
changing ingestion splitter configurations

### Deployment

Prepare to be deployed as different containers. Even when is possible to deploy
directly usinng containers on different cloud providers, Docker Compose was selected
for a reproducible deployment aligned with my experience.

See [docker](docker.md)