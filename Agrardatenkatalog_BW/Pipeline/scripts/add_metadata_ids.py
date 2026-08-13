from __future__ import annotations

import re
import shutil
import unicodedata
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "input" / "source_document_metadata.xlsx"
OUTPUT = BASE / "input" / "source_document_metadata_with_ids.xlsx"
REPORT = BASE / "output" / "metadata_id_report.md"


def is_data_row(row: pd.Series) -> bool:
    values = [row.get("Kurztitel"), row.get("Beschreibung"), row.get("Grundlagendokument Titel")]
    if not any(pd.notna(v) and str(v).strip() for v in values):
        return False
    first = row.get("Zugehöriger Prozess")
    if pd.notna(first) and re.match(r"^\[\d+\]", str(first).strip()):
        return False
    return True


def slug(value: object, fallback: str) -> str:
    text = fallback if pd.isna(value) or not str(value).strip() else str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.upper()
    repl = {
        "Ä": "AE",
        "Ö": "OE",
        "Ü": "UE",
        "ẞ": "SS",
        "ß": "SS",
    }
    for src, dst in repl.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^A-Z0-9]+", "_", text).strip("_")
    text = re.sub(r"_+", "_", text)
    return text[:42] or fallback


def make_ids(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    data_collection_ids: list[str | None] = []
    source_document_ids: list[str | None] = []

    seen_source: dict[str, int] = {}
    last_kurztitel = ""
    current_process = ""

    for idx, row in out.iterrows():
        if not is_data_row(row):
            data_collection_ids.append(None)
            source_document_ids.append(None)
            continue

        process = row.get("Zugehöriger Prozess")
        if pd.notna(process) and str(process).strip():
            current_process = str(process).strip()

        title = row.get("Kurztitel")
        if pd.notna(title) and str(title).strip():
            last_kurztitel = str(title).strip()

        title_for_id = last_kurztitel or row.get("Beschreibung") or current_process or f"ROW_{idx+2}"
        dcid = f"DC_{idx+2:03d}_{slug(title_for_id, f'ROW_{idx+2}')}"

        source_title = row.get("Grundlagendokument Titel")
        source_url = row.get("URL Grundlagendokument")
        source_basis = source_title if pd.notna(source_title) and str(source_title).strip() else source_url
        base_id = f"SRC_{slug(source_basis, f'ROW_{idx+2}')}"
        count = seen_source.get(base_id, 0) + 1
        seen_source[base_id] = count
        sid = base_id if count == 1 else f"{base_id}_{count:02d}"

        data_collection_ids.append(dcid)
        source_document_ids.append(sid)

    out.insert(0, "Data_Collection_ID", data_collection_ids)
    out.insert(1, "Source_Document_ID", source_document_ids)
    return out


def main() -> None:
    sheets = pd.read_excel(INPUT, sheet_name=None)
    main_sheet = sheets["Tabelle1"]
    enhanced = make_ids(main_sheet)

    with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
        enhanced.to_excel(writer, sheet_name="Tabelle1", index=False)
        for name, sheet_df in sheets.items():
            if name == "Tabelle1":
                continue
            sheet_df.to_excel(writer, sheet_name=name, index=False)

    data_rows = enhanced["Data_Collection_ID"].notna().sum()
    unique_sources = enhanced["Source_Document_ID"].dropna().nunique()
    duplicate_source_titles = (
        enhanced.loc[enhanced["Source_Document_ID"].notna(), "Grundlagendokument Titel"]
        .fillna("")
        .value_counts()
    )
    repeated = duplicate_source_titles[duplicate_source_titles > 1]

    lines = [
        "# Metadata ID Report",
        "",
        f"Input: `{INPUT}`",
        f"Output: `{OUTPUT}`",
        "",
        f"- Datenerhebungs-IDs erzeugt: {data_rows}",
        f"- Source-Dokument-IDs erzeugt: {unique_sources}",
        "",
        "## Hinweise",
        "",
        "- `Data_Collection_ID` bezeichnet die einzelne Datenerhebung im Katalog.",
        "- `Source_Document_ID` bezeichnet das zugrunde gelegte Grundlagendokument bzw. die Dokumentkombination der Zeile.",
        "- Bei mehreren Grundlagendokumenten in einer Zelle ist die ID vorlaeufig zeilenbezogen. Langfristig sollte daraus eine normalisierte `Source_Document_Links`-Tabelle entstehen.",
    ]
    if not repeated.empty:
        lines.extend(["", "## Wiederholt genannte Grundlagendokument-Titel", ""])
        for title, count in repeated.items():
            if str(title).strip():
                lines.append(f"- {count}x: {title[:180]}")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(OUTPUT, BASE / "input" / "source_document_metadata_active.xlsx")
    print(OUTPUT)


if __name__ == "__main__":
    main()
