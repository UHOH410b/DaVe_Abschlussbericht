from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parents[1]
ENV_PATH = BASE / ".env"


def load_env(path: Path = ENV_PATH) -> dict[str, str]:
    values: dict[str, str] = {}
    if path.exists():
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")

    merged = dict(os.environ)
    merged.update(values)
    return merged


def config() -> dict[str, str]:
    env = load_env()
    url = env.get("WEAVIATE_URL", "").strip()
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    return {
        "url": url.rstrip("/"),
        "api_key": env.get("WEAVIATE_API_KEY", "").strip(),
        "openai_api_key": env.get("WEAVIATE_OPENAI_API_KEY", "").strip(),
        "requirement_collection": env.get("WEAVIATE_REQUIREMENT_COLLECTION", "AtomicRequirement").strip(),
        "section_collection": env.get("WEAVIATE_SECTION_COLLECTION", "DocumentSection").strip(),
        "vectorizer": env.get("WEAVIATE_VECTORIZER", "none").strip(),
    }


def require_config() -> dict[str, str]:
    cfg = config()
    missing = [key for key in ["url", "api_key"] if not cfg[key]]
    if missing:
        raise SystemExit(
            "Weaviate ist noch nicht konfiguriert. Lege `work/ki-flow-anforderungskatalog/.env` "
            "nach Vorlage `.env.example` an und trage URL und API-Key ein."
        )
    return cfg


def request_json(
    cfg: dict[str, str],
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> Any:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        cfg["url"] + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {cfg['api_key']}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            **({"X-OpenAI-Api-Key": cfg["openai_api_key"]} if cfg.get("openai_api_key") else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read()
            if not raw:
                return {}
            return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Weaviate HTTP {exc.code} bei {method} {path}:\n{detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Weaviate nicht erreichbar: {exc}") from exc


def class_exists(cfg: dict[str, str], class_name: str) -> bool:
    schema = request_json(cfg, "GET", "/v1/schema")
    return any(item.get("class") == class_name for item in schema.get("classes", []))
