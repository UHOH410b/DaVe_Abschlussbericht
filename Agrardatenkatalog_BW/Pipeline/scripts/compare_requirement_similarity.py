from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
MASTER = BASE / "output" / "master_catalog" / "atomic_requirements_master.csv"
OUT_DIR = BASE / "output" / "relations"
OUT_CSV = OUT_DIR / "requirement_relations_candidates.csv"
OUT_XLSX = OUT_DIR / "requirement_relations_candidates.xlsx"
REPORT = OUT_DIR / "requirement_relations_report.md"

STOPWORDS = {
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einer", "eines",
    "und", "oder", "nach", "bei", "mit", "für", "von", "zur", "zum", "zu",
    "auf", "im", "in", "am", "an", "ist", "sind", "muss", "müssen", "hat",
    "haben", "werden", "wird", "betriebsinhaber", "betrieb", "leiter",
}

DOMAIN_TERMS = {
    "düng": "Düngung",
    "duenge": "Düngung",
    "dunge": "Düngung",
    "naehrstoff": "Nährstoffe",
    "stickstoff": "Stickstoff",
    "phosphat": "Phosphat",
    "pflanzenschutz": "Pflanzenschutz",
    "pflanzenschutzmittel": "Pflanzenschutz",
    "weide": "Weidehaltung",
    "flaeche": "Fläche",
    "schlag": "Fläche",
    "aufzeichnung": "Aufzeichnung",
    "aufzeichnungen": "Aufzeichnung",
    "aufbewahrung": "Aufbewahrung",
    "aufbewahr": "Aufbewahrung",
}


def tokenize(text: object) -> list[str]:
    if pd.isna(text):
        return []
    value = str(text).lower()
    value = value.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    tokens = re.findall(r"[a-z0-9]{3,}", value)
    return [token for token in tokens if token not in STOPWORDS]


def vectorize(text: object) -> Counter:
    return Counter(tokenize(text))


def domain_tags(*values: object) -> set[str]:
    text = " ".join("" if pd.isna(value) else str(value).lower() for value in values)
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    tags = set()
    for needle, tag in DOMAIN_TERMS.items():
        if needle in text:
            tags.add(tag)
    return tags


def main_object_token(value: object) -> str:
    tokens = [t for t in tokenize(value) if t not in {"aufzeichnungen", "aufzeichnung", "pflicht", "frist"}]
    return tokens[0] if tokens else ""


def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def relation_type(score: float, shared_keywords: set[str]) -> str:
    if score >= 0.75:
        return "ähnlich"
    if score >= 0.45:
        return "teilweise überlappend"
    if {"aufzeichnen", "aufzeichnungen"} & shared_keywords:
        return "thematisch verwandt"
    return "schwach verwandt"


