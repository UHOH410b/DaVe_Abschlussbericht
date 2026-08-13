from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
MASTER_XLSX = BASE / "output" / "master_catalog" / "master_catalog.xlsx"
LINKS_CSV = BASE / "output" / "source_document_links.csv"
DATA_COLLECTIONS_JSON = BASE / "output" / "data_collections" / "data_collections.json"
OUT_DIR = BASE / "output" / "base44_seed"
OUT_JSON = OUT_DIR / "base44_requirement_seed.json"
OUT_CSV = OUT_DIR / "atomic_requirements_for_import.csv"
OUT_DATA_COLLECTIONS_CSV = OUT_DIR / "data_collections_for_import.csv"
REPORT = OUT_DIR / "base44_seed_report.md"


def clean(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def read_sheet(name: str) -> pd.DataFrame:
    try:
        return pd.read_excel(MASTER_XLSX, sheet_name=name)
    except ValueError:
        return pd.DataFrame()


def category_map(assignments: pd.DataFrame) -> dict[str, dict]:
    result: dict[str, dict] = {}
    if assignments.empty:
        return result
    for requirement_id, group in assignments.groupby("Requirement_ID"):
        primary = group[group["Is_Primary_Category"] == True]
        result[str(requirement_id)] = {
            "primary_category": clean(primary.iloc[0]["Category_Name"]) if not primary.empty else "",
            "secondary_categories": [
                clean(row["Category_Name"])
                for _, row in group[group["Is_Primary_Category"] != True].iterrows()
                if clean(row["Category_Name"])
            ],
            "assignments": [
                {
                    "category_id": clean(row.get("Category_ID")),
                    "category_name": clean(row.get("Category_Name")),
                    "category_type": clean(row.get("Category_Type")),
                    "is_primary_category": bool(row.get("Is_Primary_Category")),
                    "confidence": clean(row.get("Confidence")),
                }
                for _, row in group.iterrows()
            ],
        }
    return result


def source_map() -> dict[str, dict]:
    if not LINKS_CSV.exists():
        return {}
    links = pd.read_csv(LINKS_CSV, encoding="utf-8-sig")
    foundation = links[links["Link_Type"].astype(str) == "Grundlagendokument"]
    result: dict[str, dict] = {}
    for source_document_id, group in foundation.groupby("Source_Document_ID"):
        first = group.iloc[0]
        result[str(source_document_id)] = {
            "source_document_id": clean(source_document_id),
            "title": clean(first.get("Link_Title")),
            "url": clean(first.get("URL")),
            "format": clean(first.get("Format")),
            "kurztitel": clean(first.get("Kurztitel")),
        }
    return result


def relation_map(relations: pd.DataFrame) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    if relations.empty:
        return result
    for _, row in relations.iterrows():
        for side, other in [("Requirement_ID_A", "Requirement_ID_B"), ("Requirement_ID_B", "Requirement_ID_A")]:
            requirement_id = clean(row.get(side))
            if not requirement_id:
                continue
            result.setdefault(requirement_id, []).append(
                {
                    "other_requirement_id": clean(row.get(other)),
                    "relation_type": clean(row.get("Relation_Type")),
                    "similarity_rationale": clean(row.get("Similarity_Rationale")),
                    "confidence": clean(row.get("Confidence")),
                    "review_status": clean(row.get("Review_Status")),
                }
            )
    return result


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    requirements = read_sheet("Atomic_Requirements")
    assignments = read_sheet("Category_Assignments")
    relations = read_sheet("Relation_Candidates")
    categories = category_map(assignments)
    sources = source_map()
    relations_by_requirement = relation_map(relations)
    data_collections = []
    if DATA_COLLECTIONS_JSON.exists():
        data_collections = json.loads(DATA_COLLECTIONS_JSON.read_text(encoding="utf-8"))

    records = []
    for _, row in requirements.iterrows():
        requirement_id = clean(row.get("Requirement_ID"))
        source_document_id = clean(row.get("Source_Document_ID"))
        cat = categories.get(requirement_id, {})
        source = sources.get(source_document_id, {})
        record = {
            "requirement_id": requirement_id,
            "source_document_id": source_document_id,
            "source_reference": clean(row.get("Source_Reference")),
            "atomic_requirement": clean(row.get("Atomic_Requirement")),
            "requirement_type": clean(row.get("Requirement_Type")),
            "actor": clean(row.get("Actor")),
            "action": clean(row.get("Action")),
            "object": clean(row.get("Object")),
            "condition": clean(row.get("Condition")),
            "deadline_or_frequency": clean(row.get("Deadline_or_Frequency")),
            "evidence_required": clean(row.get("Evidence_Required")),
            "primary_category": clean(cat.get("primary_category")),
            "secondary_categories": cat.get("secondary_categories", []),
            "source_title": clean(source.get("title")),
            "source_url": clean(source.get("url")),
            "source_format": clean(source.get("format")),
            "extraction_status": clean(row.get("Extraction_Status")),
            "notes": clean(row.get("Notes")),
            "category_assignments": cat.get("assignments", []),
            "relations": relations_by_requirement.get(requirement_id, []),
        }
        records.append(record)

    payload = {
        "version": "0.1",
        "description": "Seed-Daten für die Anforderungssuche in Base44.",
        "counts": {
            "atomic_requirements": len(records),
            "data_collections": len(data_collections),
            "source_documents": len(sources),
            "category_assignments": len(assignments),
            "relation_candidates": len(relations),
        },
        "atomic_requirements": records,
        "data_collections": data_collections,
        "source_documents": list(sources.values()),
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.DataFrame(records).drop(columns=["category_assignments", "relations"]).to_csv(
        OUT_CSV, index=False, encoding="utf-8-sig"
    )
    if data_collections:
        pd.DataFrame(
            {
                **record,
                "foundation_document_urls": "; ".join(record.get("foundation_document_urls", [])),
                "transmission_urls": "; ".join(record.get("transmission_urls", [])),
            }
            for record in data_collections
        ).to_csv(OUT_DATA_COLLECTIONS_CSV, index=False, encoding="utf-8-sig")

    lines = [
        "# Base44 Seed Export Report",
        "",
        f"Atomic requirements: {len(records)}",
        f"Data collections: {len(data_collections)}",
        f"Source documents: {len(sources)}",
        f"Category assignments: {len(assignments)}",
        f"Relation candidates: {len(relations)}",
        "",
        f"JSON: `{OUT_JSON}`",
        f"CSV: `{OUT_CSV}`",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_JSON)


if __name__ == "__main__":
    main()
