from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
OUTPUT = BASE / "output"
MASTER_DIR = OUTPUT / "master_catalog"
PILOT_REQUIREMENTS = OUTPUT / "pilot_duev" / "atomic_requirements_draft.csv"

MASTER_REQUIREMENTS = MASTER_DIR / "atomic_requirements_master.csv"
MASTER_XLSX = MASTER_DIR / "master_catalog.xlsx"
REPORT = MASTER_DIR / "master_catalog_report.md"
CATEGORY_CATALOG = BASE / "spec" / "category_catalog_v0_1.csv"
CATEGORY_ASSIGNMENTS = OUTPUT / "categories" / "requirement_category_assignments.csv"
RELATION_CANDIDATES = OUTPUT / "relations" / "requirement_relations_candidates.csv"


def load_requirements() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    if PILOT_REQUIREMENTS.exists():
        df = pd.read_csv(PILOT_REQUIREMENTS)
        df["Catalog_Source"] = "pilot_duev"
        frames.append(df)

    jobs_dir = OUTPUT / "extraction_jobs"
    if jobs_dir.exists():
        for csv_path in jobs_dir.glob("*/atomic_requirements_output.csv"):
            df = pd.read_csv(csv_path)
            if df.empty:
                continue
            df["Catalog_Source"] = csv_path.parent.name
            frames.append(df)

    if not frames:
        return pd.DataFrame()
    combined = pd.concat(frames, ignore_index=True)
    combined = combined.drop_duplicates(subset=["Requirement_ID"], keep="last")
    return combined


def derive_data_objects(requirements: pd.DataFrame) -> pd.DataFrame:
    if requirements.empty:
        return pd.DataFrame()
    rows = []
    seen = set()
    for _, row in requirements.iterrows():
        evidence = row.get("Evidence_Required")
        if pd.isna(evidence) or not str(evidence).strip():
            continue
        for item in str(evidence).split("/"):
            name = item.strip()
            if not name:
                continue
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "Data_Object_ID": f"DO_{len(rows)+1:04d}",
                    "Data_Object_Name": name,
                    "Data_Object_Type": "Nachweis / Datenobjekt",
                    "Related_Requirement_IDs": "; ".join(
                        requirements[
                            requirements["Evidence_Required"].fillna("").astype(str).str.contains(name, regex=False)
                        ]["Requirement_ID"].astype(str).tolist()
                    ),
                    "Notes": "Automatisch aus Evidence_Required abgeleitet; fachlich zu prüfen.",
                }
            )
    return pd.DataFrame(rows)


def derive_parameters(requirements: pd.DataFrame) -> pd.DataFrame:
    if requirements.empty:
        return pd.DataFrame()
    rows = []
    patterns = [
        ("14", "Tage", "Aufzeichnungsfrist"),
        ("31. März", "Datum", "Jährliche Zusammenfassungsfrist"),
    ]
    for value, unit, name in patterns:
        matches = requirements[
            requirements.apply(
                lambda r: value in str(r.get("Atomic_Requirement", ""))
                or value in str(r.get("Deadline_or_Frequency", "")),
                axis=1,
            )
        ]
        if not matches.empty:
            rows.append(
                {
                    "Parameter_ID": f"PARAM_{len(rows)+1:04d}",
                    "Parameter_Name": name,
                    "Parameter_Value": value,
                    "Parameter_Unit": unit,
                    "Threshold_Type": "Frist",
                    "Related_Requirement_IDs": "; ".join(matches["Requirement_ID"].astype(str).tolist()),
                    "Notes": "Automatisch erkannt; fachlich zu prüfen.",
                }
            )
    return pd.DataFrame(rows)


def read_optional_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, encoding="utf-8-sig")


def write_master_workbook(
    target: Path,
    requirements: pd.DataFrame,
    data_objects: pd.DataFrame,
    parameters: pd.DataFrame,
    categories: pd.DataFrame,
    category_assignments: pd.DataFrame,
    relation_candidates: pd.DataFrame,
) -> tuple[Path, str]:
    actual_target = target
    note = ""
    try:
        writer = pd.ExcelWriter(actual_target, engine="openpyxl")
    except PermissionError:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        actual_target = target.with_name(f"{target.stem}_{stamp}{target.suffix}")
        note = f"Standarddatei war gesperrt; geschrieben wurde `{actual_target}`."
        writer = pd.ExcelWriter(actual_target, engine="openpyxl")

    with writer:
        requirements.to_excel(writer, sheet_name="Atomic_Requirements", index=False)
        data_objects.to_excel(writer, sheet_name="Data_Object_Catalog", index=False)
        parameters.to_excel(writer, sheet_name="Parameter_Catalog", index=False)
        if not categories.empty:
            categories.to_excel(writer, sheet_name="Category_Catalog", index=False)
        if not category_assignments.empty:
            category_assignments.to_excel(writer, sheet_name="Category_Assignments", index=False)
        if not relation_candidates.empty:
            relation_candidates.to_excel(writer, sheet_name="Relation_Candidates", index=False)

    return actual_target, note


def main() -> None:
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    requirements = load_requirements()
    data_objects = derive_data_objects(requirements)
    parameters = derive_parameters(requirements)
    categories = read_optional_csv(CATEGORY_CATALOG)
    category_assignments = read_optional_csv(CATEGORY_ASSIGNMENTS)
    relation_candidates = read_optional_csv(RELATION_CANDIDATES)

    requirements.to_csv(MASTER_REQUIREMENTS, index=False, encoding="utf-8-sig")
    actual_xlsx, write_note = write_master_workbook(
        MASTER_XLSX,
        requirements,
        data_objects,
        parameters,
        categories,
        category_assignments,
        relation_candidates,
    )

    lines = [
        "# Master Catalog Report",
        "",
        f"Atomic requirements: {len(requirements)}",
        f"Data objects derived: {len(data_objects)}",
        f"Parameters derived: {len(parameters)}",
        f"Categories: {len(categories)}",
        f"Category assignments: {len(category_assignments)}",
        f"Relation candidates: {len(relation_candidates)}",
        "",
        f"CSV: `{MASTER_REQUIREMENTS}`",
        f"XLSX: `{actual_xlsx}`",
        "",
        "## Hinweis",
        "",
        "Dieser Master-Katalog ist ein erster technischer Sammelpunkt. Automatisch abgeleitete Datenobjekte und Parameter sind als Review-Vorschlag zu verstehen.",
    ]
    if write_note:
        lines += ["", "## Schreibhinweis", "", write_note]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(actual_xlsx)


if __name__ == "__main__":
    main()
