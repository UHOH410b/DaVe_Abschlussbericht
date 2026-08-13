from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import pdfplumber


BASE = Path(__file__).resolve().parents[1]
PDF = BASE / "input" / "source_pdfs" / "ecovin_2025_04" / "ECOVIN_Richtline_29.04.2025.pdf"
JOB_DIR = BASE / "output" / "extraction_jobs" / "JOB_ECOVIN_2025_04_FULL_DRAFT"
SECTIONS_CSV = BASE / "output" / "document_sections" / "ECOVIN_2025_04" / "document_sections.csv"
LINKS_CSV = BASE / "output" / "source_document_links.csv"

SOURCE_DOCUMENT_ID = "SRC_ECOVIN_RICHTLINIE_2025_04"
DATA_COLLECTION_ID = "DC_ECOVIN_RICHTLINIE_2025_04"
LINK_ID = "LINK_ECOVIN_2025_04"
SOURCE_TITLE = "ECOVIN-Richtlinie, 18. Fassung, gültig ab 29.04.2025"
SOURCE_URL = "https://www.ecovin.de/"

COLUMNS = [
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

OBLIGATION_RE = re.compile(
    r"\b("
    r"muss|müssen|darf|dürfen|darf nicht|dürfen nicht|ist verboten|sind verboten|"
    r"ist verpflichtet|sind verpflichtet|verpflichtet|hat zu|haben zu|ist zu|sind zu|"
    r"zu vermerken|zu dokumentieren|zu kontrollieren|aufzuzeichnen|nachzuweisen|"
    r"vorzuhalten|einzuhalten|erforderlich|zulässig|nicht zulässig|unzulässig"
    r")\b",
    re.IGNORECASE,
)

SECTION_RE = re.compile(r"^(?P<num>\d+(?:\.\d+){0,5})\s+(?P<title>[A-ZÄÖÜa-zäöüß][^\n]{2,130})$")
NOISE_RE = re.compile(
    r"^(Richtlinie des ECOVIN Bundesverbandes|Inhaltsverzeichnis|Seite\s+\d+\s+von\s+\d+|"
    r"ECOVIN BUNDESVERBANDES|18\. Fassung|Richtlinie$)"
)


def clean_text(text: str) -> str:
    text = text.replace("\u00ad", "")

    def fix_hyphen(match: re.Match) -> str:
        left = match.group(1)
        right = match.group(2)
        if right.lower() in {"und", "oder", "bzw"}:
            return f"{left}- {right}"
        return f"{left}{right}"

    text = re.sub(r"(\w+)-\s+(\w+)", fix_hyphen, text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pages() -> list[dict]:
    pages: list[dict] = []
    with pdfplumber.open(PDF) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = clean_text(page.extract_text() or "")
            pages.append({"page": page_no, "text": text})
    return pages


def is_heading(line: str) -> re.Match | None:
    line = line.strip()
    if not line or NOISE_RE.search(line):
        return None
    if len(line) > 150 or "." * 5 in line:
        return None
    match = SECTION_RE.match(line)
    if not match:
        return None
    if re.search(r"\.{3,}\s*\d+$", line):
        return None
    return match


def extract_sections(pages: list[dict]) -> list[dict]:
    sections: list[dict] = []
    current: dict | None = None

    for page in pages:
        if page["page"] <= 2:
            continue
        for raw_line in page["text"].splitlines():
            line = raw_line.strip()
            heading = is_heading(line)
            if heading:
                if current and current["lines"]:
                    sections.append(current)
                number = heading.group("num")
                title = heading.group("title").strip()
                current = {
                    "section_id": f"ECOVIN_2025_04_SEC_{len(sections)+1:04d}",
                    "section_number": number,
                    "section_title": title,
                    "source_reference": f"{number} {title}",
                    "start_page": page["page"],
                    "end_page": page["page"],
                    "lines": [],
                }
                continue
            if current:
                current["end_page"] = page["page"]
                if line and not NOISE_RE.search(line):
                    current["lines"].append(line)

    if current and current["lines"]:
        sections.append(current)

    for section in sections:
        section["text"] = clean_text("\n".join(section.pop("lines")))
    return sections


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    abbreviations = {
        "bzw.": "bzw§",
        "z. B.": "z§ B§",
        "u. a.": "u§ a§",
        "d. h.": "d§ h§",
        "ca.": "ca§",
        "Nr.": "Nr§",
        "Abs.": "Abs§",
        "e.V.": "e§V§",
    }
    for source, protected in abbreviations.items():
        text = text.replace(source, protected)
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ0-9a-z]\)|[A-ZÄÖÜ0-9])", text)
    restored = []
    for piece in pieces:
        for source, protected in abbreviations.items():
            piece = piece.replace(protected, source)
        piece = re.sub(r"^[a-z]\)\s+", "", piece.strip())
        restored.append(piece)
    return [piece for piece in restored if len(piece) >= 25]


