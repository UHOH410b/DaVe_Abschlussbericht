from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path
from typing import Any

from weaviate_common import class_exists, request_json, require_config


BASE = Path(__file__).resolve().parents[1]
VECTOR_DIR = BASE / "output" / "vector_index"
REQUIREMENTS_JSONL = VECTOR_DIR / "atomic_requirements.jsonl"
DATA_COLLECTIONS_JSONL = VECTOR_DIR / "data_collections.jsonl"
SOURCE_DOCUMENTS_JSONL = VECTOR_DIR / "source_documents.jsonl"
SECTIONS_JSONL = VECTOR_DIR / "document_sections.jsonl"
OUT_DIR = BASE / "output" / "weaviate"
REPORT = OUT_DIR / "weaviate_upload_report.md"


REQUIREMENT_PROPERTIES = [
    ("record_type", "text"),
    ("object_id", "text"),
    ("source_document_id", "text"),
    ("data_collection_id", "text"),
    ("source_reference", "text"),
    ("source_title", "text"),
    ("source_short_title", "text"),
    ("source_long_name", "text"),
    ("source_display", "text"),
    ("source_url", "text"),
    ("source_format", "text"),
    ("source_link_id", "text"),
    ("source_citation", "text"),
    ("original_text", "text"),
    ("text", "text"),
    ("requirement_type", "text"),
    ("document_type", "text"),
    ("requirement_count", "text"),
    ("data_collection_count", "text"),
    ("actor", "text"),
    ("action", "text"),
    ("object", "text"),
    ("condition", "text"),
    ("deadline_or_frequency", "text"),
    ("evidence_required", "text"),
    ("bpmn_element_type", "text"),
    ("extraction_status", "text"),
    ("short_title", "text"),
    ("long_title", "text"),
    ("display_title", "text"),
    ("description", "text"),
    ("catalog_level", "text"),
    ("parent_collection_title", "text"),
    ("data_sender", "text"),
    ("data_receiver", "text"),
    ("collection_method", "text"),
    ("data_source", "text"),
    ("data_structure", "text"),
    ("format", "text"),
    ("frequency", "text"),
    ("transmission_method", "text"),
    ("foundation_document_title", "text"),
]

SECTION_PROPERTIES = [
    ("object_id", "text"),
    ("source_document_id", "text"),
    ("data_collection_id", "text"),
    ("source_reference", "text"),
    ("text", "text"),
]


def read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
            if limit and len(rows) >= limit:
                break
    return rows


def make_class_payload(class_name: str, properties: list[tuple[str, str]], vectorizer: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "class": class_name,
        "description": "DaVe KI-Flow Collection",
        "vectorizer": vectorizer,
        "properties": [
            {"name": name, "dataType": [data_type], "description": name}
            for name, data_type in properties
        ],
    }
    if vectorizer == "text2vec-openai":
        payload["moduleConfig"] = {
            "text2vec-openai": {
                "model": "text-embedding-3-small",
                "type": "text",
                "vectorizeClassName": False,
            }
        }
    return payload


def ensure_class(cfg: dict[str, str], class_name: str, properties: list[tuple[str, str]], dry_run: bool) -> str:
    if class_exists(cfg, class_name):
        return ensure_properties(cfg, class_name, properties, dry_run)
    payload = make_class_payload(class_name, properties, cfg["vectorizer"])
    if dry_run:
        return f"{class_name}: would create"
    request_json(cfg, "POST", "/v1/schema", payload)
    return f"{class_name}: created"


def current_properties(cfg: dict[str, str], class_name: str) -> set[str]:
    schema = request_json(cfg, "GET", f"/v1/schema/{class_name}")
    return {prop.get("name", "") for prop in schema.get("properties", [])}


def ensure_properties(
    cfg: dict[str, str],
    class_name: str,
    properties: list[tuple[str, str]],
    dry_run: bool,
) -> str:
    existing = current_properties(cfg, class_name)
    missing = [(name, data_type) for name, data_type in properties if name not in existing]
    if not missing:
        return f"{class_name}: exists"
    if dry_run:
        return f"{class_name}: exists, would add {len(missing)} properties"
    for name, data_type in missing:
        request_json(
            cfg,
            "POST",
            f"/v1/schema/{class_name}/properties",
            {"name": name, "dataType": [data_type], "description": name},
        )
    return f"{class_name}: exists, added {len(missing)} properties"


