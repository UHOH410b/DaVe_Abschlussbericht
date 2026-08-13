from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
MASTER_XLSX = BASE / "output" / "master_catalog" / "master_catalog.xlsx"
OUT_DIR = BASE / "output" / "search_prototype"


SEARCH_COLUMNS = [
    "Atomic_Requirement",
    "Requirement_Type",
    "Actor",
    "Action",
    "Object",
    "Condition",
    "Deadline_or_Frequency",
    "Evidence_Required",
    "Notes",
]

DISPLAY_COLUMNS = [
    "Query",
    "Score",
    "Requirement_ID",
    "Source_Document_ID",
    "Source_Reference",
    "Atomic_Requirement",
    "Requirement_Type",
    "Actor",
    "Action",
    "Object",
    "Condition",
    "Deadline_or_Frequency",
    "Evidence_Required",
    "Primary_Category",
    "Secondary_Categories",
    "Matched_Terms",
]

DEFAULT_QUERIES = [
    "Stickstoff Hektar",
    "Pflanzenschutz Aufbewahrung",
    "Aufzeichnung Frist",
    "maximale Menge pro Hektar",
    "Düngeaufzeichnungen sieben Jahre",
]

QUERY_EXPANSIONS = {
    "maximal": ["hoechstens", "nicht mehr als", "bis zu", "mindestens"],
    "maximale": ["hoechstens", "nicht mehr als", "bis zu", "mindestens"],
    "maximum": ["hoechstens", "nicht mehr als", "bis zu", "mindestens"],
    "menge": ["kilogramm", "kg", "gesamtstickstoff", "phosphat"],
    "stickstoffmenge": ["stickstoff", "gesamtstickstoff", "verfuegbarer stickstoff"],
    "frist": ["tage", "jahre", "spaetestens", "innerhalb", "bis zum"],
    "aufbewahrungsfrist": ["aufbewahrung", "aufbewahren", "sieben jahre"],
    "dokument": ["aufzeichnung", "dokumentation", "nachweis"],
    "dokumente": ["aufzeichnung", "dokumentation", "nachweis"],
}


def normalize(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).lower()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"\s+", " ", text).strip()


def tokenize(query: str) -> list[str]:
    normalized = normalize(query)
    terms = [part for part in re.split(r"[^a-z0-9.]+", normalized) if len(part) >= 2]
    expanded = list(terms)
    for term in terms:
        expanded.extend(QUERY_EXPANSIONS.get(term, []))
    return list(dict.fromkeys(expanded))


def load_catalog() -> tuple[pd.DataFrame, pd.DataFrame]:
    requirements = pd.read_excel(MASTER_XLSX, sheet_name="Atomic_Requirements")
    assignments = pd.read_excel(MASTER_XLSX, sheet_name="Category_Assignments")
    return requirements, assignments


def category_summary(assignments: pd.DataFrame) -> pd.DataFrame:
    if assignments.empty:
        return pd.DataFrame(columns=["Requirement_ID", "Primary_Category", "Secondary_Categories"])

    primary = assignments[assignments["Is_Primary_Category"] == True][
        ["Requirement_ID", "Category_Name"]
    ].rename(columns={"Category_Name": "Primary_Category"})

    secondary = (
        assignments[assignments["Is_Primary_Category"] != True]
        .groupby("Requirement_ID")["Category_Name"]
        .apply(lambda values: "; ".join(sorted(set(str(v) for v in values if pd.notna(v)))))
        .reset_index()
        .rename(columns={"Category_Name": "Secondary_Categories"})
    )

    return primary.merge(secondary, on="Requirement_ID", how="outer")


