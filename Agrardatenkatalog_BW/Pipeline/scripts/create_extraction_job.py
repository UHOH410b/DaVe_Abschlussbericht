from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
SECTION_TEXT_ROOT = BASE / "output" / "section_texts"
JOBS_ROOT = BASE / "output" / "extraction_jobs"
PROMPT_TEMPLATE = BASE / "spec" / "prompt_templates_v0_1.md"
ACTIVE_METADATA = BASE / "input" / "source_document_metadata_active.xlsx"


def read_kv_metadata(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ": " in line and not line.startswith("#"):
            key, value = line.split(": ", 1)
            data[key.strip()] = value.strip()
    return data


def extract_template_block(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    start = markdown.find(marker)
    if start == -1:
        raise ValueError(f"Missing template heading: {heading}")
    next_start = markdown.find("\n## ", start + len(marker))
    block = markdown[start: next_start if next_start != -1 else len(markdown)]
    return block.strip()


def fill_extraction_prompt(template_block: str, meta: dict[str, str], section_text: str) -> str:
    catalog_meta = read_catalog_metadata(meta.get("Data_Collection_ID", ""))
    values = {
        "Data_Collection_ID": meta.get("Data_Collection_ID", ""),
        "Source_Document_ID": meta.get("Source_Document_ID", ""),
        "Source_Document_Title": catalog_meta.get("Grundlagendokument Titel") or meta.get("Link_Title", meta.get("Source_Document_ID", "")),
        "Source_Reference": meta.get("Source_Reference", ""),
        "Data_Sender": catalog_meta.get("Datengebende Stelle", ""),
        "Data_Receiver": catalog_meta.get("Datenempfangende Stelle", ""),
        "Frequency": catalog_meta.get("Frequenz", ""),
        "Original_Section_Text": section_text,
    }
    prompt = template_block
    for key, value in values.items():
        prompt = prompt.replace("{{" + key + "}}", value)
    return prompt


def read_catalog_metadata(data_collection_id: str) -> dict[str, str]:
    if not data_collection_id or not ACTIVE_METADATA.exists():
        return {}
    try:
        import pandas as pd

        df = pd.read_excel(ACTIVE_METADATA, sheet_name="Tabelle1")
        match = df[df["Data_Collection_ID"].astype(str) == data_collection_id]
        if match.empty:
            return {}
        row = match.iloc[0]
        return {str(key): "" if pd.isna(value) else str(value) for key, value in row.items()}
    except Exception:
        return {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section-id", required=True)
    args = parser.parse_args()

    section_dir = SECTION_TEXT_ROOT / args.section_id
    metadata_path = section_dir / "metadata.md"
    text_path = section_dir / "text.txt"
    if not metadata_path.exists() or not text_path.exists():
        raise SystemExit(f"Missing section text or metadata for {args.section_id}. Run fetch_document_section.py first.")

    meta = read_kv_metadata(metadata_path)
    section_text = text_path.read_text(encoding="utf-8")
    templates = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    extraction_template = extract_template_block(templates, "Requirement Extraction Agent")
    qa_template = extract_template_block(templates, "QA Agent")

    job_id = f"JOB_{args.section_id}"
    job_dir = JOBS_ROOT / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    prompt = fill_extraction_prompt(extraction_template, meta, section_text)
    (job_dir / "input_section.txt").write_text(section_text, encoding="utf-8")
    (job_dir / "source_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (job_dir / "extraction_prompt.md").write_text(prompt, encoding="utf-8")
    (job_dir / "qa_prompt_template.md").write_text(qa_template, encoding="utf-8")
    (job_dir / "atomic_requirements_output.csv").write_text(
        "Requirement_ID,Data_Collection_ID,Source_Document_ID,Source_Reference,Original_Text,Atomic_Requirement,Requirement_Type,Actor,Action,Object,Condition,Deadline_or_Frequency,Evidence_Required,BPMN_Element_Type,Extraction_Status,Notes\n",
        encoding="utf-8",
    )

    manifest = {
        "job_id": job_id,
        "section_id": args.section_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "created",
        "inputs": {
            "section_text": "input_section.txt",
            "source_metadata": "source_metadata.json",
            "extraction_prompt": "extraction_prompt.md",
            "qa_prompt_template": "qa_prompt_template.md",
        },
        "outputs": {
            "atomic_requirements": "atomic_requirements_output.csv",
            "qa_report": "qa_report.md",
        },
        "next_step": "Run the extraction prompt with an LLM or paste a reviewed CSV into atomic_requirements_output.csv.",
    }
    (job_dir / "job_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(job_dir)


if __name__ == "__main__":
    main()
