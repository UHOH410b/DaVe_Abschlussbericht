from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
ACCESS_ROOT = BASE / "output" / "document_access"
OUT_ROOT = BASE / "output" / "document_sections"

LINK_RE = re.compile(r'<a\s+href="([^"]+)">(.+?)</a>', re.I | re.S)
EMBEDDED_NORM_RE = re.compile(
    r'<div\s+class="jnnorm"\s+id="([^"]+)"\s+title="Einzelnorm".*?<h3>(.*?)</h3>',
    re.I | re.S,
)


def clean_html_text(value: str) -> str:
    value = re.sub(r"(?i)<br\s*/?>", " ", value)
    value = re.sub(r"(?s)<.*?>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def read_metadata(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ": " in line and not line.startswith("#"):
            key, value = line.split(": ", 1)
            data[key.strip()] = value.strip()
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--link-id", required=True)
    args = parser.parse_args()

    access_dir = ACCESS_ROOT / args.link_id
    raw_path = access_dir / "raw.html"
    metadata_path = access_dir / "metadata.md"
    if not raw_path.exists():
        raise SystemExit(f"Missing raw HTML: {raw_path}")
    meta = read_metadata(metadata_path)
    raw = raw_path.read_text(encoding="utf-8", errors="replace")
    base_url = meta.get("Final_URL") or meta.get("URL", "")

    rows = []
    seen = set()
    for href, label_html in LINK_RE.findall(raw):
        label = clean_html_text(label_html)
        if not label.startswith(("§", "Anlage")):
            continue
        if not re.match(r"^(__\w+|anlage_\d+)\.html$", href):
            continue
        url = urljoin(base_url, href)
        if url in seen:
            continue
        seen.add(url)
        section_type = "Paragraph" if label.startswith("§") else "Anlage"
        match = re.match(r"^§\s*([0-9]+[a-zA-Z]?)\s*(.*)$", label)
        section_number = match.group(1) if match else ""
        section_title = match.group(2) if match else label
        rows.append(
            {
                "Document_Section_ID": f"{args.link_id}_SEC_{len(rows)+1:04d}",
                "Link_ID": args.link_id,
                "Data_Collection_ID": meta.get("Data_Collection_ID", ""),
                "Source_Document_ID": meta.get("Source_Document_ID", ""),
                "Section_Type": section_type,
                "Section_Number": section_number,
                "Section_Title": section_title,
                "Source_Reference": label,
                "Section_URL": url,
                "Discovery_Status": "discovered",
            }
        )

    if not rows:
        for anchor, heading_html in EMBEDDED_NORM_RE.findall(raw):
            heading = clean_html_text(heading_html)
            if not heading.startswith(("§", "Art.")):
                continue
            match = re.match(r"^(§|Art\.)\s*([0-9]+[a-zA-Z]?)\s*(.*)$", heading)
            section_number = match.group(2) if match else ""
            section_title = match.group(3) if match else heading
            url = f"{base_url}#{anchor}"
            if url in seen:
                continue
            seen.add(url)
            rows.append(
                {
                    "Document_Section_ID": f"{args.link_id}_SEC_{len(rows)+1:04d}",
                    "Link_ID": args.link_id,
                    "Data_Collection_ID": meta.get("Data_Collection_ID", ""),
                    "Source_Document_ID": meta.get("Source_Document_ID", ""),
                    "Section_Type": "Paragraph" if heading.startswith("§") else "Artikel",
                    "Section_Number": section_number,
                    "Section_Title": section_title,
                    "Source_Reference": heading,
                    "Section_URL": url,
                    "Discovery_Status": "discovered_embedded",
                }
            )

    out_dir = OUT_ROOT / args.link_id
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "document_sections.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(out_dir / "document_sections.xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Document_Sections", index=False)

    report = [
        "# Document Sections Report",
        "",
        f"Link_ID: {args.link_id}",
        f"Sections discovered: {len(df)}",
        f"Output: `{out_dir}`",
        "",
        "## First Sections",
        "",
    ]
    for _, row in df.head(20).iterrows():
        report.append(f"- {row['Document_Section_ID']}: {row['Source_Reference']} -> {row['Section_URL']}")
    (out_dir / "document_sections_report.md").write_text("\n".join(report), encoding="utf-8")
    print(out_dir)


if __name__ == "__main__":
    main()
