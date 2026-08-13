from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
VECTOR_ROOT = BASE / "output" / "vector_index"
SECTION_TEXT_ROOT = BASE / "output" / "section_texts"
REQUIREMENTS_CSV = BASE / "output" / "pilot_duev" / "atomic_requirements_draft.csv"
MASTER_REQUIREMENTS_CSV = BASE / "output" / "master_catalog" / "atomic_requirements_master.csv"
DATA_COLLECTIONS_JSONL = BASE / "output" / "data_collections" / "data_collections.jsonl"
LINKS_CSV = BASE / "output" / "source_document_links.csv"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def clean_value(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value)


KNOWN_SOURCE_ABBREVIATIONS = [
    "VO (EU) 1308/2013",
    "GAPInVeKoSV",
    "PflSchSachkV",
    "PflSchAnwV",
    "PflSchG",
    "QZBW",
    "BioZBW",
    "Bioland",
    "WeinÜV",
    "WeinG",
    "DüV",
]

KNOWN_SOURCE_LONG_NAMES = {
    "VO (EU) 1308/2013": "GMO-Verordnung",
    "DüV": "Düngeverordnung",
    "PflSchG": "Pflanzenschutzgesetz",
    "PflSchAnwV": "Pflanzenschutz-Anwendungsverordnung",
    "PflSchSachkV": "Pflanzenschutz-Sachkundeverordnung",
    "GAPInVeKoSV": "GAPInVeKoS-Verordnung",
    "QZBW": "Qualitätszeichen Baden-Württemberg",
    "BioZBW": "Biozeichen Baden-Württemberg",
    "Bioland": "Bioland-Richtlinien",
    "WeinG": "Weingesetz",
    "WeinÜV": "Wein-Überwachungsverordnung",
}

TITLE_SOURCE_OVERRIDES = [
    ("Verordnung (EU) Nr. 1308/2013", "VO (EU) 1308/2013", "GMO-Verordnung"),
    ("Pflanzenschutzgesetz", "PflSchG", "Pflanzenschutzgesetz"),
    ("Pflanzenschutz-Anwendungsverordnung", "PflSchAnwV", "Pflanzenschutz-Anwendungsverordnung"),
    ("Pflanzenschutz-Sachkundeverordnung", "PflSchSachkV", "Pflanzenschutz-Sachkundeverordnung"),
    ("Düngeverordnung", "DüV", "Düngeverordnung"),
    ("Wein-Überwachungsverordnung", "WeinÜV", "Wein-Überwachungsverordnung"),
    ("Wein-Überwachungsgesetz", "WeinÜG", "Wein-Überwachungsgesetz"),
    ("Weingesetz", "WeinG", "Weingesetz"),
    ("Qualitätszeichen Baden-Württemberg", "QZBW", "Qualitätszeichen Baden-Württemberg"),
    ("Biozeichen Baden-Württemberg", "BioZBW", "Biozeichen Baden-Württemberg"),
    ("Bioland-Richtlinien", "Bioland", "Bioland-Richtlinien"),
    ("Zweite GAP‑RefVO BW", "GAP-RefVO BW", "Zweite GAP-Referenzflächenverordnung Baden-Württemberg"),
    ("SchALVO", "SchALVO", "Schutzgebiets- und Ausgleichs-Verordnung Baden-Württemberg"),
    ("EU-Leitlinien für eine gute Praxis bei freiwilligen Zertifizierungssystemen", "EU-Leitlinien Zertifizierungssysteme", "EU-Leitlinien für freiwillige Zertifizierungssysteme"),
]


def load_source_links() -> pd.DataFrame:
    if not LINKS_CSV.exists():
        return pd.DataFrame()
    return pd.read_csv(LINKS_CSV, encoding="utf-8-sig")


def source_tokens(title: str) -> list[str]:
    tokens: list[str] = []
    ignored = {
        "GAP",
        "PDF",
        "HTML",
        "Gesetz",
        "Verordnung",
        "Durchführung",
        "Rahmen",
        "Gemeinsamen",
        "Agrarpolitik",
        "Direktzahlungen",
        "Landesrecht",
    }
    for marker in ["(", "-", "–"]:
        title = title.replace(marker, " ")
    for raw in title.replace(")", " ").split():
        token = raw.strip(" ,;:")
        if len(token) >= 3 and token not in ignored and any(char.isupper() for char in token):
            tokens.append(token)
    return sorted(tokens, key=len, reverse=True)