def flatten_requirement(entry: dict[str, Any]) -> dict[str, Any]:
    meta = entry.get("metadata", {})
    source_display = entry.get("source_display", meta.get("source_display", ""))
    source_title = entry.get("source_title", meta.get("source_title", ""))
    source_long_name = entry.get("source_long_name", meta.get("source_long_name", ""))
    source_blob = " ".join(
        [
            str(entry.get("object_id", "")),
            str(entry.get("source_document_id", "")),
            str(source_display),
            str(source_title),
            str(source_long_name),
        ]
    ).lower()
    if (
        "bioland" in source_blob
        or "ecovin" in source_blob
        or "ifs" in source_blob
        or "klimawin" in source_blob
        or "qzbw" in source_blob
        or "qualitätszeichen" in source_blob
        or "biozeichen" in source_blob
    ):
        document_type = "Label/Standard"
    elif "förder" in source_blob or "foerder" in source_blob or "beihilfe" in source_blob or "vwv" in source_blob:
        document_type = "Förderung"
    elif any(term in source_blob for term in ["gesetz", "verordnung", "richtlinie", "pflsch", "duev", "düv"]):
        document_type = "Fachrecht"
    else:
        document_type = meta.get("document_type", "")
    return {
        "record_type": "atomic_requirement",
        "object_id": entry.get("object_id", ""),
        "source_document_id": entry.get("source_document_id", ""),
        "data_collection_id": entry.get("data_collection_id", ""),
        "source_reference": entry.get("source_reference", ""),
        "source_title": source_title or source_display,
        "source_short_title": entry.get("source_short_title", meta.get("source_short_title", "")),
        "source_long_name": source_long_name or source_title,
        "source_display": source_display,
        "source_url": entry.get("source_url", meta.get("source_url", "")),
        "source_format": entry.get("source_format", meta.get("source_format", "")),
        "source_link_id": entry.get("source_link_id", meta.get("source_link_id", "")),
        "source_citation": entry.get("source_citation", meta.get("source_citation", "")),
        "original_text": entry.get("original_text", meta.get("original_text", "")),
        "text": entry.get("text", ""),
        "requirement_type": meta.get("requirement_type", ""),
        "document_type": document_type,
        "actor": meta.get("actor", ""),
        "action": meta.get("action", ""),
        "object": meta.get("object", ""),
        "condition": meta.get("condition", ""),
        "deadline_or_frequency": meta.get("deadline_or_frequency", ""),
        "evidence_required": meta.get("evidence_required", ""),
        "bpmn_element_type": meta.get("bpmn_element_type", ""),
        "extraction_status": meta.get("extraction_status", ""),
        "short_title": source_display,
        "long_title": source_title or source_long_name or source_display,
        "description": "",
        "data_sender": "",
        "data_receiver": "",
        "format": "",
        "frequency": "",
        "transmission_method": "",
        "foundation_document_title": "",
    }


def flatten_data_collection(entry: dict[str, Any]) -> dict[str, Any]:
    meta = entry.get("metadata", {})
    return {
        "record_type": "data_collection",
        "object_id": entry.get("object_id", ""),
        "source_document_id": entry.get("source_document_id", ""),
        "data_collection_id": entry.get("data_collection_id", ""),
        "source_reference": entry.get("source_reference", ""),
        "source_title": meta.get("foundation_document_title", ""),
        "source_short_title": entry.get("source_reference", ""),
        "source_long_name": meta.get("foundation_document_title", ""),
        "source_display": entry.get("source_reference", "") or meta.get("foundation_document_title", ""),
        "source_url": meta.get("source_url", ""),
        "source_format": meta.get("format", ""),
        "source_link_id": "",
        "source_citation": " | ".join(
            part for part in [meta.get("foundation_document_title", ""), entry.get("source_reference", "")] if part
        ),
        "original_text": "",
        "text": entry.get("text", ""),
        "requirement_type": "",
        "document_type": "",
        "requirement_count": "",
        "data_collection_count": "",
        "actor": "",
        "action": "",
        "object": "",
        "condition": "",
        "deadline_or_frequency": "",
        "evidence_required": "",
        "bpmn_element_type": "",
        "extraction_status": "",
        "short_title": meta.get("short_title", ""),
        "long_title": meta.get("long_title", ""),
        "display_title": meta.get("display_title", "") or meta.get("short_title", "") or meta.get("long_title", ""),
        "description": meta.get("description", ""),
        "catalog_level": meta.get("catalog_level", ""),
        "parent_collection_title": meta.get("parent_collection_title", ""),
        "data_sender": meta.get("data_sender", ""),
        "data_receiver": meta.get("data_receiver", ""),
        "collection_method": meta.get("collection_method", ""),
        "data_source": meta.get("data_source", ""),
        "data_structure": meta.get("data_structure", ""),
        "format": meta.get("format", ""),
        "frequency": meta.get("frequency", ""),
        "transmission_method": meta.get("transmission_method", ""),
        "foundation_document_title": meta.get("foundation_document_title", ""),
    }


