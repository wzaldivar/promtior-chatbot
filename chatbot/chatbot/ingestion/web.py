from collections import deque
from urllib.parse import urlparse, urlunparse, urljoin

import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader

from chatbot.ingestion.config import get_ingestion_config
from chatbot.ingestion.vector_store import store_documents


def normalize_url(url):
    parsed = urlparse(url)
    normalized = parsed._replace(fragment="", query="")
    normalized_path = normalized.path.rstrip("/")
    normalized = normalized._replace(path=normalized_path)
    return urlunparse(normalized)


def discover_urls(url, max_depth=2):
    to_visit = deque([(url, 0)])
    visited = set()
    unique_urls = []

    domain = urlparse(url).netloc

    while to_visit:
        current_url, depth = to_visit.popleft()
        normalized = normalize_url(current_url)

        if normalized in visited or depth > max_depth:
            continue

        visited.add(normalized)
        unique_urls.append(normalized)

        if depth < max_depth:
            try:
                res = requests.get(current_url)
                soup = BeautifulSoup(res.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    href = urljoin(normalized, link.get("href"))
                    href = normalize_url(href)
                    if urlparse(href).netloc == domain and href not in visited:
                        to_visit.append((href, depth + 1))
            except Exception as e:
                print(f"Failed to fetch {current_url}: {e}")

    return unique_urls


def load_url(url):
    docs = []

    try:
        loader = WebBaseLoader(url)
        docs.extend(loader.load())
        print(f"{url} loaded")
    except Exception as e:
        print(f"Failed to load {url}: {e}")

    return docs


def ingest_websites():
    web_sources = get_ingestion_config().web_sources

    for web_source in web_sources:
        docs = []
        urls = []
        normalized = normalize_url(web_source.url)
        if web_source.follow_links:
            urls.extend(discover_urls(normalized, max_depth=web_source.max_depth))
        else:
            urls.append(normalized)

        for url in urls:
            docs.extend(load_url(url))

        store_documents(docs, web_source)
