from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
LINKS = BASE / "output" / "source_document_links.csv"
DOCUMENT_ACCESS = BASE / "output" / "document_access"
DOCUMENT_SECTIONS = BASE / "output" / "document_sections"
SECTION_TEXTS = BASE / "output" / "section_texts"
EXTRACTION_JOBS = BASE / "output" / "extraction_jobs"
OUT_DIR = BASE / "output" / "processing_queue"
OUT_CSV = OUT_DIR / "processing_queue.csv"
OUT_XLSX = OUT_DIR / "processing_queue.xlsx"
REPORT = OUT_DIR / "processing_queue_report.md"


def exists_dir(path: Path) -> bool:
    return path.exists() and path.is_dir()


def count_sections(link_id: str) -> int:
    csv_path = DOCUMENT_SECTIONS / link_id / "document_sections.csv"
    if not csv_path.exists():
        return 0
    try:
        return len(pd.read_csv(csv_path, encoding="utf-8-sig"))
    except Exception:
        return 0


def count_section_texts(link_id: str) -> int:
    prefix = f"{link_id}_SEC_"
    if not SECTION_TEXTS.exists():
        return 0
    return sum(1 for path in SECTION_TEXTS.iterdir() if path.is_dir() and path.name.startswith(prefix))


def count_extraction_jobs(link_id: str) -> int:
    prefix = f"JOB_{link_id}_SEC_"
    if not EXTRACTION_JOBS.exists():
        return 0
    return sum(1 for path in EXTRACTION_JOBS.iterdir() if path.is_dir() and path.name.startswith(prefix))


def has_completed_output(link_id: str) -> bool:
    prefix = f"JOB_{link_id}_SEC_"
    if not EXTRACTION_JOBS.exists():
        return False
    for path in EXTRACTION_JOBS.iterdir():
        if not path.is_dir() or not path.name.startswith(prefix):
            continue
        output = path / "atomic_requirements_output.csv"
        if output.exists() and output.stat().st_size > 250:
            return True
    return False


def infer_status(row: pd.Series) -> tuple[str, str]:
    link_id = str(row["Link_ID"])
    url = "" if pd.isna(row.get("URL")) else str(row.get("URL")).strip()
    fmt = "" if pd.isna(row.get("Format")) else str(row.get("Format")).strip().upper()
    link_type = "" if pd.isna(row.get("Link_Type")) else str(row.get("Link_Type")).strip()

    if not url:
        return "blocked_no_url", "Keine URL vorhanden."
    if link_type != "Grundlagendokument":
        return "not_in_scope_transmission_link", "Übermittlungs-/Vorlagenlink; nicht primär für Rechtstext-Extraktion."
    if fmt not in {"HTML", "PDF"}:
        return "blocked_unknown_format", f"Format `{fmt}` braucht eigene Verarbeitung."

    sections = count_sections(link_id)
    section_texts = count_section_texts(link_id)
    jobs = count_extraction_jobs(link_id)

    if has_completed_output(link_id):
        return "extraction_output_present", "Mindestens ein Extraktionsergebnis vorhanden."
    if jobs:
        return "extraction_job_created", f"{jobs} Extraktionsjob(s) angelegt."
    if section_texts:
        return "section_text_fetched", f"{section_texts} Abschnittstext(e) geladen."
    if sections:
        return "sections_discovered", f"{sections} Abschnitt(e) entdeckt."
    if exists_dir(DOCUMENT_ACCESS / link_id):
        return "document_accessed", "Dokument wurde abgerufen."
    return "queued", "Bereit für Dokumentabruf."


def next_action(status: str, fmt: str, url: str) -> str:
    if status == "queued":
        return "document_access.py ausführen"
    if status == "document_accessed" and "gesetze-im-internet" in url:
        return "discover_gii_sections.py ausführen"
    if status == "document_accessed" and fmt == "PDF":
        return "PDF-Segmentierung ergänzen"
    if status == "document_accessed":
        return "generische HTML-Segmentierung ergänzen"
    if status == "sections_discovered":
        return "relevante Document_Section_ID auswählen und fetch_document_section.py ausführen"
    if status == "section_text_fetched":
        return "create_extraction_job.py ausführen"
    if status == "extraction_job_created":
        return "LLM-Extraktion / Review durchführen"
    if status == "extraction_output_present":
        return "QA und Master-Katalog aktualisieren"
    return "prüfen"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    links = pd.read_csv(LINKS, encoding="utf-8-sig")
    rows = []

    for _, row in links.iterrows():
        status, note = infer_status(row)
        url = "" if pd.isna(row.get("URL")) else str(row.get("URL")).strip()
        fmt = "" if pd.isna(row.get("Format")) else str(row.get("Format")).strip().upper()
        rows.append(
            {
                "Queue_ID": f"QUEUE_{len(rows)+1:04d}",
                "Link_ID": row.get("Link_ID"),
                "Data_Collection_ID": row.get("Data_Collection_ID"),
                "Source_Document_ID": row.get("Source_Document_ID"),
                "Kurztitel": row.get("Kurztitel"),
                "Link_Type": row.get("Link_Type"),
                "Link_Title": row.get("Link_Title"),
                "URL": url,
                "Format": fmt,
                "Status": status,
                "Next_Action": next_action(status, fmt, url),
                "Sections_Discovered": count_sections(str(row.get("Link_ID"))),
                "Section_Texts_Fetched": count_section_texts(str(row.get("Link_ID"))),
                "Extraction_Jobs": count_extraction_jobs(str(row.get("Link_ID"))),
                "Notes": note,
            }
        )

    queue = pd.DataFrame(rows)
    queue.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        queue.to_excel(writer, sheet_name="Processing_Queue", index=False)

    lines = [
        "# Processing Queue Report",
        "",
        f"Queue rows: {len(queue)}",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in queue["Status"].value_counts().items():
        lines.append(f"- {status}: {count}")
    lines += ["", "## Next 20 Queued Foundation Documents", ""]
    todo = queue[(queue["Status"] == "queued") & (queue["Link_Type"] == "Grundlagendokument")].head(20)
    for _, row in todo.iterrows():
        lines.append(f"- {row['Queue_ID']} / {row['Link_ID']}: {row['Link_Title']}")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_XLSX)


if __name__ == "__main__":
    main()