def flatten_source_document(entry: dict[str, Any]) -> dict[str, Any]:
    meta = entry.get("metadata", {})
    return {
        "record_type": "source_document",
        "object_id": entry.get("object_id", ""),
        "source_document_id": entry.get("source_document_id", ""),
        "data_collection_id": entry.get("data_collection_id", ""),
        "source_reference": entry.get("source_reference", ""),
        "source_title": entry.get("source_title", meta.get("long_title", "")),
        "source_short_title": entry.get("source_short_title", ""),
        "source_long_name": entry.get("source_long_name", ""),
        "source_display": entry.get("source_display", meta.get("display_title", "")),
        "source_url": entry.get("source_url", meta.get("source_url", "")),
        "source_format": entry.get("source_format", meta.get("source_format", "")),
        "source_link_id": entry.get("source_link_id", meta.get("source_link_id", "")),
        "source_citation": entry.get("source_citation", ""),
        "original_text": "",
        "text": entry.get("text", ""),
        "requirement_type": "",
        "document_type": meta.get("document_type", ""),
        "requirement_count": meta.get("requirement_count", ""),
        "data_collection_count": meta.get("data_collection_count", ""),
        "actor": "",
        "action": "",
        "object": "",
        "condition": "",
        "deadline_or_frequency": "",
        "evidence_required": "",
        "bpmn_element_type": "",
        "extraction_status": meta.get("extraction_status", ""),
        "short_title": meta.get("short_title", entry.get("source_display", "")),
        "long_title": meta.get("long_title", entry.get("source_title", "")),
        "display_title": meta.get("display_title", entry.get("source_display", "")),
        "description": meta.get("description", entry.get("source_title", "")),
        "catalog_level": "",
        "parent_collection_title": "",
        "data_sender": "",
        "data_receiver": "",
        "collection_method": "",
        "data_source": "",
        "data_structure": "",
        "format": entry.get("source_format", meta.get("source_format", "")),
        "frequency": "",
        "transmission_method": "",
        "foundation_document_title": "",
    }


def flatten_section(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "object_id": entry.get("object_id", ""),
        "source_document_id": entry.get("source_document_id", ""),
        "data_collection_id": entry.get("data_collection_id", ""),
        "source_reference": entry.get("source_reference", ""),
        "text": entry.get("text", ""),
    }


def stable_uuid(class_name: str, object_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"dave:{class_name}:{object_id}"))


def upload_batch(cfg: dict[str, str], class_name: str, objects: list[dict[str, Any]], dry_run: bool) -> str:
    if dry_run:
        return f"{class_name}: would upload {len(objects)} objects"
    payload = {
        "objects": [
            {
                "class": class_name,
                "id": stable_uuid(class_name, str(obj.get("object_id", idx))),
                "properties": obj,
            }
            for idx, obj in enumerate(objects)
        ]
    }
    result = request_json(cfg, "POST", "/v1/batch/objects", payload)
    errors = [item for item in result if item.get("result", {}).get("errors")]
    if errors:
        return f"{class_name}: uploaded with {len(errors)} errors"
    return f"{class_name}: uploaded {len(objects)} objects"


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload DaVe-Anforderungen nach Weaviate.")
    parser.add_argument("--dry-run", action="store_true", help="Nur prüfen, nichts schreiben.")
    parser.add_argument("--limit", type=int, help="Maximale Zahl je Collection.")
    parser.add_argument("--skip-sections", action="store_true", help="Nur Anforderungen hochladen.")
    parser.add_argument("--skip-data-collections", action="store_true", help="Keine Datenerhebungen hochladen.")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cfg = require_config()

    requirement_class = cfg["requirement_collection"]
    section_class = cfg["section_collection"]
    lines = ["# Weaviate Upload Report", "", f"Dry run: {args.dry_run}", f"URL: `{cfg['url']}`", ""]

    lines.append(ensure_class(cfg, requirement_class, REQUIREMENT_PROPERTIES, args.dry_run))
    requirement_entries = [flatten_requirement(item) for item in read_jsonl(REQUIREMENTS_JSONL, args.limit)]
    data_collection_entries = []
    if not args.skip_data_collections and DATA_COLLECTIONS_JSONL.exists():
        data_collection_entries = [
            flatten_data_collection(item) for item in read_jsonl(DATA_COLLECTIONS_JSONL, args.limit)
        ]
    source_document_entries = []
    if SOURCE_DOCUMENTS_JSONL.exists():
        source_document_entries = [
            flatten_source_document(item) for item in read_jsonl(SOURCE_DOCUMENTS_JSONL, args.limit)
        ]
    mixed_entries = requirement_entries + data_collection_entries + source_document_entries
    lines.append(
        f"{requirement_class}: prepared {len(requirement_entries)} atomic requirements, {len(data_collection_entries)} data collections and {len(source_document_entries)} source documents"
    )
    lines.append(upload_batch(cfg, requirement_class, mixed_entries, args.dry_run))

    if not args.skip_sections:
        lines.append(ensure_class(cfg, section_class, SECTION_PROPERTIES, args.dry_run))
        section_entries = [flatten_section(item) for item in read_jsonl(SECTIONS_JSONL, args.limit)]
        lines.append(upload_batch(cfg, section_class, section_entries, args.dry_run))

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
