from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
METADATA = BASE / "input" / "source_document_metadata_active.xlsx"
SECTIONS_ROOT = BASE / "output" / "document_sections"
OUT_DIR = BASE / "output" / "section_selection"
OUT_CSV = OUT_DIR / "relevant_section_candidates.csv"
OUT_XLSX = OUT_DIR / "relevant_section_candidates.xlsx"
REPORT = OUT_DIR / "relevant_section_candidates_report.md"

STOPWORDS = {
    "und", "oder", "der", "die", "das", "den", "dem", "des", "ein", "eine", "einer", "einem",
    "für", "fuer", "zur", "zum", "von", "mit", "im", "in", "am", "an", "auf", "bei", "nach",
    "daten", "antrags", "nachweis", "nachweise", "grundlagendokument", "verordnung", "gesetz",
}


def norm(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).lower()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"\s+", " ", text)


def tokens(value: object) -> list[str]:
    parts = re.split(r"[^a-zA-Z0-9äöüÄÖÜß]+", norm(value))
    return [part for part in parts if len(part) >= 4 and part not in STOPWORDS]


def metadata_terms(row: pd.Series) -> set[str]:
    text = " ".join(
        str(row.get(col, ""))
        for col in [
            "Kurztitel",
            "Langtitel (sofern zutreffend)",
            "Beschreibung",
            "Grundlagendokument Titel",
            "Datengebende Stelle",
            "Datenempfangende Stelle",
            "Frequenz",
        ]
    )
    return set(tokens(text))


def main() -> None:
    parser = argparse.ArgumentParser(description="Relevante Dokumentabschnitte je Datenerhebung vorschlagen.")
    parser.add_argument("--top-per-link", type=int, default=8)
    parser.add_argument("--link-id", action="append")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = pd.read_excel(METADATA, sheet_name="Tabelle1")
    metadata = metadata[metadata["Data_Collection_ID"].notna()].copy()
    meta_by_dc = {str(row["Data_Collection_ID"]): row for _, row in metadata.iterrows()}

    rows = []
    for sections_csv in SECTIONS_ROOT.glob("*/document_sections.csv"):
        link_id = sections_csv.parent.name
        if args.link_id and link_id not in args.link_id:
            continue
        try:
            sections = pd.read_csv(sections_csv, encoding="utf-8-sig")
        except pd.errors.EmptyDataError:
            continue
        if sections.empty:
            continue
        data_collection_id = str(sections.iloc[0].get("Data_Collection_ID", ""))
        meta = meta_by_dc.get(data_collection_id)
        if meta is None:
            continue
        terms = metadata_terms(meta)
        for _, section in sections.iterrows():
            section_text = f"{section.get('Source_Reference', '')} {section.get('Section_Title', '')}"
            section_terms = set(tokens(section_text))
            hits = sorted(terms & section_terms)
            score = len(hits) * 10
            title_norm = norm(section_text)
            # Generische, häufig relevante Prozesswörter etwas höher bewerten.
            for key in ["antrag", "angabe", "aufzeichnung", "meldung", "mitteilung", "nachweis", "kontrolle", "frist"]:
                if key in title_norm:
                    score += 4
            if score <= 0:
                continue
            rows.append(
                {
                    "Link_ID": link_id,
                    "Data_Collection_ID": data_collection_id,
                    "Kurztitel": meta.get("Kurztitel", ""),
                    "Document_Section_ID": section.get("Document_Section_ID", ""),
                    "Source_Reference": section.get("Source_Reference", ""),
                    "Section_Title": section.get("Section_Title", ""),
                    "Section_URL": section.get("Section_URL", ""),
                    "Relevance_Score": score,
                    "Matched_Terms": "; ".join(hits),
                    "Selection_Status": "candidate",
                }
            )

    candidates = pd.DataFrame(rows)
    if not candidates.empty:
        candidates = (
            candidates.sort_values(["Link_ID", "Relevance_Score", "Document_Section_ID"], ascending=[True, False, True])
            .groupby("Link_ID", group_keys=False)
            .head(args.top_per_link)
            .sort_values(["Relevance_Score", "Link_ID"], ascending=[False, True])
        )
    candidates.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        candidates.to_excel(writer, sheet_name="Relevant_Sections", index=False)

    lines = [
        "# Relevant Section Candidates Report",
        "",
        f"Candidates: {len(candidates)}",
        f"Top per link: {args.top_per_link}",
        "",
        "## Top Candidates",
        "",
    ]
    for _, row in candidates.head(30).iterrows():
        lines.append(
            f"- {row['Document_Section_ID']} | {row['Relevance_Score']} | {row['Source_Reference']} | {row['Kurztitel']}"
        )
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_XLSX)


if __name__ == "__main__":
    main()
