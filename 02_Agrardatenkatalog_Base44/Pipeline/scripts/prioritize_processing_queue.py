from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
QUEUE_CSV = BASE / "output" / "processing_queue" / "processing_queue.csv"
OUT_DIR = BASE / "output" / "processing_queue"
OUT_CSV = OUT_DIR / "processing_priority.csv"
OUT_XLSX = OUT_DIR / "processing_priority.xlsx"
REPORT = OUT_DIR / "processing_priority_report.md"


def domain(url: object) -> str:
    if pd.isna(url):
        return ""
    return urlparse(str(url)).netloc.lower()


def priority(row: pd.Series) -> tuple[int, str, str]:
    status = str(row.get("Status", ""))
    link_type = str(row.get("Link_Type", ""))
    fmt = str(row.get("Format", "")).upper()
    url = str(row.get("URL", ""))
    dom = domain(url)

    if link_type != "Grundlagendokument":
        return 900, "Nicht Grundlagendokument", "Übermittlungs-/Vorlagenlinks später."
    if status in {"extraction_output_present", "extraction_job_created"}:
        return 20, "Bereits begonnen", "Vorhandene Extraktionsjobs zuerst konsolidieren."
    if status != "queued":
        return 100, "In Bearbeitung", "Nächsten Statusschritt ausführen."
    if "gesetze-im-internet.de" in dom and fmt == "HTML":
        return 10, "Sehr gut automatisierbar", "Gesetze-im-Internet HTML mit Paragraphenstruktur."
    if "landesrecht-bw.de" in dom and fmt == "HTML":
        return 30, "Gut automatisierbar", "Landesrecht HTML; eigene Segmentierung nötig."
    if "eur-lex.europa.eu" in dom and fmt == "HTML":
        return 40, "Gut automatisierbar", "EUR-Lex HTML; eigene Segmentierung nötig."
    if fmt == "PDF":
        return 60, "PDF", "PDF-Extraktion/Sichtung nötig."
    if fmt == "HTML":
        return 70, "Generische Website", "Manuelle oder domainspezifische Segmentierung nötig."
    return 80, "Unklar", "Format oder URL prüfen."


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    queue = pd.read_csv(QUEUE_CSV, encoding="utf-8-sig")
    queue["Domain"] = queue["URL"].map(domain)
    classifications = queue.apply(priority, axis=1)
    queue["Processing_Priority"] = [item[0] for item in classifications]
    queue["Automation_Class"] = [item[1] for item in classifications]
    queue["Automation_Reason"] = [item[2] for item in classifications]
    queue = queue.sort_values(["Processing_Priority", "Link_ID"])

    queue.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        queue.to_excel(writer, sheet_name="Processing_Priority", index=False)

    lines = [
        "# Processing Priority Report",
        "",
        f"Rows: {len(queue)}",
        "",
        "## Automation Classes",
        "",
    ]
    for name, count in queue["Automation_Class"].value_counts().items():
        lines.append(f"- {name}: {count}")
    lines += ["", "## Top 30", ""]
    for _, row in queue.head(30).iterrows():
        lines.append(
            f"- {row['Link_ID']} | P{row['Processing_Priority']} | {row['Automation_Class']} | {row['Link_Title']}"
        )
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_XLSX)


if __name__ == "__main__":
    main()
