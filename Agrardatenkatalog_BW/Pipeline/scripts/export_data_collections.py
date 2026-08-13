from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
METADATA = BASE / "input" / "source_document_metadata_active.xlsx"
OUT_DIR = BASE / "output" / "data_collections"
OUT_JSONL = OUT_DIR / "data_collections.jsonl"
OUT_JSON = OUT_DIR / "data_collections.json"
OUT_CSV = OUT_DIR / "data_collections.csv"
OUT_XLSX = OUT_DIR / "data_collections.xlsx"
REPORT = OUT_DIR / "data_collections_report.md"


SEARCH_FIELDS = [
    "Kurztitel",
    "Langtitel (sofern zutreffend)",
    "Beschreibung",
    "Grundlagendokument Titel",
    "Datengebende Stelle",
    "Datenempfangende Stelle",
    "Erhebungsmethode",
    "Datenquelle",
    "Format",
    "Datenstruktur",
    "Übermittlungsart",
    "Frequenz",
]

DATA_COLLECTION_OVERRIDES = {
    "DC_018_WEINBAUKARTEI": {
        "short_title": "Weinbaukartei",
        "long_title": "Sammel-/Fachverfahren Weinbaukartei",
        "description": (
            "Sammelverfahren der Weinbauverwaltung fuer weinbaukarteibezogene Meldungen "
            "und Nachweise. Umfasst u. a. Antrag auf Bescheinigung der Hangneigung, "
            "Bescheinigung zur nutzbaren geografischen Angabe, Erlaeuterungsblatt und "
            "Aenderungsmeldung zur Fortfuehrung der gemeinschaftlichen Weinbaukartei."
        ),
        "data_source": "Rebflaechen; Lage-/Hangneigungsdaten; geografische Angaben; Aenderungsdaten",
        "data_structure": "Sammelverfahren; Formulare; Meldedaten",
        "catalog_level": "Sammelverfahren",
        "parent_collection_title": "",
    },
    "DC_019_WEINBAUKARTEI": {
        "short_title": "Weinbaukartei - geografische Angabe",
        "catalog_level": "Unterformular",
        "parent_collection_title": "Weinbaukartei",
    },
    "DC_020_WEINBAUKARTEI": {
        "short_title": "Weinbaukartei - Erlaeuterungsblatt Aenderungsmeldung",
        "catalog_level": "Unterformular",
        "parent_collection_title": "Weinbaukartei",
    },
    "DC_021_WEINBAUKARTEI": {
        "short_title": "Weinbaukartei - Aenderungsmeldung",
        "catalog_level": "Unterformular",
        "parent_collection_title": "Weinbaukartei",
    },
    "DC_022_WEINMARKTVERWALTUNG": {
        "short_title": "Weinmarktverwaltung",
        "long_title": "Sammel-/Fachverfahren Weinmarktverwaltung",
        "description": (
            "Sammelverfahren der Weinmarktverwaltung fuer weinrechtliche Meldungen und "
            "Formulare, u. a. Lieferantenverzeichnis, Weinerzeugungsmeldung, "
            "Ernte- und Ertragsmeldung sowie Hektarertragsmeldung."
        ),
        "data_source": "Erzeugungs-, Lieferanten-, Ernte- und Ertragsdaten",
        "data_structure": "Sammelverfahren; Formulare; Meldedaten",
        "catalog_level": "Sammelverfahren",
        "parent_collection_title": "",
    },
    "DC_023_WEINMARKTVERWALTUNG": {
        "short_title": "Weinmarktverwaltung - Lieferantenverzeichnis",
        "description": "Lieferantenverzeichnis zur Weinerzeugungsmeldung fuer externe Erzeugnisse.",
        "data_source": "Lieferantendaten; externe Erzeugnisse; Weinerzeugungsmeldung",
        "data_structure": "Formular; Meldedaten",
        "catalog_level": "Unterformular",
        "parent_collection_title": "Weinmarktverwaltung",
    },
    "DC_024_WEINMARKTVERWALTUNG": {
        "short_title": "Weinmarktverwaltung - Weinerzeugungsmeldung",
        "description": "Weinerzeugungsmeldung fuer Erzeugnisse, die nicht in der Ernte- und Erzeugungsmeldung enthalten sind.",
        "data_source": "Erzeugungsdaten; Weinbauerzeugnisse",
        "data_structure": "Formular; Meldedaten",
        "catalog_level": "Unterformular",
        "parent_collection_title": "Weinmarktverwaltung",
    },
    "DC_025_WEINMARKTVERWALTUNG": {
        "short_title": "Weinmarktverwaltung - Erlaeuterungen Ernte-/Erzeugungsmeldung",
        "description": "Erlaeuterungen zur Ernte- und Erzeugungsmeldung mit Rebsortenschluessel.",
        "data_source": "Erntedaten; Erzeugungsdaten; Rebsortenschluessel",
        "data_structure": "Erlaeuterungsdokument",
        "catalog_level": "Unterformular",
        "parent_collection_title": "Weinmarktverwaltung",
    },
    "DC_026_WEINMARKTVERWALTUNG": {
        "short_title": "Weinmarktverwaltung - Ernte- und Ertragsmeldung",
        "description": "Formular zur Ernte- und Ertragsmeldung an die Weinbaukartei fuer das bestimmte Anbaugebiet Baden.",
        "data_source": "Erntedaten; Ertragsdaten; Rebflaechen",
        "data_structure": "Formular; Meldedaten",
        "catalog_level": "Unterformular",
        "parent_collection_title": "Weinmarktverwaltung",
    },
    "DC_027_WEINMARKTVERWALTUNG": {
        "short_title": "Weinmarktverwaltung - Hektarertragsmeldung",
        "description": "Hektarertragsmeldung zur Durchfuehrung der Mengenregulierung.",
        "data_source": "Hektarertrag; Ertragsdaten; Mengenregulierung",
        "data_structure": "Formular; Meldedaten",
        "catalog_level": "Unterformular",
        "parent_collection_title": "Weinmarktverwaltung",
    },
}