def requirement_type(sentence: str) -> str:
    s = sentence.lower()
    if ("darf" in s and ("nicht" in s or "nur" in s)) or "nicht zulässig" in s or "unzulässig" in s:
        return "Verbot / bedingte Erlaubnis"
    if any(term in s for term in ["aufzuzeichnen", "dokumentieren", "vermerken", "nachweis", "unterlagen"]):
        return "Dokumentations-/Nachweispflicht"
    if "verpflichtet" in s or "muss" in s or "müssen" in s:
        return "Pflicht"
    if "erforderlich" in s or "einzuhalten" in s:
        return "Anforderung"
    return "Anforderung"


def action_from_sentence(sentence: str) -> str:
    s = sentence.lower()
    mapping = [
        ("nicht zulässig", "nicht anwenden/unterlassen"),
        ("unzulässig", "nicht anwenden/unterlassen"),
        ("darf nicht", "nicht anwenden/unterlassen"),
        ("dürfen nicht", "nicht anwenden/unterlassen"),
        ("aufzuzeichnen", "aufzeichnen"),
        ("dokumentieren", "dokumentieren"),
        ("vermerken", "vermerken"),
        ("nachzuweisen", "nachweisen"),
        ("vorzuhalten", "vorhalten"),
        ("einzuhalten", "einhalten"),
        ("beantragen", "beantragen"),
        ("melden", "melden"),
        ("lagern", "lagern"),
        ("kennzeichnen", "kennzeichnen"),
        ("verwenden", "verwenden"),
        ("einsetzen", "einsetzen"),
        ("bewirtschaften", "bewirtschaften"),
        ("erfolgen", "durchführen"),
    ]
    for key, action in mapping:
        if key in s:
            return action
    return "beachten"


def evidence_from_sentence(sentence: str) -> str:
    s = sentence.lower()
    evidence = []
    if "aufzeich" in s:
        evidence.append("Aufzeichnung")
    if "nachweis" in s or "nachzuweisen" in s:
        evidence.append("Nachweis")
    if "unterlagen" in s:
        evidence.append("Unterlagen")
    if "dokument" in s:
        evidence.append("Dokumentation")
    if "kontroll" in s:
        evidence.append("Kontrollunterlagen")
    return " / ".join(dict.fromkeys(evidence))


def normalize_requirement(sentence: str) -> str:
    sentence = sentence.strip()
    if not sentence.endswith("."):
        sentence += "."
    return sentence


def section_slug(section_number: str) -> str:
    return section_number.replace(".", "-")


