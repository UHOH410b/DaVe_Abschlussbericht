from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
PRIORITY = BASE / "output" / "processing_queue" / "processing_priority.csv"
SCRIPTS = BASE / "scripts"
OUT_DIR = BASE / "output" / "batch_runs"
REPORT = OUT_DIR / "gii_discovery_batch_report.md"


def run_script(script_name: str, *args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script_name), *args],
        cwd=BASE,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch: Gesetze-im-Internet abrufen und Paragraphen entdecken.")
    parser.add_argument("--max-links", type=int, default=5)
    parser.add_argument("--link-id", action="append", help="Optional gezielt Link_ID verarbeiten.")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    priority = pd.read_csv(PRIORITY, encoding="utf-8-sig")
    if args.link_id:
        batch = priority[priority["Link_ID"].astype(str).isin(args.link_id)].copy()
    else:
        batch = priority[
            (priority["Automation_Class"] == "Sehr gut automatisierbar")
            & (priority["Status"].isin(["queued", "document_accessed", "sections_discovered"]))
        ].head(args.max_links).copy()

    lines = [
        "# GII Discovery Batch Report",
        "",
        f"Run: {datetime.now().isoformat(timespec='seconds')}",
        f"Links selected: {len(batch)}",
        "",
    ]
    rows = []
    for _, row in batch.iterrows():
        link_id = str(row["Link_ID"])
        title = str(row.get("Link_Title", ""))
        lines += [f"## {link_id} - {title}", ""]

        access_code, access_out, access_err = run_script("document_access.py", "--link-id", link_id)
        discover_code = None
        discover_out = ""
        discover_err = ""
        if access_code == 0:
            discover_code, discover_out, discover_err = run_script("discover_gii_sections.py", "--link-id", link_id)

        status = "ok" if access_code == 0 and discover_code == 0 else "failed"
        rows.append(
            {
                "Link_ID": link_id,
                "Link_Title": title,
                "Status": status,
                "Document_Access_Returncode": access_code,
                "Document_Access_Output": access_out,
                "Document_Access_Error": access_err,
                "Discover_Returncode": discover_code,
                "Discover_Output": discover_out,
                "Discover_Error": discover_err,
            }
        )
        lines += [
            f"- Status: {status}",
            f"- Document access: {access_code}",
            f"- Discover sections: {discover_code}",
        ]
        if access_err:
            lines += ["", "Document access error:", "", "```text", access_err, "```"]
        if discover_err:
            lines += ["", "Discover error:", "", "```text", discover_err, "```"]
        lines.append("")

    result = pd.DataFrame(rows)
    result.to_csv(OUT_DIR / "gii_discovery_batch.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUT_DIR / "gii_discovery_batch.xlsx", engine="openpyxl") as writer:
        result.to_excel(writer, sheet_name="GII_Discovery_Batch", index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