def source_abbreviation_from_reference(source_reference: str) -> str:
    for abbreviation in KNOWN_SOURCE_ABBREVIATIONS:
        if abbreviation.lower() in source_reference.lower():
            return abbreviation
    return ""


def source_display_parts(title: str, source_reference: str) -> tuple[str, str, str]:
    abbreviation = source_abbreviation_from_reference(source_reference)
    long_name = title

    for title_fragment, override_abbreviation, override_long_name in TITLE_SOURCE_OVERRIDES:
        if title_fragment.lower() in title.lower():
            abbreviation = abbreviation or override_abbreviation
            long_name = override_long_name
            break

    match = re.search(r"\(([^()]*?)\s+-\s+([^()]*?)\)", title)
    if match and long_name == title:
        long_name = match.group(1).strip()
        abbreviation = abbreviation or match.group(2).strip()
    elif not abbreviation:
        short_match = re.search(r"\b([A-ZÄÖÜ][A-Za-zÄÖÜäöüß]*[A-ZÄÖÜ][A-Za-zÄÖÜäöüß]*)\b", title)
        if short_match:
            abbreviation = short_match.group(1).strip()

    if abbreviation and (not long_name or long_name == title):
        long_name = KNOWN_SOURCE_LONG_NAMES.get(abbreviation, long_name)
    if abbreviation and long_name:
        display = f"{abbreviation} ({long_name})"
    else:
        display = abbreviation or long_name
    return abbreviation, long_name, display


def source_info(row: pd.Series, links: pd.DataFrame) -> dict[str, str]:
    if links.empty:
        return {}
    source_document_id = clean_value(row.get("Source_Document_ID", ""))
    data_collection_id = clean_value(row.get("Data_Collection_ID", ""))
    source_reference = clean_value(row.get("Source_Reference", ""))
    candidates = links[
        (links["Source_Document_ID"].astype(str) == source_document_id)
        & (links["Link_Type"].astype(str) == "Grundlagendokument")
    ]
    if data_collection_id and "Data_Collection_ID" in candidates.columns:
        scoped = candidates[candidates["Data_Collection_ID"].astype(str) == data_collection_id]
        if not scoped.empty:
            candidates = scoped
    if candidates.empty:
        return {}
    if len(candidates) > 1 and source_reference:
        reference_lc = source_reference.lower()
        for _, candidate in candidates.iterrows():
            title = clean_value(candidate.get("Link_Title", ""))
            if any(token.lower() in reference_lc for token in source_tokens(title)):
                return {
                    "source_title": title,
                    "source_url": clean_value(candidate.get("URL", "")),
                    "source_format": clean_value(candidate.get("Format", "")),
                    "source_link_id": clean_value(candidate.get("Link_ID", "")),
                }
    first = candidates.iloc[0]
    return {
        "source_title": clean_value(first.get("Link_Title", "")),
        "source_url": clean_value(first.get("URL", "")),
        "source_format": clean_value(first.get("Format", "")),
        "source_link_id": clean_value(first.get("Link_ID", "")),
    }


def section_entries() -> list[dict]:
    entries: list[dict] = []
    for metadata_path in SECTION_TEXT_ROOT.glob("*/metadata.md"):
        section_dir = metadata_path.parent
        text_path = section_dir / "text.txt"
        if not text_path.exists():
            continue

        meta = {}
        for line in metadata_path.read_text(encoding="utf-8").splitlines():
            if ": " in line and not line.startswith("#"):
                key, value = line.split(": ", 1)
                meta[key.strip()] = value.strip()

        entries.append(
            {
                "object_id": meta.get("Document_Section_ID", section_dir.name),
                "object_type": "document_section",
                "source_document_id": meta.get("Source_Document_ID", ""),
                "data_collection_id": meta.get("Data_Collection_ID", ""),
                "source_reference": meta.get("Source_Reference", ""),
                "text": text_path.read_text(encoding="utf-8"),
                "metadata": meta,
            }
        )
    return entries


