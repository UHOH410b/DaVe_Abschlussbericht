from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
MASTER_XLSX = BASE / "output" / "master_catalog" / "master_catalog.xlsx"
LINKS_CSV = BASE / "output" / "source_document_links.csv"
DATA_COLLECTIONS_CSV = BASE / "output" / "data_collections" / "data_collections.csv"
OUT_DIR = BASE / "output" / "base44_import_tables"


def clean(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def source_display_title(title: str) -> str:
    normalized = clean(title)
    replacements = {
        "Qualitätszeichen Baden-Württemberg": "QZBW (Qualitätszeichen Baden-Württemberg)",
        "Qualitaetszeichen Baden-Wuerttemberg": "QZBW (Qualitätszeichen Baden-Württemberg)",
        "Biozeichen Baden-Württemberg": "BioZBW (Biozeichen Baden-Württemberg)",
        "Biozeichen Baden-Wuerttemberg": "BioZBW (Biozeichen Baden-Württemberg)",
    }
    return replacements.get(normalized, normalized)


def normalize_display_text(value: object) -> str:
    text = clean(value)
    if not text:
        return ""
    replacements = {
        "Nicht aufbringung": "Nichtaufbringung",
        "Nicht-Aufbringung": "Nichtaufbringung",
        "nicht aufbringung": "Nichtaufbringung",
        "nicht-Aufbringung": "Nichtaufbringung",
        "Qualitätszeichen Baden-Württemberg": "QZBW (Qualitätszeichen Baden-Württemberg)",
        "Qualitaetszeichen Baden-Wuerttemberg": "QZBW (Qualitätszeichen Baden-Württemberg)",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def read_sheet(name: str) -> pd.DataFrame:
    try:
        return pd.read_excel(MASTER_XLSX, sheet_name=name)
    except ValueError:
        return pd.DataFrame()


def confidence_number(value: object) -> float:
    text = clean(value).lower()
    if text == "hoch":
        return 0.9
    if text == "mittel":
        return 0.65
    if text == "niedrig":
        return 0.4
    try:
        return float(text)
    except ValueError:
        return 0.5


def app_requirement_type(row: pd.Series) -> str:
    text = " ".join([clean(row.get("Requirement_Type")), clean(row.get("Atomic_Requirement"))]).lower()
    if "freiwillig" in text or "kann " in text:
        return "freiwillig"
    if clean(row.get("Condition")) or "wenn " in text or "sofern " in text:
        return "bedingt"
    return "pflicht"


def relation_type_app(value: object) -> str:
    text = clean(value).lower()
    if "konflikt" in text or "widerspruch" in text:
        return "widerspruechlich"
    if "konkretisiert" in text or "abgeleitet" in text:
        return "abgeleitet"
    if "überlapp" in text or "ueberlapp" in text or "ergän" in text or "ergaenz" in text:
        return "ergaenzend"
    return "aehnlich"


def category_type_app(value: object) -> str:
    text = clean(value).lower()
    if "recht" in text:
        return "recht"
    if "förder" in text or "foerder" in text:
        return "foerder"
    return "thema"


def source_documents() -> pd.DataFrame:
    links = pd.read_csv(LINKS_CSV, encoding="utf-8-sig")
    foundation = links[links["Link_Type"].astype(str) == "Grundlagendokument"]
    rows = []
    seen = set()
    for _, row in foundation.iterrows():
        source_document_id = clean(row.get("Source_Document_ID"))
        if not source_document_id or source_document_id in seen:
            continue
        seen.add(source_document_id)
        rows.append(
            {
                "source_document_id": source_document_id,
                "title": source_display_title(clean(row.get("Link_Title")) or clean(row.get("Kurztitel"))),
                "version": "",
                "publisher": "",
                "url": clean(row.get("URL")),
                "document_type": "sonstiges",
                "format": clean(row.get("Format")),
                "status": "gueltig",
            }
        )
    return pd.DataFrame(rows)


def atomic_requirements(requirements: pd.DataFrame, assignments: pd.DataFrame, sources: pd.DataFrame) -> pd.DataFrame:
    primary = assignments[assignments["Is_Primary_Category"] == True][
        ["Requirement_ID", "Category_Name"]
    ].rename(columns={"Category_Name": "primary_category"})
    secondary = (
        assignments[assignments["Is_Primary_Category"] != True]
        .groupby("Requirement_ID")["Category_Name"]
        .apply(lambda values: "; ".join(sorted(set(clean(v) for v in values if clean(v)))))
        .reset_index()
        .rename(columns={"Category_Name": "secondary_categories"})
    )
    source_lookup = sources.set_index("source_document_id").to_dict("index") if not sources.empty else {}

    enriched = requirements.merge(primary, on="Requirement_ID", how="left").merge(
        secondary, on="Requirement_ID", how="left"
    )
    rows = []
    for _, row in enriched.iterrows():
        source_document_id = clean(row.get("Source_Document_ID"))
        source = source_lookup.get(source_document_id, {})
        evidence = clean(row.get("Evidence_Required"))
        rows.append(
            {
                "requirement_id": clean(row.get("Requirement_ID")),
                "source_document_id": source_document_id,
                "source_reference": clean(row.get("Source_Reference")),
                "atomic_requirement": normalize_display_text(row.get("Atomic_Requirement")),
                "requirement_type": app_requirement_type(row),
                "actor": clean(row.get("Actor")),
                "action": normalize_display_text(row.get("Action")),
                "object": normalize_display_text(row.get("Object")),
                "condition": normalize_display_text(row.get("Condition")),
                "deadline_or_frequency": clean(row.get("Deadline_or_Frequency")),
                "evidence_required": bool(evidence),
                "primary_category": clean(row.get("primary_category")),
                "secondary_categories": clean(row.get("secondary_categories")),
                "source_title": clean(source.get("title")),
                "source_url": clean(source.get("url")),
                "extraction_status": "extrahiert",
                "notes": clean(row.get("Notes")),
            }
        )
    return pd.DataFrame(rows)


def category_assignments(assignments: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in assignments.iterrows():
        rows.append(
            {
                "requirement_id": clean(row.get("Requirement_ID")),
                "category_id": clean(row.get("Category_ID")),
                "category_name": clean(row.get("Category_Name")),
                "category_type": category_type_app(row.get("Category_Type")),
                "is_primary_category": bool(row.get("Is_Primary_Category")),
                "confidence": confidence_number(row.get("Confidence")),
            }
        )
    return pd.DataFrame(rows)


def requirement_relations(relations: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in relations.iterrows():
        rows.append(
            {
                "requirement_id_a": clean(row.get("Requirement_ID_A")),
                "requirement_id_b": clean(row.get("Requirement_ID_B")),
                "relation_type": relation_type_app(row.get("Relation_Type")),
                "similarity_rationale": clean(row.get("Similarity_Rationale")),
                "confidence": confidence_number(row.get("Confidence")),
                "review_status": "offen",
            }
        )
    return pd.DataFrame(rows)


def data_catalog_entries() -> pd.DataFrame:
    if not DATA_COLLECTIONS_CSV.exists():
        return pd.DataFrame()
    df = pd.read_csv(DATA_COLLECTIONS_CSV, encoding="utf-8-sig")
    rows = []
    for _, row in df.iterrows():
        rows.append(
            {
                "dct:subject": clean(row.get("short_title")),
                "dct:source": clean(row.get("foundation_document_title")),
                "dct:isPartOf": clean(row.get("process")),
                "dct:description": clean(row.get("description")),
                "dcat:frequency": clean(row.get("frequency")),
                "doc_id": clean(row.get("source_document_id")),
                "doc_title": clean(row.get("foundation_document_title")),
                "doc_type": "data_collection",
                "doc_publisher": clean(row.get("data_receiver")),
                "doc_year": "",
                "doc_source_ref": clean(row.get("foundation_document_urls")),
                "layout_type": "metadata_catalog_row",
                "function_type": "data_requirement",
                "data_point_label_raw": clean(row.get("short_title")),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    requirements = read_sheet("Atomic_Requirements")
    assignments = read_sheet("Category_Assignments")
    relations = read_sheet("Relation_Candidates")
    sources = source_documents()

    tables = {
        "SourceDocument": sources,
        "AtomicRequirement": atomic_requirements(requirements, assignments, sources),
        "RequirementCategoryAssignment": category_assignments(assignments),
        "RequirementRelation": requirement_relations(relations),
        "DataCatalogEntry": data_catalog_entries(),
    }

    for name, table in tables.items():
        table.to_csv(OUT_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")

    with pd.ExcelWriter(OUT_DIR / "base44_import_tables.xlsx", engine="openpyxl") as writer:
        for name, table in tables.items():
            table.to_excel(writer, sheet_name=name[:31], index=False)

    report = ["# Base44 Import Tables Report", ""]
    for name, table in tables.items():
        report.append(f"- {name}: {len(table)} rows")
    (OUT_DIR / "base44_import_tables_report.md").write_text("\n".join(report), encoding="utf-8")
    print(OUT_DIR / "base44_import_tables.xlsx")


if __name__ == "__main__":
    main()