def context_relation(base_relation: str, left: pd.Series, right: pd.Series, shared_keywords: set[str], score: float) -> tuple[str, str, str]:
    tags_a = domain_tags(left.get("Atomic_Requirement"), left.get("Object"), left.get("Condition"), left.get("Evidence_Required"))
    tags_b = domain_tags(right.get("Atomic_Requirement"), right.get("Object"), right.get("Condition"), right.get("Evidence_Required"))
    shared_tags = tags_a & tags_b
    object_a = main_object_token(left.get("Object"))
    object_b = main_object_token(right.get("Object"))
    same_object = bool(object_a and object_b and object_a == object_b)
    action_a = str(left.get("Action", "")).lower()
    action_b = str(right.get("Action", "")).lower()
    type_a = str(left.get("Requirement_Type", "")).lower()
    type_b = str(right.get("Requirement_Type", "")).lower()
    same_action = bool(action_a and action_b and action_a == action_b)
    same_type_family = any(fam in type_a and fam in type_b for fam in ["dokumentation", "frist", "aufbewahrung", "ausnahme", "pflicht", "erlaubnis"])

    only_record_overlap = shared_tags and shared_tags <= {"Aufzeichnung", "Aufbewahrung"}
    different_sources = left.get("Source_Document_ID") != right.get("Source_Document_ID")

    if "Aufbewahrung" in (tags_a | tags_b) or "aufbewahren" in shared_keywords or only_record_overlap:
        if not same_object and object_a and object_b:
            return (
                "gleiches Pflichtmuster, anderes Objekt",
                "; ".join(sorted(shared_tags)) or "Aufbewahrung/Aufzeichnungen",
                f"Unterschiedliche Objekte: {left.get('Object')} vs. {right.get('Object')}",
            )
        if different_sources and only_record_overlap:
            return (
                "gleiches Pflichtmuster, anderer Fachkontext",
                "; ".join(sorted(shared_tags)),
                f"Gleiches Muster, aber andere Rechts-/Fachquelle: {left.get('Object')} vs. {right.get('Object')}",
            )

    if same_object and same_action and same_type_family and score >= 0.68:
        return (
            "echte Redundanz",
            "; ".join(sorted(shared_tags)),
            "Gleiche Handlung, ähnlicher Pflichttyp und ähnliches Objekt.",
        )

    if same_object and score >= 0.45:
        return (
            "teilweise Überlappung",
            "; ".join(sorted(shared_tags)),
            "Gleiches oder sehr ähnliches Objekt, aber Details fachlich prüfen.",
        )

    if shared_tags and score >= 0.32 and not same_object:
        if same_action or same_type_family:
            return (
                "gleiches Pflichtmuster, anderes Objekt",
                "; ".join(sorted(shared_tags)),
                f"Gleiches Muster, aber anderes Objekt: {left.get('Object')} vs. {right.get('Object')}",
            )
        return (
            "gleiches Thema, andere Pflicht",
            "; ".join(sorted(shared_tags)),
            "Gleiches Thema, aber andere Handlung oder anderes Objekt.",
        )

    if base_relation in {"ähnlich", "teilweise überlappend"} and not shared_tags:
        return (
            "lexikalisch ähnlich, Kontext prüfen",
            "",
            "Textähnlichkeit vorhanden, aber keine gemeinsamen Domänen-Tags erkannt.",
        )

    return (
        base_relation,
        "; ".join(sorted(shared_tags)),
        "Objektkontext ähnlich." if same_object else "Kontext fachlich prüfen.",
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(MASTER, encoding="utf-8-sig")
    df = df[df["Atomic_Requirement"].fillna("").astype(str).str.strip() != ""].copy()
    df["vector_text"] = (
        df["Atomic_Requirement"].fillna("").astype(str)
        + " "
        + df["Object"].fillna("").astype(str)
        + " "
        + df["Condition"].fillna("").astype(str)
        + " "
        + df["Evidence_Required"].fillna("").astype(str)
    )
    vectors = [vectorize(text) for text in df["vector_text"]]

    rows = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            left = df.iloc[i]
            right = df.iloc[j]
            if left.get("Source_Document_ID") == right.get("Source_Document_ID"):
                continue
            score = cosine(vectors[i], vectors[j])
            left_tokens = set(vectors[i])
            right_tokens = set(vectors[j])
            shared = left_tokens & right_tokens
            if score < 0.28 and not ({"aufzeichnungen", "aufzeichnen", "pflanzenschutzmittel"} & shared):
                continue
            base_relation = relation_type(score, shared)
            refined_relation, shared_tags, context_note = context_relation(base_relation, left, right, shared, score)
            review_status = "candidate"
            if refined_relation in {"nur Suchtreffer", "lexikalisch ähnlich, Kontext prüfen"}:
                review_status = "needs_domain_review"
            rows.append(
                {
                    "Relation_ID": f"REL_{len(rows)+1:04d}",
                    "Requirement_ID_A": left["Requirement_ID"],
                    "Requirement_ID_B": right["Requirement_ID"],
                    "Source_A": left["Source_Document_ID"],
                    "Source_B": right["Source_Document_ID"],
                    "Relation_Type": refined_relation,
                    "Similarity_Score": round(score, 3),
                    "Shared_Terms": "; ".join(sorted(shared)[:20]),
                    "Shared_Domain_Tags": shared_tags,
                    "Object_A": left.get("Object"),
                    "Object_B": right.get("Object"),
                    "Requirement_A": left["Atomic_Requirement"],
                    "Requirement_B": right["Atomic_Requirement"],
                    "Confidence": "mittel" if score >= 0.45 else "niedrig",
                    "Reviewer_Notes": f"Automatischer Kandidat; fachlich prüfen. {context_note}",
                    "Review_Status": review_status,
                }
            )

    rel = pd.DataFrame(rows).sort_values("Similarity_Score", ascending=False) if rows else pd.DataFrame()
    rel.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    xlsx_path = OUT_XLSX
    try:
        writer = pd.ExcelWriter(xlsx_path, engine="openpyxl")
    except PermissionError:
        xlsx_path = OUT_DIR / "requirement_relations_candidates_new.xlsx"
        writer = pd.ExcelWriter(xlsx_path, engine="openpyxl")
    with writer:
        rel.to_excel(writer, sheet_name="Requirement_Relations", index=False)

    report = [
        "# Requirement Relations Report",
        "",
        f"Requirements compared: {len(df)}",
        f"Candidate relations: {len(rel)}",
        f"Output CSV: `{OUT_CSV}`",
        f"Output XLSX: `{xlsx_path}`",
        "",
        "## Top Candidates",
        "",
    ]
    for _, row in rel.head(10).iterrows():
        report.append(
            f"- {row['Relation_ID']} ({row['Similarity_Score']}): {row['Requirement_ID_A']} ↔ {row['Requirement_ID_B']} | {row['Relation_Type']}"
        )
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(OUT_XLSX)


if __name__ == "__main__":
    main()