def requirement_entries() -> list[dict]:
    source_csv = MASTER_REQUIREMENTS_CSV if MASTER_REQUIREMENTS_CSV.exists() else REQUIREMENTS_CSV
    if not source_csv.exists():
        return []
    df = pd.read_csv(source_csv, encoding="utf-8-sig")
    links = load_source_links()
    entries: list[dict] = []
    for _, row in df.iterrows():
        text = str(row.get("Atomic_Requirement", "")).strip()
        if not text:
            continue
        source = source_info(row, links)
        source_reference = clean_value(row.get("Source_Reference", ""))
        source_title = source.get("source_title", "")
        source_short_title, source_long_name, source_display = source_display_parts(source_title, source_reference)
        source_citation = " | ".join(part for part in [source_display, source_reference] if part)
        entries.append(
            {
                "object_id": clean_value(row.get("Requirement_ID", "")),
                "object_type": "atomic_requirement",
                "source_document_id": clean_value(row.get("Source_Document_ID", "")),
                "data_collection_id": clean_value(row.get("Data_Collection_ID", "")),
                "source_reference": source_reference,
                "source_title": source_title,
                "source_short_title": source_short_title,
                "source_long_name": source_long_name,
                "source_display": source_display,
                "source_url": source.get("source_url", ""),
                "source_format": source.get("source_format", ""),
                "source_link_id": source.get("source_link_id", ""),
                "source_citation": source_citation,
                "original_text": clean_value(row.get("Original_Text", "")),
                "text": text,
                "metadata": {
                    "requirement_type": clean_value(row.get("Requirement_Type", "")),
                    "actor": clean_value(row.get("Actor", "")),
                    "action": clean_value(row.get("Action", "")),
                    "object": clean_value(row.get("Object", "")),
                    "condition": clean_value(row.get("Condition", "")),
                    "deadline_or_frequency": clean_value(row.get("Deadline_or_Frequency", "")),
                    "evidence_required": clean_value(row.get("Evidence_Required", "")),
                    "bpmn_element_type": clean_value(row.get("BPMN_Element_Type", "")),
                    "extraction_status": clean_value(row.get("Extraction_Status", "")),
                    "source_title": source_title,
                    "source_short_title": source_short_title,
                    "source_long_name": source_long_name,
                    "source_display": source_display,
                    "source_url": source.get("source_url", ""),
                    "source_format": source.get("source_format", ""),
                    "source_link_id": source.get("source_link_id", ""),
                    "source_citation": source_citation,
                    "original_text": clean_value(row.get("Original_Text", "")),
                },
            }
        )
    return entries


def data_collection_entries() -> list[dict]:
    if not DATA_COLLECTIONS_JSONL.exists():
        return []
    entries: list[dict] = []
    with DATA_COLLECTIONS_JSONL.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            entries.append(
                {
                    "object_id": clean_value(row.get("object_id", "")),
                    "object_type": "data_collection",
                    "source_document_id": clean_value(row.get("source_document_id", "")),
                    "data_collection_id": clean_value(row.get("data_collection_id", "")),
                    "source_reference": clean_value(row.get("short_title", "")),
                    "display_title": clean_value(row.get("display_title", "")),
                    "text": clean_value(row.get("text", "")),
                    "metadata": {
                        "short_title": clean_value(row.get("short_title", "")),
                        "long_title": clean_value(row.get("long_title", "")),
                        "description": clean_value(row.get("description", "")),
                        "display_title": clean_value(row.get("display_title", "")),
                        "catalog_level": clean_value(row.get("catalog_level", "")),
                        "parent_collection_title": clean_value(row.get("parent_collection_title", "")),
                        "data_sender": clean_value(row.get("data_sender", "")),
                        "data_receiver": clean_value(row.get("data_receiver", "")),
                        "collection_method": clean_value(row.get("collection_method", "")),
                        "data_source": clean_value(row.get("data_source", "")),
                        "data_structure": clean_value(row.get("data_structure", "")),
                        "format": clean_value(row.get("format", "")),
                        "frequency": clean_value(row.get("frequency", "")),
                        "transmission_method": clean_value(row.get("transmission_method", "")),
                        "foundation_document_title": clean_value(row.get("foundation_document_title", "")),
                        "source_url": "; ".join(row.get("transmission_urls", []))
                        if isinstance(row.get("transmission_urls"), list)
                        else clean_value(row.get("source_url", "")),
                    },
                }
            )
    return entries