def build_requirements(sections: list[dict]) -> list[dict]:
    rows: list[dict] = []
    section_counts: dict[str, int] = {}
    for section in sections:
        for sentence in split_sentences(section["text"]):
            if not OBLIGATION_RE.search(sentence):
                continue
            if "fühlen uns" in sentence.lower():
                continue
            section_key = section_slug(section["section_number"])
            section_counts[section_key] = section_counts.get(section_key, 0) + 1
            requirement_id = f"ECOVIN-{section_key}-{section_counts[section_key]:03d}"
            rows.append(
                {
                    "Requirement_ID": requirement_id,
                    "Data_Collection_ID": DATA_COLLECTION_ID,
                    "Source_Document_ID": SOURCE_DOCUMENT_ID,
                    "Source_Reference": f"{section['source_reference']} (S. {section['start_page']}-{section['end_page']})",
                    "Original_Text": sentence,
                    "Atomic_Requirement": normalize_requirement(sentence),
                    "Requirement_Type": requirement_type(sentence),
                    "Actor": "ECOVIN-Vertragspartner / zertifizierter Betrieb",
                    "Action": action_from_sentence(sentence),
                    "Object": section["section_title"],
                    "Condition": "",
                    "Deadline_or_Frequency": "",
                    "Evidence_Required": evidence_from_sentence(sentence),
                    "BPMN_Element_Type": "Task; Business Rule",
                    "Extraction_Status": "draft_imported_rule_based",
                    "Notes": "Automatisch regelbasiert aus ECOVIN-PDF extrahiert; fachlich zu prüfen.",
                }
            )
    return rows


def upsert_source_link() -> None:
    row = {
        "Link_ID": LINK_ID,
        "Data_Collection_ID": DATA_COLLECTION_ID,
        "Source_Document_ID": SOURCE_DOCUMENT_ID,
        "Kurztitel": "ECOVIN",
        "Link_Type": "Grundlagendokument",
        "Link_Title": SOURCE_TITLE,
        "URL": SOURCE_URL,
        "Format": "PDF",
        "Excel_Row": "",
        "Notes": "Automatisch aus lokalem PDF-Import ECOVIN 29.04.2025 ergänzt.",
    }
    if LINKS_CSV.exists():
        df = pd.read_csv(LINKS_CSV, encoding="utf-8-sig")
        df = df[df["Link_ID"].astype(str) != LINK_ID]
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(LINKS_CSV, index=False, encoding="utf-8-sig")


def write_outputs(sections: list[dict], requirements: list[dict]) -> None:
    JOB_DIR.mkdir(parents=True, exist_ok=True)
    SECTIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(requirements, columns=COLUMNS).to_csv(
        JOB_DIR / "atomic_requirements_output.csv", index=False, encoding="utf-8-sig"
    )
    pd.DataFrame(
        [
            {
                "Document_Section_ID": section["section_id"],
                "Link_ID": LINK_ID,
                "Data_Collection_ID": DATA_COLLECTION_ID,
                "Source_Document_ID": SOURCE_DOCUMENT_ID,
                "Section_Type": "PDF section",
                "Section_Number": section["section_number"],
                "Section_Title": section["section_title"],
                "Source_Reference": section["source_reference"],
                "Section_URL": "",
                "Discovery_Status": "pdf_extracted",
                "Start_Page": section["start_page"],
                "End_Page": section["end_page"],
                "Text_Length": len(section["text"]),
            }
            for section in sections
        ]
    ).to_csv(SECTIONS_CSV, index=False, encoding="utf-8-sig")
    (JOB_DIR / "source_metadata.json").write_text(
        "{\n"
        f'  "Source_Document_ID": "{SOURCE_DOCUMENT_ID}",\n'
        f'  "Source_Document_Title": "{SOURCE_TITLE}",\n'
        f'  "Data_Collection_ID": "{DATA_COLLECTION_ID}",\n'
        f'  "Source_URL": "{SOURCE_URL}",\n'
        '  "Extraction_Method": "rule_based_pdf_draft"\n'
        "}\n",
        encoding="utf-8",
    )


def main() -> None:
    pages = extract_pages()
    sections = extract_sections(pages)
    requirements = build_requirements(sections)
    upsert_source_link()
    write_outputs(sections, requirements)
    print(f"pages={len(pages)}")
    print(f"sections={len(sections)}")
    print(f"requirements={len(requirements)}")
    print(JOB_DIR / "atomic_requirements_output.csv")


if __name__ == "__main__":
    main()