def score_row(row: pd.Series, terms: list[str], phrase: str) -> tuple[int, list[str]]:
    score = 0
    matched: set[str] = set()

    field_weights = {
        "Atomic_Requirement": 10,
        "Object": 7,
        "Condition": 7,
        "Deadline_or_Frequency": 6,
        "Evidence_Required": 5,
        "Requirement_Type": 4,
        "Action": 4,
        "Actor": 3,
        "Notes": 2,
    }

    combined = normalize(" ".join(str(row.get(col, "")) for col in SEARCH_COLUMNS))
    if phrase and phrase in combined:
        score += 25
        matched.add(phrase)

    for term in terms:
        for col, weight in field_weights.items():
            text = normalize(row.get(col, ""))
            if term in text:
                score += weight
                matched.add(term)
                break

    category_text = normalize(
        f"{row.get('Primary_Category', '')} {row.get('Secondary_Categories', '')}"
    )
    for term in terms:
        if term in category_text:
            score += 4
            matched.add(term)

    return score, sorted(matched)


def run_query(
    requirements: pd.DataFrame,
    assignments: pd.DataFrame,
    query: str,
    top: int,
    category_filter: str | None = None,
) -> pd.DataFrame:
    categories = category_summary(assignments)
    enriched = requirements.merge(categories, on="Requirement_ID", how="left")
    if category_filter:
        wanted = normalize(category_filter)
        category_text = (
            enriched["Primary_Category"].fillna("").astype(str)
            + " "
            + enriched["Secondary_Categories"].fillna("").astype(str)
        ).map(normalize)
        enriched = enriched[category_text.str.contains(wanted, regex=False)]

    terms = tokenize(query)
    phrase = normalize(query)

    rows = []
    for _, row in enriched.iterrows():
        score, matched = score_row(row, terms, phrase)
        if score <= 0:
            continue
        result = row.to_dict()
        result["Query"] = query
        result["Score"] = score
        result["Matched_Terms"] = "; ".join(matched)
        rows.append(result)

    if not rows:
        return pd.DataFrame(columns=DISPLAY_COLUMNS)

    results = pd.DataFrame(rows)
    results = results.sort_values(["Score", "Requirement_ID"], ascending=[False, True])
    for col in DISPLAY_COLUMNS:
        if col not in results.columns:
            results[col] = ""
    return results[DISPLAY_COLUMNS].head(top)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lokaler Such-Prototyp für den Anforderungskatalog.")
    parser.add_argument("--query", help="Suchfrage, z. B. 'Stickstoff Hektar'.")
    parser.add_argument("--category", help="Optionaler Kategorienfilter, z. B. 'Düngung'.")
    parser.add_argument("--top", type=int, default=10, help="Maximale Trefferzahl je Suchfrage.")
    parser.add_argument("--output-name", default="search_results", help="Dateiname ohne Endung.")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_base = re.sub(r"[^A-Za-z0-9_-]+", "_", args.output_name).strip("_") or "search_results"
    out_xlsx = OUT_DIR / f"{out_base}.xlsx"
    out_csv = OUT_DIR / f"{out_base}.csv"
    report = OUT_DIR / f"{out_base}_report.md"

    requirements, assignments = load_catalog()
    queries = [args.query] if args.query else DEFAULT_QUERIES

    all_results = []
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        for query in queries:
            results = run_query(requirements, assignments, query, args.top, args.category)
            all_results.append(results)
            sheet_name = re.sub(r"[^A-Za-z0-9]+", "_", normalize(query)).strip("_")[:31] or "Query"
            results.to_excel(writer, sheet_name=sheet_name, index=False)

    combined = pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
    combined.to_csv(out_csv, index=False, encoding="utf-8-sig")

    lines = [
        "# Search Prototype Report",
        "",
        f"Queries: {len(queries)}",
        f"Category filter: {args.category or 'none'}",
        f"Requirements searched: {len(requirements)}",
        f"Results written: {len(combined)}",
        "",
    ]
    for query in queries:
        count = len(combined[combined["Query"] == query]) if not combined.empty else 0
        lines.append(f"- `{query}`: {count} Treffer")
    lines += [
        "",
        "## Hinweis",
        "",
        "Das ist noch keine Vektorsuche. Es ist ein lokaler Such-Prototyp auf Basis von Textfeldern und Kategorien.",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(out_xlsx)


if __name__ == "__main__":
    main()
