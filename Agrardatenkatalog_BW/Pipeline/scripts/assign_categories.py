from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
MASTER = BASE / "output" / "master_catalog" / "atomic_requirements_master.csv"
CATEGORY_CATALOG = BASE / "spec" / "category_catalog_v0_1.csv"
OUT_DIR = BASE / "output" / "categories"
OUT_CSV = OUT_DIR / "requirement_category_assignments.csv"
OUT_XLSX = OUT_DIR / "requirement_category_assignments.xlsx"
REPORT = OUT_DIR / "category_assignment_report.md"


def normalize(text: object) -> str:
    if pd.isna(text):
        return ""
    value = str(text).lower()
    value = value.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return value


def keyword_hit(text: str, keyword: str) -> bool:
    key = normalize(keyword).strip()
    if not key:
        return False
    if " " in key or "." in key:
        return key in text
    return re.search(rf"\b{re.escape(key)}", text) is not None


def score_assignment(category_id: str, category_type: str, hits: list[str]) -> int:
    score = len(hits) * 10
    if category_type == "Fachthema":
        score += 8
    elif category_type == "Pflichtmuster":
        score += 6
    elif category_type == "Regellogik":
        score += 4
    elif category_type == "Datenobjekt":
        score += 2

    # Akteur-Kategorien sind nützlich, sollen aber selten die Hauptkategorie sein.
    if category_id == "CAT_BETRIEB":
        score -= 12
    return max(score, 1)


def assign_one(row: pd.Series, categories: pd.DataFrame) -> list[dict]:
    text = normalize(
        " ".join(
            str(row.get(col, ""))
            for col in [
                "Atomic_Requirement",
                "Requirement_Type",
                "Actor",
                "Action",
                "Object",
                "Condition",
                "Deadline_or_Frequency",
                "Evidence_Required",
                "BPMN_Element_Type",
                "Notes",
            ]
        )
    )
    assignments: list[dict] = []
    for _, cat in categories.iterrows():
        keywords = [kw.strip() for kw in str(cat.get("Keywords", "")).split(";") if kw.strip()]
        hits = [kw for kw in keywords if keyword_hit(text, kw)]
        if not hits:
            continue
        category_id = str(cat.get("Category_ID", ""))
        category_type = str(cat.get("Category_Type", ""))
        score = score_assignment(category_id, category_type, hits)
        confidence = "hoch" if len(hits) >= 3 else "mittel" if len(hits) == 2 else "niedrig"
        assignments.append(
            {
                "Requirement_ID": row.get("Requirement_ID"),
                "Source_Document_ID": row.get("Source_Document_ID"),
                "Category_ID": category_id,
                "Category_Name": cat.get("Category_Name"),
                "Category_Type": category_type,
                "Matched_Keywords": "; ".join(hits),
                "Match_Count": len(hits),
                "Assignment_Score": score,
                "Is_Primary_Category": False,
                "Confidence": confidence,
                "Assignment_Status": "candidate",
            }
        )
    if assignments:
        primary = max(
            range(len(assignments)),
            key=lambda idx: (
                assignments[idx]["Assignment_Score"],
                assignments[idx]["Match_Count"],
                assignments[idx]["Category_ID"] != "CAT_BETRIEB",
            ),
        )
        assignments[primary]["Is_Primary_Category"] = True
    return assignments


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    requirements = pd.read_csv(MASTER, encoding="utf-8-sig")
    categories = pd.read_csv(CATEGORY_CATALOG, encoding="utf-8")

    rows = []
    for _, req in requirements.iterrows():
        rows.extend(assign_one(req, categories))

    assignments = pd.DataFrame(rows)
    assignments.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
        assignments.to_excel(writer, sheet_name="Category_Assignments", index=False)
        categories.to_excel(writer, sheet_name="Category_Catalog", index=False)

    lines = [
        "# Category Assignment Report",
        "",
        f"Requirements: {len(requirements)}",
        f"Categories: {len(categories)}",
        f"Assignments: {len(assignments)}",
        "",
        "## Assignments per Category",
        "",
    ]
    if not assignments.empty:
        for name, count in assignments["Category_Name"].value_counts().items():
            lines.append(f"- {name}: {count}")
        uncovered = set(requirements["Requirement_ID"].astype(str)) - set(assignments["Requirement_ID"].astype(str))
    else:
        uncovered = set(requirements["Requirement_ID"].astype(str))
    lines += [
        "",
        f"Requirements without category: {len(uncovered)}",
        "",
        "## Hinweis",
        "",
        "Das ist eine einfache regelbasierte Kategorie-Zuordnung. Sie ist ein Startpunkt für das spätere assign_category-Tool.",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_XLSX)


if __name__ == "__main__":
    main()
