from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
METADATA = BASE / "input" / "source_document_metadata_active.xlsx"
OUTPUT_XLSX = BASE / "output" / "source_document_links.xlsx"
OUTPUT_CSV = BASE / "output" / "source_document_links.csv"
REPORT = BASE / "output" / "source_document_links_report.md"

URL_RE = re.compile(r"https?://\S+")


def is_data_row(row: pd.Series) -> bool:
    values = [row.get("Kurztitel"), row.get("Beschreibung"), row.get("Grundlagendokument Titel")]
    if not any(pd.notna(v) and str(v).strip() for v in values):
        return False
    first = row.get("Zugehöriger Prozess")
    if pd.notna(first) and re.match(r"^\[\d+\]", str(first).strip()):
        return False
    return True


def split_lines(value: object) -> list[str]:
    if pd.isna(value) or not str(value).strip():
        return []
    return [line.strip() for line in str(value).splitlines() if line.strip()]


def split_titles(value: object) -> list[str]:
    if pd.isna(value) or not str(value).strip():
        return []
    text = str(value).strip()
    parts: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts.extend([part.strip() for part in line.split(" | ") if part.strip()])
    return parts


def classify_url(url: str) -> str:
    low = url.lower()
    if low.endswith(".pdf") or ".pdf" in low:
        return "PDF"
    if "gesetze-im-internet" in low or "landesrecht-bw" in low or "eur-lex" in low:
        return "HTML"
    if "fiona" in low or "duengung-bw" in low or "psmdok" in low or "weinbau.lgl-bw" in low:
        return "HTML"
    return "HTML"


def main() -> None:
    df = pd.read_excel(METADATA, sheet_name="Tabelle1")
    rows = []

    for idx, row in df.iterrows():
        if not is_data_row(row):
            continue

        data_collection_id = row.get("Data_Collection_ID")
        source_document_id = row.get("Source_Document_ID")
        kurztitel = row.get("Kurztitel")
        titles = split_titles(row.get("Grundlagendokument Titel"))
        foundation_urls = split_lines(row.get("URL Grundlagendokument"))
        transmission_urls = split_lines(row.get("URL Übermittlung / Vorlagen / Online-Programm"))

        max_len = max(len(titles), len(foundation_urls), 1)
        for pos in range(max_len):
            title = titles[pos] if pos < len(titles) else ""
            url = foundation_urls[pos] if pos < len(foundation_urls) else ""
            rows.append(
                {
                    "Link_ID": f"LINK_{len(rows)+1:04d}",
                    "Data_Collection_ID": data_collection_id,
                    "Source_Document_ID": source_document_id,
                    "Kurztitel": kurztitel,
                    "Link_Type": "Grundlagendokument",
                    "Link_Title": title,
                    "URL": url,
                    "Format": classify_url(url) if url else "",
                    "Excel_Row": idx + 2,
                    "Notes": "Titel/URL positionsbasiert aus Mehrfachzelle extrahiert." if max_len > 1 else "",
                }
            )

        for url in transmission_urls:
            rows.append(
                {
                    "Link_ID": f"LINK_{len(rows)+1:04d}",
                    "Data_Collection_ID": data_collection_id,
                    "Source_Document_ID": source_document_id,
                    "Kurztitel": kurztitel,
                    "Link_Type": "Übermittlung/Vorlage/Online-Programm",
                    "Link_Title": "",
                    "URL": url,
                    "Format": classify_url(url),
                    "Excel_Row": idx + 2,
                    "Notes": "",
                }
            )

    links = pd.DataFrame(rows)
    links.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
        links.to_excel(writer, sheet_name="Source_Document_Links", index=False)

    empty_url = int((links["URL"].fillna("").str.strip() == "").sum())
    by_type = links["Link_Type"].value_counts().to_dict()
    by_format = links["Format"].fillna("").replace("", "<leer>").value_counts().to_dict()

    lines = [
        "# Source Document Links Report",
        "",
        f"Input: `{METADATA}`",
        f"Output XLSX: `{OUTPUT_XLSX}`",
        f"Output CSV: `{OUTPUT_CSV}`",
        "",
        f"- Link-Zeilen erzeugt: {len(links)}",
        f"- Davon ohne URL: {empty_url}",
        "",
        "## Link-Typen",
        "",
    ]
    for key, value in by_type.items():
        lines.append(f"- {key}: {value}")
    lines += ["", "## Formate", ""]
    for key, value in by_format.items():
        lines.append(f"- {key}: {value}")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT_XLSX)


if __name__ == "__main__":
    main()
