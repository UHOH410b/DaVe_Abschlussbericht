from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
SCRIPTS = BASE / "scripts"
OUT_DIR = BASE / "output" / "pipeline"
REPORT = OUT_DIR / "local_pipeline_report.md"


STEPS = [
    ("Metadatenkatalog prüfen", "validate_metadata_catalog.py"),
    ("IDs für Metadaten erzeugen", "add_metadata_ids.py"),
    ("Dokumentlinks sammeln", "build_source_document_links.py"),
    ("Verarbeitungs-Warteschlange bauen", "build_processing_queue.py"),
    ("Verarbeitungs-Warteschlange priorisieren", "prioritize_processing_queue.py"),
    ("Master-Katalog initial bauen", "build_master_catalog.py"),
    ("Relationskandidaten berechnen", "compare_requirement_similarity.py"),
    ("Relationen kurz prüfen", "review_relation_candidates.py"),
    ("Kategorien zuweisen", "assign_categories.py"),
    ("Master-Katalog final bauen", "build_master_catalog.py"),
    ("Datenerhebungen exportieren", "export_data_collections.py"),
    ("Vektorindex-Eingaben erzeugen", "build_vector_index_inputs.py"),
    ("Base44-Seed-Daten exportieren", "export_base44_seed_data.py"),
    ("Base44-Importtabellen exportieren", "export_base44_import_tables.py"),
    ("Statische Suchdemo bauen", "build_static_search_demo.py"),
    ("Beispielsuche erzeugen", "query_catalog.py --output-name search_examples"),
]


def run_step(label: str, command: str) -> dict:
    parts = command.split()
    script = SCRIPTS / parts[0]
    args = parts[1:]
    started = datetime.now()
    result = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=BASE,
        text=True,
        capture_output=True,
    )
    finished = datetime.now()
    return {
        "label": label,
        "command": command,
        "returncode": result.returncode,
        "started": started.isoformat(timespec="seconds"),
        "finished": finished.isoformat(timespec="seconds"),
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    failed = False
    for label, command in STEPS:
        if failed:
            results.append(
                {
                    "label": label,
                    "command": command,
                    "returncode": None,
                    "started": "",
                    "finished": "",
                    "stdout": "",
                    "stderr": "Übersprungen, weil ein vorheriger Schritt fehlgeschlagen ist.",
                }
            )
            continue
        result = run_step(label, command)
        results.append(result)
        if result["returncode"] != 0:
            failed = True

    lines = [
        "# Local Pipeline Report",
        "",
        f"Run finished: {datetime.now().isoformat(timespec='seconds')}",
        f"Status: {'failed' if failed else 'ok'}",
        "",
        "## Steps",
        "",
    ]
    for idx, result in enumerate(results, start=1):
        status = "OK" if result["returncode"] == 0 else "FAILED" if result["returncode"] else "SKIPPED"
        lines += [
            f"### {idx}. {result['label']} - {status}",
            "",
            f"- Command: `{result['command']}`",
            f"- Started: {result['started'] or '-'}",
            f"- Finished: {result['finished'] or '-'}",
        ]
        if result["stdout"]:
            lines += ["", "Stdout:", "", "```text", result["stdout"], "```"]
        if result["stderr"]:
            lines += ["", "Stderr:", "", "```text", result["stderr"], "```"]
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
