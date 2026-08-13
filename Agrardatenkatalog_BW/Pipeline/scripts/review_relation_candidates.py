from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
RELATIONS = BASE / "output" / "relations" / "requirement_relations_candidates.csv"
OUT = BASE / "output" / "relations" / "relation_candidate_self_review.md"


def verdict(row: pd.Series) -> tuple[str, str]:
    relation = str(row.get("Relation_Type", ""))
    object_a = str(row.get("Object_A", ""))
    object_b = str(row.get("Object_B", ""))
    score = float(row.get("Similarity_Score", 0))

    if relation == "echte Redundanz":
        return "prüfen", "Automatisch als starke Redundanz erkannt; fachlich bestätigen."
    if relation == "gleiches Pflichtmuster, anderes Objekt":
        return "plausibel", "Kein Redundanzfall, aber als wiederkehrendes Pflichtmuster sinnvoll."
    if relation == "teilweise Überlappung" and score >= 0.45:
        return "plausibel", "Kann als Überlappungskandidat geprüft werden."
    if object_a == "jeweiliger Anwender" or object_b == "jeweiliger Anwender":
        return "eher schwach", "Treffer beruht vermutlich auf Aufzeichnungs-Kontext, nicht auf gleicher Pflicht."
    return "prüfen", "Kandidat braucht fachliche Sichtung."


def main() -> None:
    df = pd.read_csv(RELATIONS, encoding="utf-8-sig")
    rows = []
    for _, row in df.head(25).iterrows():
        status, note = verdict(row)
        rows.append(
            {
                "Relation_ID": row.get("Relation_ID"),
                "Relation_Type": row.get("Relation_Type"),
                "Similarity_Score": row.get("Similarity_Score"),
                "Requirement_ID_A": row.get("Requirement_ID_A"),
                "Requirement_ID_B": row.get("Requirement_ID_B"),
                "Self_Review": status,
                "Self_Review_Note": note,
            }
        )

    review = pd.DataFrame(rows)
    lines = [
        "# Relation Candidate Self Review",
        "",
        "Diese Prüfung ist eine einfache Plausibilitätsprüfung der ersten 25 Kandidaten.",
        "",
        "## Ergebnis",
        "",
    ]
    for status, count in review["Self_Review"].value_counts().items():
        lines.append(f"- {status}: {count}")
    lines += ["", "## Top-Kandidaten", ""]
    for _, row in review.iterrows():
        lines.append(
            f"- {row['Relation_ID']}: {row['Self_Review']} | {row['Relation_Type']} | "
            f"{row['Requirement_ID_A']} ↔ {row['Requirement_ID_B']} | {row['Self_Review_Note']}"
        )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
