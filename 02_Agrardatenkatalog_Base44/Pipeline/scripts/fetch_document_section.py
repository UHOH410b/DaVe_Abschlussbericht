from __future__ import annotations

import argparse
import hashlib
import html
import re
import urllib.request
from pathlib import Path
from urllib.parse import urldefrag

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
SECTIONS_ROOT = BASE / "output" / "document_sections"
OUT_ROOT = BASE / "output" / "section_texts"


def html_to_text(raw_html: str) -> str:
    raw_html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw_html)
    raw_html = re.sub(r"(?i)<br\s*/?>", "\n", raw_html)
    raw_html = re.sub(r"(?i)</(div|p|dd|dt|dl|li|h1|h2|h3)>", "\n", raw_html)
    raw_html = re.sub(r"(?i)<(dt|li)[^>]*>", "\n", raw_html)
    text = re.sub(r"(?s)<.*?>", " ", raw_html)
    text = html.unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def decode_bytes(data: bytes, content_type: str = "") -> str:
    match = re.search(r"charset=([^;\s]+)", content_type, re.I)
    encodings = []
    if match:
        encodings.append(match.group(1))
    encodings.extend(["utf-8", "iso-8859-1"])
    for enc in encodings:
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def fetch(url: str) -> tuple[bytes, str, str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (DaVe section fetch pilot)"},
    )
    with urllib.request.urlopen(req, timeout=40) as response:
        data = response.read()
        content_type = response.headers.get("content-type", "")
        final_url = response.geturl()
    return data, content_type, final_url


def extract_norm_body(text: str, source_reference: str) -> str:
    marker = source_reference
    pos = text.find(marker)
    if pos != -1:
        text = text[pos:]
    start = re.search(r"\(\d+\)", text)
    if start:
        header = marker if marker in text[: start.start()] else source_reference
        body = text[start.start() :]
        text = f"{header}\n{body}"
    footer = text.find("zum Seitenanfang")
    if footer != -1:
        text = text[:footer]
    return text.strip()


def extract_embedded_norm(raw_html: str, final_url: str) -> str:
    _, fragment = urldefrag(final_url)
    if not fragment:
        return ""
    start_match = re.search(
        rf'<div\s+class="jnnorm"\s+id="{re.escape(fragment)}"\s+title="Einzelnorm"',
        raw_html,
        re.I,
    )
    if not start_match:
        return ""
    start = start_match.start()
    next_match = re.search(r'<div\s+class="jnnorm"\s+id="[^"]+"\s+title="(?:Einzelnorm|Gliederung)"', raw_html[start + 1 :], re.I)
    end = start + 1 + next_match.start() if next_match else len(raw_html)
    return html_to_text(raw_html[start:end])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section-id", required=True)
    args = parser.parse_args()

    link_id = args.section_id.split("_SEC_", 1)[0]
    index_path = SECTIONS_ROOT / link_id / "document_sections.csv"
    if not index_path.exists():
        raise SystemExit(f"Missing section index: {index_path}")
    index = pd.read_csv(index_path, encoding="utf-8-sig")
    match = index[index["Document_Section_ID"].astype(str) == args.section_id]
    if match.empty:
        raise SystemExit(f"Document_Section_ID not found: {args.section_id}")
    row = match.iloc[0]
    url = str(row["Section_URL"])

    data, content_type, final_url = fetch(url)
    raw_text = decode_bytes(data, content_type)
    section_text = extract_embedded_norm(raw_text, final_url)
    if not section_text:
        full_text = html_to_text(raw_text)
        section_text = extract_norm_body(full_text, str(row["Source_Reference"]))

    out_dir = OUT_ROOT / args.section_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "raw.html").write_bytes(data)
    (out_dir / "text.txt").write_text(section_text, encoding="utf-8")

    metadata = [
        "# Section Text Metadata",
        "",
        f"Document_Section_ID: {row.get('Document_Section_ID')}",
        f"Link_ID: {row.get('Link_ID')}",
        f"Data_Collection_ID: {row.get('Data_Collection_ID')}",
        f"Source_Document_ID: {row.get('Source_Document_ID')}",
        f"Source_Reference: {row.get('Source_Reference')}",
        f"Section_URL: {url}",
        f"Final_URL: {final_url}",
        f"Content_Type: {content_type}",
        f"SHA256: {hashlib.sha256(data).hexdigest()}",
        f"Character_Count: {len(section_text)}",
    ]
    (out_dir / "metadata.md").write_text("\n".join(metadata), encoding="utf-8")
    print(out_dir)


if __name__ == "__main__":
    main()
