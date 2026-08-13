from __future__ import annotations

from weaviate_common import config, request_json, require_config


def main() -> None:
    cfg = require_config()
    meta = request_json(cfg, "GET", "/v1/meta")
    schema = request_json(cfg, "GET", "/v1/schema")
    print("Weaviate erreichbar")
    print(f"URL: {cfg['url']}")
    print(f"Version: {meta.get('version', 'unbekannt')}")
    print(f"Vectorizer setting: {cfg['vectorizer']}")
    print(f"Classes: {len(schema.get('classes', []))}")
    for cls in schema.get("classes", []):
        print(f"- {cls.get('class')}")


if __name__ == "__main__":
    main()
