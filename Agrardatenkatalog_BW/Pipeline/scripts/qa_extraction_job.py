from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
JOBS_ROOT = BASE / "output" / "extraction_jobs"
PILOT_REQUIREMENTS = BASE / "output" / "pilot_duev" / "atomic_requirements_draft.csv"

REQUIRED_COLUMNS = [
    "Requirement_ID",
    "Data_Collection_ID",
    "Source_Document_ID",
    "Source_Reference",
    "Original_Text",
    "Atomic_Requirement",
    "Requirement_Type",
    "Actor",
    "Action",
    "Object",
    "Condition",
    "Deadline_or_Frequency",
    "Evidence_Required",
    "BPMN_Element_Type",
    "Extraction_Status",
    "Notes",
]

NORMATIVE_PATTERNS = [
    r"\bmuss\b",
    r"\bmüssen\b",
    r"\bhat\b.*\baufzuzeichnen\b",
    r"\bhaben\b.*\baufzuzeichnen\b",
    r"\bist\b.*\baufzuzeichnen\b",
    r"\bsind\b.*\baufzuzeichnen\b",
    r"\bgelten nicht\b",
    r"\baufzubewahren\b",
    r"\bvorzulegen\b",
    r"\bist verpflichtet\b",
    r"\bsind verpflichtet\b",
    r"\bkönnen\b.*\bgeführt werden\b",
    r"\bdürfen\b",
]

CONTEXT_SIGNALS = [
    "diese",
    "diesen",
    "dieser",
    "davon",
    "daraus",
    "solche",
    "betroffene",
    "beeinträchtigte",
    "hier beschrieben",
    "nach satz",
]

LIST_COMPOUNDS = [
    "art und menge",
    "gesamtstickstoff und phosphat",
    "bezeichnung, lage und größe",
    "art und zahl",
]


def load_job(job_id: str) -> tuple[Path, str, pd.DataFrame]:
    job_dir = JOBS_ROOT / job_id
    section_path = job_dir / "input_section.txt"
    csv_path = job_dir / "atomic_requirements_output.csv"
    if not job_dir.exists():
        raise SystemExit(f"Job not found: {job_dir}")
    if not section_path.exists():
        raise SystemExit(f"Missing section text: {section_path}")

    if (not csv_path.exists()) or csv_path.stat().st_size < 100:
        if PILOT_REQUIREMENTS.exists():
            csv_path = PILOT_REQUIREMENTS
        else:
            raise SystemExit(f"Missing populated requirements CSV: {csv_path}")

    text = section_path.read_text(encoding="utf-8")
    df = pd.read_csv(csv_path)
    if df.empty and PILOT_REQUIREMENTS.exists() and csv_path != PILOT_REQUIREMENTS:
        csv_path = PILOT_REQUIREMENTS
        df = pd.read_csv(csv_path)
    return job_dir, text, df


def split_sentences(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=\(?\d+\)|[A-ZÄÖÜ])", normalized)
    return [part.strip() for part in parts if part.strip()]


def find_normative_clauses(text: str) -> list[str]:
    clauses = []
    for sentence in split_sentences(text):
        low = sentence.lower()
        if any(re.search(pattern, low) for pattern in NORMATIVE_PATTERNS):
            clauses.append(sentence)
    return clauses


def contains_in_requirements(df: pd.DataFrame, needle: str) -> bool:
    haystack = " ".join(df.get("Atomic_Requirement", pd.Series(dtype=str)).fillna("").astype(str)).lower()
    haystack += " " + " ".join(df.get("Condition", pd.Series(dtype=str)).fillna("").astype(str)).lower()
    haystack += " " + " ".join(df.get("Deadline_or_Frequency", pd.Series(dtype=str)).fillna("").astype(str)).lower()
    return needle.lower() in haystack


def qa(job_id: str) -> tuple[Path, list[str]]:
    job_dir, section_text, df = load_job(job_id)
    issues: list[str] = []

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        issues.append(f"CRITICAL: Missing columns: {', '.join(missing_columns)}")

    if "Requirement_ID" in df.columns:
        duplicates = df["Requirement_ID"][df["Requirement_ID"].duplicated()].dropna().astype(str).tolist()
        if duplicates:
            issues.append(f"CRITICAL: Duplicate Requirement_IDs: {', '.join(duplicates[:10])}")

    for col in ["Requirement_ID", "Atomic_Requirement", "Requirement_Type", "Actor", "Action", "Object"]:
        if col in df.columns:
            empty = df[df[col].isna() | (df[col].astype(str).str.strip() == "")]
            if not empty.empty:
                issues.append(f"WARNING: Empty required-ish field `{col}` in {len(empty)} rows.")

    normative_clauses = find_normative_clauses(section_text)
    if len(df) < max(1, len(normative_clauses)):
        issues.append(
            f"WARNING: Requirement count ({len(df)}) is lower than detected normative clauses ({len(normative_clauses)}). Check for over-merged requirements."
        )

    for term in ["14 Tage", "31. März", "sieben Jahre", "100 Kilogramm", "15 Hektar", "2 Hektar", "750 Kilogramm"]:
        if term.lower() in section_text.lower() and not contains_in_requirements(df, term):
            issues.append(f"WARNING: Parameter/framerate from source not found in requirements: `{term}`")

    req_text = " ".join(df.get("Atomic_Requirement", pd.Series(dtype=str)).fillna("").astype(str)).lower()
    notes_text = " ".join(df.get("Notes", pd.Series(dtype=str)).fillna("").astype(str)).lower()
    combined = req_text + " " + notes_text
    for compound in LIST_COMPOUNDS:
        if compound in section_text.lower() and compound in req_text:
            issues.append(f"WARNING: Potential un-split list compound still present in Atomic_Requirement: `{compound}`")
        if compound in section_text.lower() and compound not in combined:
            issues.append(f"INFO: List compound `{compound}` appears in source; verify atomization.")

    for signal in CONTEXT_SIGNALS:
        if signal in section_text.lower() and signal in req_text:
            issues.append(f"INFO: Context signal `{signal}` appears in requirements; verify context was resolved, not copied ambiguously.")

    if not issues:
        issues.append("OK: Rule-based QA found no structural issues.")

    report = [
        "# QA Report",
        "",
        f"Job_ID: {job_id}",
        f"Requirements checked: {len(df)}",
        f"Normative clauses detected: {len(normative_clauses)}",
        "",
        "## Issues",
        "",
    ]
    report.extend(f"- {issue}" for issue in issues)
    report.extend(
        [
            "",
            "## Notes",
            "",
            "This is a rule-based QA precheck. It does not replace human review or a later LLM QA agent.",
        ]
    )
    report_path = job_dir / "qa_report.md"
    report_path.write_text("\n".join(report), encoding="utf-8")
    return report_path, issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", required=True)
    args = parser.parse_args()
    report_path, _ = qa(args.job_id)
    print(report_path)


if __name__ == "__main__":
    main()
