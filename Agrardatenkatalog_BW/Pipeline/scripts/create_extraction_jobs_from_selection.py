from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
SELECTION = BASE / "output" / "section_selection" / "relevant_section_candidates.csv"
SCRIPTS = BASE / "scripts"
OUT_DIR = BASE / "output" / "batch_runs"
REPORT = OUT_DIR / "extraction_job_batch_report.md"


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
    parser = argparse.ArgumentParser(description="Aus relevanten Abschnitten Extraktionsjobs erzeugen.")
    parser.add_argument("--max-sections", type=int, default=10)
    parser.add_argument("--min-score", type=int, default=10)
    parser.add_argument("--section-id", action="append")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    selection = pd.read_csv(SELECTION, encoding="utf-8-sig")
    if args.section_id:
        batch = selection[selection["Document_Section_ID"].astype(str).isin(args.section_id)].copy()
    else:
        batch = selection[selection["Relevance_Score"] >= args.min_score].head(args.max_sections).copy()

    rows = []
    lines = [
        "# Extraction Job Batch Report",
        "",
        f"Run: {datetime.now().isoformat(timespec='seconds')}",
        f"Sections selected: {len(batch)}",
        "",
    ]

    for _, row in batch.iterrows():
        section_id = str(row["Document_Section_ID"])
        lines += [f"## {section_id}", ""]
        fetch_code, fetch_out, fetch_err = run_script("fetch_document_section.py", "--section-id", section_id)
        job_code = None
        job_out = ""
        job_err = ""
        if fetch_code == 0:
            job_code, job_out, job_err = run_script("create_extraction_job.py", "--section-id", section_id)
        status = "ok" if fetch_code == 0 and job_code == 0 else "failed"
        rows.append(
            {
                "Document_Section_ID": section_id,
                "Status": status,
                "Relevance_Score": row.get("Relevance_Score"),
                "Source_Reference": row.get("Source_Reference"),
                "Data_Collection_ID": row.get("Data_Collection_ID"),
                "Fetch_Returncode": fetch_code,
                "Fetch_Output": fetch_out,
                "Fetch_Error": fetch_err,
                "Job_Returncode": job_code,
                "Job_Output": job_out,
                "Job_Error": job_err,
            }
        )
        lines += [
            f"- Status: {status}",
            f"- Fetch: {fetch_code}",
            f"- Job: {job_code}",
        ]
        if fetch_err:
            lines += ["", "Fetch error:", "", "```text", fetch_err, "```"]
        if job_err:
            lines += ["", "Job error:", "", "```text", job_err, "```"]
        lines.append("")

    result = pd.DataFrame(rows)
    result.to_csv(OUT_DIR / "extraction_job_batch.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUT_DIR / "extraction_job_batch.xlsx", engine="openpyxl") as writer:
        result.to_excel(writer, sheet_name="Extraction_Job_Batch", index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
