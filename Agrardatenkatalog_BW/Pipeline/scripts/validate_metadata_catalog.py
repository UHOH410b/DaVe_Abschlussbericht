from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "input" / "source_document_metadata.xlsx"
OUTPUT = BASE / "output" / "metadata_validation_report.md"

URL_COL = "URL Übermittlung / Vorlagen / Online-Programm"
FORMAT_COL = "Format"


def is_data_row(row: pd.Series) -> bool:
    values = [row.get("Kurztitel"), row.get("Beschreibung"), row.get("Grundlagendokument Titel")]
    if not any(pd.notna(v) and str(v).strip() for v in values):
        return False
    first = row.get("Zugehöriger Prozess")
    if pd.notna(first) and re.match(r"^\[\d+\]", str(first).strip()):
        return False
    return True


def validate_url_cell(value: object) -> list[str]:
    if pd.isna(value) or not str(value).strip():
        return []
    issues: list[str] = []
    for part in str(value).splitlines():
        part = part.strip()
        if not part:
            continue
        if not re.fullmatch(r"https?://\S+", part):
            issues.append(f"not_a_plain_url: {part}")
        if "fionaschulung" in part.lower():
            issues.append(f"irrelevant_training_url: {part}")
    return issues


def main() -> None:
    df = pd.read_excel(INPUT, sheet_name="Tabelle1")
    data_mask = df.apply(is_data_row, axis=1)
    data = df.loc[data_mask].copy()

    url_issues = []
    format_issues = []
    missing_foundation_url = []

    for idx, row in data.iterrows():
        excel_row = idx + 2
        title = "" if pd.isna(row.get("Kurztitel")) else str(row.get("Kurztitel"))

        for issue in validate_url_cell(row.get(URL_COL)):
            url_issues.append((excel_row, title, issue))

        fmt = "" if pd.isna(row.get(FORMAT_COL)) else str(row.get(FORMAT_COL)).strip()
        if not fmt or "Zu erheben" in fmt:
            format_issues.append((excel_row, title, fmt or "<leer>"))

        foundation_url = row.get("URL Grundlagendokument")
        if pd.isna(foundation_url) or not str(foundation_url).strip():
            missing_foundation_url.append((excel_row, title))

    lines = [
        "# Metadata Validation Report",
        "",
        f"Input: `{INPUT}`",
        f"Datenerhebungszeilen erkannt: {len(data)}",
        "",
        "## Checks",
        "",
        f"- URL-Spalte nur URLs/leer: {'OK' if not url_issues else 'Pruefen'}",
        f"- Format-Spalte ohne Platzhalter: {'OK' if not format_issues else 'Pruefen'}",
        f"- Grundlagendokument-URLs vorhanden: {'OK' if not missing_foundation_url else 'Pruefen'}",
        "",
    ]

    if url_issues:
        lines += ["## URL Issues", ""]
        for row, title, issue in url_issues:
            lines.append(f"- Excel-Zeile {row}: {title} -> {issue}")
        lines.append("")

    if format_issues:
        lines += ["## Format Issues", ""]
        for row, title, fmt in format_issues:
            lines.append(f"- Excel-Zeile {row}: {title} -> {fmt}")
        lines.append("")

    if missing_foundation_url:
        lines += ["## Fehlende URL Grundlagendokument", ""]
        for row, title in missing_foundation_url:
            lines.append(f"- Excel-Zeile {row}: {title}")
        lines.append("")

    lines += [
        "## Naechste empfohlene Strukturpflege",
        "",
        "- Stabile `Source_Document_ID` je Datenerhebung bzw. Grundlagendokument ergaenzen.",
        "- Leere `Kurztitel`-Folgezeilen fachlich pruefen: Entweder eigene Datenerhebung benennen oder als Unterobjekt der vorherigen Zeile markieren.",
        "- Bei mehreren URLs in einer Zelle langfristig eine eigene Link-Tabelle `Source_Document_Links` anlegen.",
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
