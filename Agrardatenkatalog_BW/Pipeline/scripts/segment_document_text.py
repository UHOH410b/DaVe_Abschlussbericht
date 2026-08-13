from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
ACCESS_ROOT = BASE / "output" / "document_access"
SEGMENT_ROOT = BASE / "output" / "segments"


SECTION_RE = re.compile(r"(?m)^§\s*(\d+[a-zA-Z]?)\s+(.+?)\s*$")


def read_metadata(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ": " in line and not line.startswith("#"):
            key, value = line.split(": ", 1)
            data[key.strip()] = value.strip()
    return data


def clean_heading_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"\s+Nichtamtliches Inhaltsverzeichnis.*$", "", title)
    return title


def segment_legal_text(text: str) -> list[dict[str, str]]:
    matches = list(SECTION_RE.finditer(text))
    segments: list[dict[str, str]] = []
    seen_keys: set[str] = set()

    for idx, match in enumerate(matches):
        section_no = match.group(1)
        title = clean_heading_title(match.group(2))
        if len(title) > 160:
            continue
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if len(body) < 120:
            continue
        key = f"PARA_{section_no}"
        if key in seen_keys:
            continue
        seen_keys.add(key)
        segments.append(
            {
                "Segment_Local_ID": key,
                "Source_Reference": f"§ {section_no} {title}",
                "Section_Number": section_no,
                "Section_Title": title,
                "Segment_Text": body,
            }
        )
    return segments


def fallback_segments(text: str) -> list[dict[str, str]]:
    return [
        {
            "Segment_Local_ID": "FULL_TEXT",
            "Source_Reference": "Volltext",
            "Section_Number": "",
            "Section_Title": "Volltext",
            "Segment_Text": text.strip(),
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--link-id", required=True)
    args = parser.parse_args()

    access_dir = ACCESS_ROOT / args.link_id
    text_path = access_dir / "text.txt"
    metadata_path = access_dir / "metadata.md"
    if not text_path.exists():
        raise SystemExit(f"Missing text file: {text_path}")
    if not metadata_path.exists():
        raise SystemExit(f"Missing metadata file: {metadata_path}")

    text = text_path.read_text(encoding="utf-8")
    meta = read_metadata(metadata_path)
    segments = segment_legal_text(text) or fallback_segments(text)

    out_dir = SEGMENT_ROOT / args.link_id
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for idx, seg in enumerate(segments, start=1):
        segment_id = f"{args.link_id}_SEG_{idx:04d}_{seg['Segment_Local_ID']}"
        filename = f"{segment_id}.txt"
        (out_dir / filename).write_text(seg["Segment_Text"], encoding="utf-8")
        rows.append(
            {
                "Segment_ID": segment_id,
                "Link_ID": args.link_id,
                "Data_Collection_ID": meta.get("Data_Collection_ID", ""),
                "Source_Document_ID": meta.get("Source_Document_ID", ""),
                "Source_Reference": seg["Source_Reference"],
                "Section_Number": seg["Section_Number"],
                "Section_Title": seg["Section_Title"],
                "Text_File": filename,
                "Character_Count": len(seg["Segment_Text"]),
                "Extraction_Status": "segmented",
            }
        )

    index = pd.DataFrame(rows)
    index.to_csv(out_dir / "segments_index.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(out_dir / "segments_index.xlsx", engine="openpyxl") as writer:
        index.to_excel(writer, sheet_name="Segments", index=False)

    report = [
        "# Segmentation Report",
        "",
        f"Link_ID: {args.link_id}",
        f"Segments: {len(rows)}",
        f"Output: `{out_dir}`",
        "",
        "## First Segments",
        "",
    ]
    for row in rows[:20]:
        report.append(f"- {row['Segment_ID']}: {row['Source_Reference']} ({row['Character_Count']} Zeichen)")
    (out_dir / "segmentation_report.md").write_text("\n".join(report), encoding="utf-8")
    print(out_dir)


if __name__ == "__main__":
    main()
