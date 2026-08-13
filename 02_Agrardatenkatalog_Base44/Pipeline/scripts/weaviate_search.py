from __future__ import annotations

import argparse
import sys
from typing import Any

from weaviate_common import request_json, require_config


def graphql_query(class_name: str, query: str, limit: int) -> dict[str, Any]:
    escaped = query.replace("\\", "\\\\").replace('"', '\\"')
    return {
        "query": f"""
        {{
          Get {{
            {class_name}(
              bm25: {{ query: "{escaped}" }}
              limit: {limit}
            ) {{
              object_id
              record_type
              source_document_id
              data_collection_id
              source_reference
              source_title
              source_short_title
              source_long_name
              source_display
              source_url
              source_format
              source_citation
              text
              requirement_type
              actor
              deadline_or_frequency
              evidence_required
              short_title
              description
              data_sender
              data_receiver
              frequency
              format
              _additional {{
                score
              }}
            }}
          }}
        }}
        """
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Einfache Weaviate-Suche für AtomicRequirement.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    cfg = require_config()
    payload = graphql_query(cfg["requirement_collection"], args.query, args.limit)
    result = request_json(cfg, "POST", "/v1/graphql", payload)
    if result.get("errors"):
        raise SystemExit(result["errors"])

    rows = result.get("data", {}).get("Get", {}).get(cfg["requirement_collection"], [])
    print(f"Treffer: {len(rows)}")
    for idx, row in enumerate(rows, start=1):
        score = row.get("_additional", {}).get("score", "")
        record_type = row.get("record_type") or "unknown"
        print(f"\n{idx}. {row.get('object_id')} | {record_type} | Score: {score}")
        if record_type == "data_collection":
            print(f"Titel: {row.get('short_title')}")
            print(f"Sender -> Empfänger: {row.get('data_sender')} -> {row.get('data_receiver')}")
            if row.get("frequency"):
                print(f"Frequenz: {row.get('frequency')}")
            if row.get("format"):
                print(f"Format: {row.get('format')}")
            print(row.get("description", "") or row.get("text", ""))
            continue

        citation = row.get("source_citation") or row.get("source_display") or " / ".join(
            part for part in [row.get("source_reference"), row.get("source_document_id")] if part
        )
        print(f"Quelle: {citation}")
        if row.get("source_url"):
            print(f"URL: {row.get('source_url')}")
        print(row.get("text", ""))
        if row.get("deadline_or_frequency"):
            print(f"Frist: {row.get('deadline_or_frequency')}")
        if row.get("evidence_required"):
            print(f"Nachweis: {row.get('evidence_required')}")


if __name__ == "__main__":
    main()