def document_type_from_title(title: str) -> str:
    text = title.lower()
    if any(term in text for term in ["bioland", "qualitätszeichen", "biozeichen", "ecovin", "ifs", "klimawin"]):
        return "Label/Standard"
    if any(term in text for term in ["vwv", "förder", "beihilfe", "ausgleich", "pheromon"]):
        return "Förderung"
    if any(term in text for term in ["gesetz", "verordnung", "richtlinie", "beschluss", "eu)", "(eu)", "eg)"]):
        return "Fachrecht"
    return "Sonstiges"


def source_document_description(title: str, display: str, document_type: str) -> str:
    text = title.lower()
    if "düngeverordnung" in text:
        return "Regelt die gute fachliche Praxis beim Düngen, insbesondere Düngebedarfsermittlung, Aufbringungsbeschränkungen, Abstände zu Gewässern und Aufzeichnungspflichten."
    if "pflanzenschutzgesetz" in text:
        return "Bundesgesetz zum Schutz der Kulturpflanzen. Enthält grundlegende Vorgaben zur Anwendung von Pflanzenschutzmitteln, Sachkunde, Aufzeichnung, Schutz von Mensch, Tier und Naturhaushalt sowie behördlichen Befugnissen."
    if "pflanzenschutz-anwendungsverordnung" in text or "pflanzenschutzmittel" in text and "anwendungsverbote" in text:
        return "Regelt Anwendungsverbote und Anwendungsbeschränkungen für bestimmte Pflanzenschutzmittel, unter anderem in Schutzgebieten und an Gewässern."
    if "pflanzenschutz-sachkundeverordnung" in text:
        return "Regelt den Nachweis der Sachkunde im Pflanzenschutz, Fortbildungspflichten und Anforderungen an Sachkundenachweise."
    if "gapinvekos" in text:
        return "Regelt das integrierte Verwaltungs- und Kontrollsystem fuer GAP-Zahlungen, insbesondere Sammelantrag, geodatenbasiertes Antragssystem, Antragsangaben, Kontrollen und Nachweise."
    if "gap-direktzahlungen-gesetz" in text:
        return "Regelt die nationalen Grundlagen fuer GAP-Direktzahlungen, darunter Einkommensgrundstuetzung, Umverteilung, Junglandwirte-Einkommensstuetzung, Oeko-Regelungen und gekoppelte Praemien."
    if "gap-direktzahlungen-verordnung" in text:
        return "Konkretisiert Vorgaben zu GAP-Direktzahlungen und Oeko-Regelungen, einschliesslich foerderfaehiger Flaechen, Nutzungsvorgaben und Bedingungen einzelner Praemien."
    if "weingesetz" in text:
        return "Bundesgesetz zum Weinrecht. Regelt unter anderem Anbauregeln, Weinbaukartei, Meldungen, Ernte und Erzeugung, Qualitaetspruefung und Ueberwachung."
    if "wein-überwachungsverordnung" in text or "wein-ueberwachungsverordnung" in text:
        return "Konkretisiert weinrechtliche Ueberwachungs-, Melde- und Dokumentationspflichten, darunter Weinbaukartei, Ernte- und Erzeugungsmeldungen sowie kellerwirtschaftliche Aufzeichnungen."
    if "qualitätszeichen baden-württemberg" in text or "qualitaetszeichen baden-württemberg" in text:
        return "Regelwerk fuer das Qualitaetszeichen Baden-Wuerttemberg. Beschreibt Anforderungen an Erzeugung, Herkunft, Kontrolle und Zeichennutzung."
    if "biozeichen baden-württemberg" in text or "biozeichen baden-wuerttemberg" in text:
        return "Regelwerk fuer das Biozeichen Baden-Wuerttemberg. Beschreibt Anforderungen an oekologische Erzeugung, Kontrolle und Zeichennutzung."
    if "bioland-richtlinien" in text or "bioland" in text:
        return "Privater Bio-Standard des Bioland e.V. mit Anforderungen an Erzeugung, Tierhaltung, Pflanzenbau, Verarbeitung, Kontrolle und Markennutzung."
    if "verordnung (eu) nr. 1308/2013" in text:
        return "EU-Verordnung ueber die gemeinsame Marktorganisation fuer landwirtschaftliche Erzeugnisse. Fuer den Katalog insbesondere relevant fuer weinmarktrechtliche Vorgaben."
    if "verordnung (eu) 2018/848" in text:
        return "EU-Basisverordnung zur oekologischen/biologischen Produktion und Kennzeichnung. Relevant fuer Oeko-Kontrolle, Zertifizierung und Dokumentationspflichten."
    if "zweite gap" in text and "refvo" in text:
        return "Landesrechtliche Regelung zu Referenzflaechen im GAP-Kontext in Baden-Wuerttemberg. Relevant fuer Flaechenbezug, Antragstellung und Verwaltung von Foerderdaten."
    if "schalvo" in text:
        return "Landesrechtliche Schutzgebiets- und Ausgleichsregelung in Baden-Wuerttemberg. Relevant fuer Nutzungsbeschraenkungen, Ausgleichsleistungen und Anforderungen in Wasserschutzgebieten."
    if "satzung" in text and "lieferordnung" in text:
        return "Vertragliche und organisationsbezogene Unterlagen von Genossenschaften oder Erzeugerorganisationen. Relevant fuer Mitgliedschaft, Lieferbeziehungen, Traubenlieferung und betriebliche Nachweise."
    if "freiwilligen zertifizierungssystemen" in text:
        return "EU-Leitlinien zu freiwilligen Zertifizierungssystemen fuer landwirtschaftliche Erzeugnisse und Lebensmittel. Relevant fuer private Standards, Zeichennutzung, Kontrolle und Glaubwuerdigkeit von Zertifizierungssystemen."
    if document_type == "Förderung":
        return f"Foerderrechtliches oder verwaltungsinternes Grundlagendokument. Relevant fuer Antrags-, Nachweis- und Kontrollprozesse im Zusammenhang mit {display}."
    if document_type == "Label/Standard":
        return f"Label- oder Standarddokument. Relevant fuer Zertifizierungs-, Kontroll- und Nachweispflichten im Zusammenhang mit {display}."
    if document_type == "Fachrecht":
        return f"Fachrechtliches Grundlagendokument. Relevant fuer gesetzliche Anforderungen, Nachweise und Kontrollen im Agrardatenkatalog."
    return f"Grundlagendokument im Agrardatenkatalog."


