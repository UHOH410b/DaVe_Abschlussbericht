from __future__ import annotations

import argparse
import hashlib
import html
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
LINKS = BASE / "output" / "source_document_links.csv"
OUT_ROOT = BASE / "output" / "document_access"


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return value[:80] or "document"


def html_to_text(raw_html: str) -> str:
    raw_html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw_html)
    raw_html = re.sub(r"(?i)<br\s*/?>", "\n", raw_html)
    raw_html = re.sub(r"(?i)</(div|p|dd|dt|dl|li|h1|h2|h3|tr)>", "\n", raw_html)
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
        headers={"User-Agent": "Mozilla/5.0 (DaVe document access pilot)"},
    )
    with urllib.request.urlopen(req, timeout=40) as response:
        data = response.read()
        content_type = response.headers.get("content-type", "")
        final_url = response.geturl()
    return data, content_type, final_url


def choose_extension(url: str, content_type: str, declared_format: str) -> str:
    low_url = url.lower()
    low_ct = content_type.lower()
    if ".pdf" in low_url or "application/pdf" in low_ct or declared_format == "PDF":
        return ".pdf"
    if "text/html" in low_ct or declared_format == "HTML":
        return ".html"
    if "xml" in low_ct or declared_format == "XML":
        return ".xml"
    if "csv" in low_ct or declared_format == "CSV":
        return ".csv"
    return ".bin"


def access_link(link_id: str) -> Path:
    links = pd.read_csv(LINKS, encoding="utf-8-sig")
    matches = links[links["Link_ID"].astype(str) == link_id]
    if matches.empty:
        raise SystemExit(f"Link_ID not found: {link_id}")
    row = matches.iloc[0]
    url = str(row["URL"]).strip()
    data, content_type, final_url = fetch(url)

    digest = hashlib.sha256(data).hexdigest()
    out_dir = OUT_ROOT / link_id
    out_dir.mkdir(parents=True, exist_ok=True)

    declared_format = "" if pd.isna(row.get("Format")) else str(row.get("Format"))
    ext = choose_extension(final_url, content_type, declared_format)
    raw_path = out_dir / f"raw{ext}"
    raw_path.write_bytes(data)

    text_path = out_dir / "text.txt"
    if ext in {".html", ".xml", ".csv", ".bin"}:
        raw_text = decode_bytes(data, content_type)
        text = html_to_text(raw_text) if ext == ".html" else raw_text
        text_path.write_text(text, encoding="utf-8")

    metadata = [
        "# Document Access Metadata",
        "",
        f"Link_ID: {row.get('Link_ID')}",
        f"Data_Collection_ID: {row.get('Data_Collection_ID')}",
        f"Source_Document_ID: {row.get('Source_Document_ID')}",
        f"Kurztitel: {row.get('Kurztitel')}",
        f"Link_Type: {row.get('Link_Type')}",
        f"Link_Title: {row.get('Link_Title')}",
        f"Declared_Format: {declared_format}",
        f"URL: {url}",
        f"Final_URL: {final_url}",
        f"Content_Type: {content_type}",
        f"SHA256: {digest}",
        f"Raw_File: {raw_path.name}",
        f"Text_File: {text_path.name if text_path.exists() else ''}",
    ]
    (out_dir / "metadata.md").write_text("\n".join(metadata), encoding="utf-8")
    return out_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--link-id", required=True)
    args = parser.parse_args()
    print(access_link(args.link_id))


if __name__ == "__main__":
    main()