def clean(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def split_lines(value: object) -> list[str]:
    text = clean(value)
    if not text:
        return []
    return [part.strip() for part in text.splitlines() if part.strip()]


def search_text(row: pd.Series) -> str:
    parts = [clean(row.get(col)) for col in SEARCH_FIELDS]
    return "\n".join(part for part in parts if part)


def apply_overrides(record: dict) -> dict:
    override = DATA_COLLECTION_OVERRIDES.get(record["data_collection_id"], {})
    for key, value in override.items():
        if value or not record.get(key):
            record[key] = value
    record.setdefault("catalog_level", "")
    record.setdefault("parent_collection_title", "")
    title_parts = [record.get("short_title", ""), record.get("long_title", ""), record.get("description", "")]
    record["display_title"] = next((part for part in title_parts if part), record.get("data_collection_id", ""))
    record["text"] = "\n".join(
        part
        for part in [
            record.get("display_title", ""),
            record.get("short_title", ""),
            record.get("long_title", ""),
            record.get("description", ""),
            record.get("catalog_level", ""),
            record.get("parent_collection_title", ""),
            record.get("foundation_document_title", ""),
            record.get("data_sender", ""),
            record.get("data_receiver", ""),
            record.get("collection_method", ""),
            record.get("data_source", ""),
            record.get("format", ""),
            record.get("data_structure", ""),
            record.get("transmission_method", ""),
            record.get("frequency", ""),
        ]
        if part
    )
    return record


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(METADATA, sheet_name="Tabelle1")
    data_rows = df[df["Data_Collection_ID"].notna()].copy()

    records = []
    for _, row in data_rows.iterrows():
        record = {
            "record_type": "data_collection",
            "object_id": clean(row.get("Data_Collection_ID")),
            "data_collection_id": clean(row.get("Data_Collection_ID")),
            "source_document_id": clean(row.get("Source_Document_ID")),
            "process": clean(row.get("Zugehöriger Prozess")),
            "short_title": clean(row.get("Kurztitel")),
            "long_title": clean(row.get("Langtitel (sofern zutreffend)")),
            "description": clean(row.get("Beschreibung")),
            "foundation_document_title": clean(row.get("Grundlagendokument Titel")),
            "foundation_document_urls": split_lines(row.get("URL Grundlagendokument")),
            "data_sender": clean(row.get("Datengebende Stelle")),
            "data_receiver": clean(row.get("Datenempfangende Stelle")),
            "collection_method": clean(row.get("Erhebungsmethode")),
            "data_source": clean(row.get("Datenquelle")),
            "format": clean(row.get("Format")),
            "data_structure": clean(row.get("Datenstruktur")),
            "transmission_method": clean(row.get("Übermittlungsart")),
            "transmission_urls": split_lines(row.get("URL Übermittlung / Vorlagen / Online-Programm")),
            "frequency": clean(row.get("Frequenz")),
            "text": search_text(row),
        }
        record = apply_overrides(record)
        records.append(record)

    with OUT_JSONL.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    OUT_JSON.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    flat = pd.DataFrame(
        {
            **record,
            "foundation_document_urls": "; ".join(record["foundation_document_urls"]),
            "transmission_urls": "; ".join(record["transmission_urls"]),
        }
        for record in records
    )
    flat.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        flat.to_excel(writer, sheet_name="Data_Collections", index=False)

    by_sender = flat["data_sender"].replace("", "<leer>").value_counts().head(15)
    by_receiver = flat["data_receiver"].replace("", "<leer>").value_counts().head(15)
    by_format = flat["format"].replace("", "<leer>").value_counts()

    lines = [
        "# Data Collections Export Report",
        "",
        f"Input: `{METADATA}`",
        f"Data collections: {len(records)}",
        f"JSONL: `{OUT_JSONL}`",
        f"XLSX: `{OUT_XLSX}`",
        "",
        "## Top Data Senders",
        "",
    ]
    lines.extend(f"- {name}: {count}" for name, count in by_sender.items())
    lines += ["", "## Top Data Receivers", ""]
    lines.extend(f"- {name}: {count}" for name, count in by_receiver.items())
    lines += ["", "## Formats", ""]
    lines.extend(f"- {name}: {count}" for name, count in by_format.items())
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_XLSX)


if __name__ == "__main__":
    main()