def source_document_full_title(title: str, display: str) -> str:
    clean_title = clean_value(title)
    clean_display = clean_value(display)
    if clean_title and clean_title != clean_display:
        return clean_title
    _, long_name, _ = source_display_parts(clean_title, "")
    if long_name and long_name != clean_display:
        return long_name
    return clean_title or clean_display


def source_document_entries(requirements: list[dict], data_collections: list[dict]) -> list[dict]:
    links = load_source_links()
    if links.empty:
        return []
    foundation = links[links["Link_Type"].astype(str) == "Grundlagendokument"].copy()
    if foundation.empty:
        return []

    req_by_source: dict[str, int] = {}
    for req in requirements:
        source_id = clean_value(req.get("source_document_id", ""))
        if source_id:
            req_by_source[source_id] = req_by_source.get(source_id, 0) + 1

    dc_by_source: dict[str, set[str]] = {}
    for dc in data_collections:
        source_id = clean_value(dc.get("source_document_id", ""))
        dc_id = clean_value(dc.get("data_collection_id", ""))
        if source_id and dc_id:
            dc_by_source.setdefault(source_id, set()).add(dc_id)

    groups: dict[tuple[str, str], list[pd.Series]] = {}
    for _, row in foundation.iterrows():
        title = clean_value(row.get("Link_Title", ""))
        url = clean_value(row.get("URL", ""))
        key = (title.lower(), url.lower())
        groups.setdefault(key, []).append(row)

    entries: list[dict] = []
    for idx, rows in enumerate(groups.values(), start=1):
        row = rows[0]
        link_ids = [clean_value(item.get("Link_ID", "")) for item in rows if clean_value(item.get("Link_ID", ""))]
        source_ids = sorted(
            {clean_value(item.get("Source_Document_ID", "")) for item in rows if clean_value(item.get("Source_Document_ID", ""))}
        )
        data_collection_ids = sorted(
            {clean_value(item.get("Data_Collection_ID", "")) for item in rows if clean_value(item.get("Data_Collection_ID", ""))}
        )
        link_id = link_ids[0] if link_ids else f"SOURCE_{idx:04d}"
        source_id = clean_value(row.get("Source_Document_ID", "")) or link_id
        title = clean_value(row.get("Link_Title", ""))
        url = clean_value(row.get("URL", ""))
        fmt = clean_value(row.get("Format", ""))
        short_title, long_name, display = source_display_parts(title, "")
        full_title = source_document_full_title(title, display)
        object_id = f"SRC_DOC_{link_id}" if link_id else f"SRC_DOC_{idx:04d}"
        requirement_count = sum(req_by_source.get(item, 0) for item in source_ids)
        data_collection_count = len(set(data_collection_ids).union(*(dc_by_source.get(item, set()) for item in source_ids)))
        document_type = document_type_from_title(title)
        description = source_document_description(title, display, document_type)
        text = "\n".join(
            part
            for part in [
                display,
                title,
                description,
                document_type,
                source_id,
                clean_value(row.get("Kurztitel", "")),
                url,
            ]
            if part
        )
        entries.append(
            {
                "object_id": object_id,
                "object_type": "source_document",
                "source_document_id": source_id,
                "data_collection_id": "; ".join(data_collection_ids),
                "source_reference": display,
                "source_title": title,
                "source_short_title": short_title,
                "source_long_name": long_name,
                "source_display": display,
                "source_url": url,
                "source_format": fmt,
                "source_link_id": link_id,
                "source_citation": display,
                "text": text,
                "metadata": {
                    "short_title": display,
                    "long_title": full_title,
                    "display_title": display,
                    "description": description,
                    "document_type": document_type,
                    "requirement_count": str(requirement_count),
                    "data_collection_count": str(data_collection_count),
                    "extraction_status": "teilweise extrahiert" if requirement_count else "nur Metadaten vorhanden",
                    "source_url": url,
                    "source_format": fmt,
                    "source_link_id": link_id,
                    "source_document_id": source_id,
                    "source_document_ids": "; ".join(source_ids),
                    "source_link_ids": "; ".join(link_ids),
                    "data_collection_ids": "; ".join(data_collection_ids),
                },
            }
        )
    return entries


