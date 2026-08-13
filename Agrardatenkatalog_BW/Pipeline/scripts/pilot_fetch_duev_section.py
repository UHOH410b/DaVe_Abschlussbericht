from __future__ import annotations

import html
import re
import urllib.request
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
METADATA = BASE / "input" / "source_document_metadata_active.xlsx"
OUT_DIR = BASE / "output" / "pilot_duev"
SECTION_URL = "https://www.gesetze-im-internet.de/d_v_2017/__10.html"


def html_to_text(raw_html: str) -> str:
    raw_html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw_html)
    raw_html = re.sub(r"(?i)<br\s*/?>", "\n", raw_html)
    raw_html = re.sub(r"(?i)</(div|p|dd|dt|dl|h1)>", "\n", raw_html)
    text = re.sub(r"(?s)<.*?>", " ", raw_html)
    text = html.unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_norm_text(page_text: str) -> str:
    start = page_text.find("(1) Betriebsinhaber")
    end = page_text.find("zum Seitenanfang")
    if start == -1:
        start = page_text.find("§ 10")
    if end == -1:
        end = len(page_text)
    return page_text[start:end].strip()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(METADATA, sheet_name="Tabelle1")
    row = df[df["Kurztitel"].astype(str).str.contains("Düngeverordnung", case=False, na=False)].iloc[0]

    req = urllib.request.Request(
        SECTION_URL,
        headers={"User-Agent": "Mozilla/5.0 (DaVe research metadata pilot)"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        raw_bytes = response.read()

    try:
        raw = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw = raw_bytes.decode("iso-8859-1", errors="replace")

    text = html_to_text(raw)
    section_text = extract_norm_text(text)

    metadata_lines = [
        "# Pilot Source Metadata",
        "",
        f"Data_Collection_ID: {row.get('Data_Collection_ID')}",
        f"Source_Document_ID: {row.get('Source_Document_ID')}",
        f"Kurztitel: {row.get('Kurztitel')}",
        f"Grundlagendokument: {row.get('Grundlagendokument Titel')}",
        f"URL Grundlagendokument: {row.get('URL Grundlagendokument')}",
        f"Pilot Section URL: {SECTION_URL}",
        f"Datengebende Stelle: {row.get('Datengebende Stelle')}",
        f"Datenempfangende Stelle: {row.get('Datenempfangende Stelle')}",
        f"Frequenz: {row.get('Frequenz')}",
        f"Format: {row.get('Format')}",
    ]

    (OUT_DIR / "source_metadata.md").write_text("\n".join(metadata_lines), encoding="utf-8")
    (OUT_DIR / "duev_10_raw.html").write_text(raw, encoding="utf-8")
    (OUT_DIR / "duev_10_text.txt").write_text(section_text, encoding="utf-8")
    print(OUT_DIR / "duev_10_text.txt")


if __name__ == "__main__":
    main()