def main() -> None:
    VECTOR_ROOT.mkdir(parents=True, exist_ok=True)
    sections = section_entries()
    requirements = requirement_entries()
    data_collections = data_collection_entries()
    source_documents = source_document_entries(requirements, data_collections)
    search_records = requirements + data_collections + source_documents

    write_jsonl(VECTOR_ROOT / "document_sections.jsonl", sections)
    write_jsonl(VECTOR_ROOT / "atomic_requirements.jsonl", requirements)
    write_jsonl(VECTOR_ROOT / "data_collections.jsonl", data_collections)
    write_jsonl(VECTOR_ROOT / "source_documents.jsonl", source_documents)
    write_jsonl(VECTOR_ROOT / "search_records.jsonl", search_records)

    manifest = {
        "version": "0.1",
        "description": "Vorbereitende JSONL-Dateien fuer spaetere Vektorindizes.",
        "collections": [
            {
                "name": "global_document_sections",
                "file": "document_sections.jsonl",
                "object_type": "document_section",
                "count": len(sections),
            },
            {
                "name": "global_atomic_requirements",
                "file": "atomic_requirements.jsonl",
                "object_type": "atomic_requirement",
                "count": len(requirements),
            },
            {
                "name": "global_data_collections",
                "file": "data_collections.jsonl",
                "object_type": "data_collection",
                "count": len(data_collections),
            },
            {
                "name": "global_source_documents",
                "file": "source_documents.jsonl",
                "object_type": "source_document",
                "count": len(source_documents),
            },
            {
                "name": "global_search_records",
                "file": "search_records.jsonl",
                "object_type": "mixed",
                "count": len(search_records),
            },
        ],
        "embedding_status": "not_created_yet",
        "notes": "Diese Dateien enthalten stabile IDs, Text und Metadaten. Embeddings werden spaeter erzeugt.",
    }
    (VECTOR_ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(VECTOR_ROOT)


if __name__ == "__main__":
    main()
