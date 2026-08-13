from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
JOBS = BASE / "output" / "extraction_jobs"

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

DC_DUEV = "DC_015_DUNGEVERORDNUNG_DUV"
SRC_DUEV = "SRC_VERORDNUNG_UBER_DIE_ANWENDUNG_VON_DUNGEMIT"
DC_PFLSCHG = "DC_016_PFLANZENSCHUTZGESETZ_PFLSCHG"
SRC_PFLSCHG = "SRC_GESETZ_ZUM_SCHUTZ_DER_KULTURPFLANZEN_PFLAN"


def write_job(job_name: str, rows: list[dict]) -> None:
    job_dir = JOBS / job_name
    job_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=COLUMNS).to_csv(
        job_dir / "atomic_requirements_output.csv",
        index=False,
        encoding="utf-8-sig",
    )


def empty_job(job_name: str, note: str) -> None:
    write_job(job_name, [])
    (JOBS / job_name / "extraction_notes.md").write_text(note, encoding="utf-8")


def req(
    rid: str,
    dc: str,
    src: str,
    ref: str,
    original: str,
    atomic: str,
    rtype: str,
    actor: str,
    action: str,
    obj: str,
    condition: str = "",
    deadline: str = "",
    evidence: str = "",
    bpmn: str = "Task",
    notes: str = "",
) -> dict:
    return {
        "Requirement_ID": rid,
        "Data_Collection_ID": dc,
        "Source_Document_ID": src,
        "Source_Reference": ref,
        "Original_Text": original,
        "Atomic_Requirement": atomic,
        "Requirement_Type": rtype,
        "Actor": actor,
        "Action": action,
        "Object": obj,
        "Condition": condition,
        "Deadline_or_Frequency": deadline,
        "Evidence_Required": evidence,
        "BPMN_Element_Type": bpmn,
        "Extraction_Status": "draft_extracted",
        "Notes": notes,
    }


def duev(ref: str, original: str, atomic: str, rtype: str, actor: str, action: str, obj: str, **kwargs) -> dict:
    return req(
        "DUEV-" + ref.split()[1].replace("Abs.", "").replace("Satz", "").replace("Nr.", "").replace("§", ""),
        DC_DUEV,
        SRC_DUEV,
        ref,
        original,
        atomic,
        rtype,
        actor,
        action,
        obj,
        **kwargs,
    )


def main() -> None:
    write_job(
        "JOB_LINK_0052_SEC_0006",
        [
            req("DUEV-006-001-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 1 Satz 1 DüV", "unverzüglich ... einzuarbeiten", "Wer organische oder organisch-mineralische Düngemittel mit wesentlichem Gehalt an verfügbarem Stickstoff oder Ammoniumstickstoff auf unbestelltes Ackerland aufbringt, muss diese unverzüglich einarbeiten.", "Handlungspflicht / Frist", "Anwender / Betriebsinhaber", "einarbeiten", "organische oder organisch-mineralische Düngemittel", "Aufbringung auf unbestelltes Ackerland; wesentlicher Gehalt an verfügbarem Stickstoff oder Ammoniumstickstoff", "unverzüglich", "Düngedokumentation / Arbeitsnachweis", "Task; Timer Event"),
            req("DUEV-006-001-002", DC_DUEV, SRC_DUEV, "§ 6 Abs. 1 Satz 1 DüV", "spätestens innerhalb von vier Stunden", "Wer die genannten Düngemittel auf unbestelltes Ackerland aufbringt, muss sie spätestens innerhalb von vier Stunden nach Beginn des Aufbringens einarbeiten.", "Handlungspflicht / Frist", "Anwender / Betriebsinhaber", "einarbeiten", "Düngemittel", "bis 31. Januar 2025; soweit keine Ausnahme nach § 6 Abs. 1 Satz 2 oder Satz 3 greift", "spätestens innerhalb von vier Stunden nach Beginn des Aufbringens", "Düngedokumentation / Arbeitsnachweis", "Task; Timer Event"),
            req("DUEV-006-001-003", DC_DUEV, SRC_DUEV, "§ 6 Abs. 1 Satz 1 DüV", "ab dem 1. Februar 2025 innerhalb einer Stunde", "Ab dem 1. Februar 2025 muss der Anwender die genannten Düngemittel auf unbestelltem Ackerland spätestens innerhalb einer Stunde nach Beginn des Aufbringens einarbeiten.", "Handlungspflicht / Frist", "Anwender / Betriebsinhaber", "einarbeiten", "Düngemittel", "ab 1. Februar 2025; Aufbringung auf unbestelltes Ackerland", "innerhalb einer Stunde nach Beginn des Aufbringens", "Düngedokumentation / Arbeitsnachweis", "Task; Timer Event"),
            req("DUEV-006-001-004", DC_DUEV, SRC_DUEV, "§ 6 Abs. 1 Satz 4 DüV", "muss die Einarbeitung unverzüglich erfolgen", "Wenn die Einarbeitungsfrist wegen nachträglicher nicht vorhersehbarer Witterungsereignisse und Nichtbefahrbarkeit des Bodens überschritten werden darf, muss die Einarbeitung unverzüglich nach Wiederherstellung der Befahrbarkeit erfolgen.", "Bedingte Handlungspflicht / Frist", "Anwender / Betriebsinhaber", "einarbeiten", "Düngemittel", "Einarbeitungsfrist kann wegen nicht vorhersehbarer Witterungsereignisse und Nichtbefahrbarkeit nicht eingehalten werden", "unverzüglich nach Wiederherstellung der Befahrbarkeit", "Witterungs-/Flächendokumentation", "Task; Timer Event"),
            req("DUEV-006-002-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 2 DüV", "Harnstoff ... nur noch aufgebracht werden", "Harnstoff als Düngemittel darf ab dem 1. Februar 2020 nur aufgebracht werden, wenn ihm ein Ureasehemmstoff zugegeben ist oder er unverzüglich eingearbeitet wird.", "Bedingtes Verbot / Anwendungsvorgabe", "Anwender / Betriebsinhaber", "aufbringen", "Harnstoff als Düngemittel", "ab 1. Februar 2020", "unverzüglich; spätestens innerhalb von vier Stunden nach Aufbringung bei Einarbeitung", "Düngemittelkennzeichnung / Arbeitsnachweis", "Gateway; Task"),
            req("DUEV-006-003-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 3 Satz 1 DüV", "nur noch streifenförmig ... oder direkt", "Flüssige organische und flüssige organisch-mineralische Düngemittel mit wesentlichem Gehalt an verfügbarem Stickstoff oder Ammoniumstickstoff dürfen auf bestelltem Ackerland ab dem 1. Februar 2020 nur streifenförmig auf den Boden aufgebracht oder direkt in den Boden eingebracht werden.", "Anwendungsvorgabe / Verbot", "Anwender / Betriebsinhaber", "streifenförmig aufbringen oder direkt einbringen", "flüssige organische und flüssige organisch-mineralische Düngemittel", "bestelltes Ackerland; ab 1. Februar 2020", "", "Arbeits-/Maschinendokumentation", "Gateway; Task"),
            req("DUEV-006-003-002", DC_DUEV, SRC_DUEV, "§ 6 Abs. 3 Satz 2 DüV", "Im Falle von Grünland ... ab dem 1. Februar 2025", "Auf Grünland, Dauergrünland oder mehrschnittigem Feldfutterbau gelten die streifenförmige Aufbringung oder direkte Einbringung flüssiger organischer und flüssiger organisch-mineralischer Düngemittel ab dem 1. Februar 2025.", "Anwendungsvorgabe / Frist", "Anwender / Betriebsinhaber", "streifenförmig aufbringen oder direkt einbringen", "flüssige organische und flüssige organisch-mineralische Düngemittel", "Grünland, Dauergrünland oder mehrschnittiger Feldfutterbau", "ab 1. Februar 2025", "Arbeits-/Maschinendokumentation", "Gateway; Task"),
            req("DUEV-006-004-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 4 Satz 1 DüV", "170 Kilogramm Gesamtstickstoff je Hektar und Jahr", "Aus organischen und organisch-mineralischen Düngemitteln einschließlich Wirtschaftsdüngern dürfen im Durchschnitt der landwirtschaftlich genutzten Flächen des Betriebes höchstens 170 Kilogramm Gesamtstickstoff je Hektar und Jahr aufgebracht werden.", "Grenzwert / Verbot", "Betriebsinhaber", "begrenzen", "Gesamtstickstoff aus organischen und organisch-mineralischen Düngemitteln", "Durchschnitt der landwirtschaftlich genutzten Flächen des Betriebes", "je Hektar und Jahr", "Nährstoffberechnung / Düngedokumentation", "Business Rule"),
            req("DUEV-006-004-002", DC_DUEV, SRC_DUEV, "§ 6 Abs. 4 Satz 2 DüV", "Kompost ... 510 Kilogramm", "Bei Kompost darf die aufgebrachte Menge an Gesamtstickstoff im Durchschnitt der landwirtschaftlich genutzten Flächen des Betriebes in einem Zeitraum von drei Jahren 510 Kilogramm Gesamtstickstoff je Hektar nicht überschreiten.", "Grenzwert / Verbot", "Betriebsinhaber", "begrenzen", "Gesamtstickstoff aus Kompost", "Kompostaufbringung", "Zeitraum von drei Jahren", "Nährstoffberechnung / Düngedokumentation", "Business Rule"),
            req("DUEV-006-005-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 5 Satz 4 DüV", "jährlich ... zu beantragen", "Eine Genehmigung für Ausnahmen beim Aufbringen von Wirtschaftsdüngern tierischer Herkunft ist jährlich bei der zuständigen Stelle zu beantragen.", "Antragspflicht / Frequenz", "Betriebsinhaber / Antragsteller", "beantragen", "Ausnahmegenehmigung", "Aufbringen von Wirtschaftsdüngern tierischer Herkunft oberhalb der regulären Beschränkung", "jährlich", "Antrag / Genehmigung", "Task; Timer Event"),
            req("DUEV-006-007-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 7 Satz 1 DüV", "170 Kilogramm ... nicht überschreitet", "Bei einer Genehmigung nach § 6 Abs. 6 dürfen die genannten Düngemittel nur aufgebracht werden, soweit die anteilig aus Wirtschaftsdüngern tierischer Herkunft stammende Menge an Gesamtstickstoff im Betriebsdurchschnitt 170 Kilogramm je Hektar und Jahr nicht überschreitet.", "Grenzwert / Bedingung", "Betriebsinhaber", "begrenzen", "anteiliger Gesamtstickstoff aus Wirtschaftsdüngern tierischer Herkunft", "Genehmigung nach § 6 Abs. 6", "je Hektar und Jahr", "Nährstoffberechnung / Genehmigung", "Business Rule"),
            req("DUEV-006-008-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 8 Satz 1 Nr. 1 DüV", "auf Ackerland ... bis 31. Januar", "Düngemittel mit wesentlichem Gehalt an Stickstoff dürfen auf Ackerland ab Ernte der letzten Hauptfrucht bis zum 31. Januar nicht aufgebracht werden.", "Verbot / Sperrfrist", "Anwender / Betriebsinhaber", "nicht aufbringen", "stickstoffhaltige Düngemittel", "Ackerland; nach Ernte der letzten Hauptfrucht", "bis 31. Januar", "Düngedokumentation / Flächenstatus", "Business Rule; Timer Event"),
            req("DUEV-006-008-002", DC_DUEV, SRC_DUEV, "§ 6 Abs. 8 Satz 1 Nr. 2 DüV", "1. November bis 31. Januar", "Düngemittel mit wesentlichem Gehalt an Stickstoff dürfen auf Grünland, Dauergrünland und Ackerland mit mehrjährigem Feldfutterbau bei Aussaat bis 15. Mai vom 1. November bis 31. Januar nicht aufgebracht werden.", "Verbot / Sperrfrist", "Anwender / Betriebsinhaber", "nicht aufbringen", "stickstoffhaltige Düngemittel", "Grünland, Dauergrünland oder Ackerland mit mehrjährigem Feldfutterbau bei Aussaat bis 15. Mai", "1. November bis 31. Januar", "Düngedokumentation / Flächenstatus", "Business Rule; Timer Event"),
            req("DUEV-006-008-003", DC_DUEV, SRC_DUEV, "§ 6 Abs. 8 Satz 2 DüV", "1. Dezember bis 15. Januar", "Festmist von Huftieren oder Klauentieren und Kompost dürfen vom 1. Dezember bis zum 15. Januar nicht aufgebracht werden.", "Verbot / Sperrfrist", "Anwender / Betriebsinhaber", "nicht aufbringen", "Festmist von Huftieren oder Klauentieren und Kompost", "", "1. Dezember bis 15. Januar", "Düngedokumentation", "Business Rule; Timer Event"),
            req("DUEV-006-008-004", DC_DUEV, SRC_DUEV, "§ 6 Abs. 8 Satz 3 DüV", "Phosphat ... 1. Dezember bis 15. Januar", "Düngemittel mit wesentlichem Gehalt an Phosphat dürfen vom 1. Dezember bis zum 15. Januar nicht aufgebracht werden.", "Verbot / Sperrfrist", "Anwender / Betriebsinhaber", "nicht aufbringen", "phosphathaltige Düngemittel", "", "1. Dezember bis 15. Januar", "Düngedokumentation", "Business Rule; Timer Event"),
            req("DUEV-006-009-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 9 Satz 1 Nr. 1 DüV", "nicht mehr als 30 Kilogramm Ammoniumstickstoff oder 60 Kilogramm Gesamtstickstoff", "Bei zulässiger Herbstdüngung zu Zwischenfrüchten, Winterraps, Feldfutter oder Wintergerste nach Getreidevorfrucht darf insgesamt nicht mehr als 30 Kilogramm Ammoniumstickstoff oder 60 Kilogramm Gesamtstickstoff je Hektar aufgebracht werden.", "Grenzwert / Ausnahme", "Anwender / Betriebsinhaber", "begrenzen", "Ammoniumstickstoff und Gesamtstickstoff", "Ackerland; Ausnahme nach § 6 Abs. 9 Satz 1 Nr. 1", "bis 1. Oktober", "Düngedokumentation / Düngebedarf", "Business Rule; Timer Event"),
            req("DUEV-006-009-002", DC_DUEV, SRC_DUEV, "§ 6 Abs. 9 Satz 1 Nr. 2 DüV", "bis zum Ablauf des 1. Dezember", "Zu Gemüse-, Erdbeer- und Beerenobstkulturen dürfen Düngemittel mit wesentlichem Stickstoffgehalt bis zur Höhe des Stickstoffdüngebedarfs bis zum 1. Dezember aufgebracht werden.", "Bedingte Erlaubnis / Frist", "Anwender / Betriebsinhaber", "aufbringen", "stickstoffhaltige Düngemittel", "Gemüse-, Erdbeer- und Beerenobstkulturen; bis zur Höhe des Stickstoffdüngebedarfs", "bis 1. Dezember", "Düngebedarfsermittlung / Düngedokumentation", "Gateway; Timer Event"),
            req("DUEV-006-011-001", DC_DUEV, SRC_DUEV, "§ 6 Abs. 11 DüV", "nicht mehr als 80 Kilogramm Gesamtstickstoff je Hektar", "Auf Grünland, Dauergrünland und Ackerland mit mehrjährigem Feldfutterbau dürfen vom 1. September bis zum Beginn des Verbotszeitraums mit flüssigen organischen oder flüssigen organisch-mineralischen Düngemitteln höchstens 80 Kilogramm Gesamtstickstoff je Hektar aufgebracht werden.", "Grenzwert / Zeitraum", "Anwender / Betriebsinhaber", "begrenzen", "Gesamtstickstoff aus flüssigen organischen oder flüssigen organisch-mineralischen Düngemitteln", "wesentlicher Gehalt an verfügbarem Stickstoff oder Ammoniumstickstoff", "1. September bis Beginn des Verbotszeitraums", "Düngedokumentation", "Business Rule; Timer Event"),
        ],
    )

    write_job(
        "JOB_LINK_0054_SEC_0012",
        [
            req("PFLSCHG-012-001-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 1 PflSchG", "nur angewandt werden, wenn sie zugelassen sind", "Pflanzenschutzmittel dürfen nur angewandt werden, wenn sie zugelassen sind und die Zulassung nicht ruht.", "Verbot / Zulassungsvoraussetzung", "Anwender", "anwenden", "Pflanzenschutzmittel", "", "", "Zulassungsprüfung / Mittelverzeichnis", "Gateway; Business Rule"),
            req("PFLSCHG-012-001-002", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 1 Nr. 1 PflSchG", "in den ... Anwendungsgebieten", "Pflanzenschutzmittel dürfen nur in den jeweils gültigen, in der Zulassung festgesetzten Anwendungsgebieten angewandt werden.", "Anwendungsvorgabe", "Anwender", "anwenden", "Pflanzenschutzmittel", "zugelassenes Pflanzenschutzmittel", "", "Zulassung / Gebrauchsanleitung", "Business Rule"),
            req("PFLSCHG-012-001-003", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 1 Nr. 2 PflSchG", "entsprechend ... Anwendungsbestimmungen", "Pflanzenschutzmittel dürfen nur entsprechend den jeweils gültigen, in der Zulassung festgesetzten Anwendungsbestimmungen angewandt werden.", "Anwendungsvorgabe", "Anwender", "anwenden", "Pflanzenschutzmittel", "zugelassenes Pflanzenschutzmittel", "", "Zulassung / Gebrauchsanleitung", "Business Rule"),
            req("PFLSCHG-012-002-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 2 Satz 1 PflSchG", "nicht auf befestigten Freilandflächen", "Pflanzenschutzmittel dürfen nicht auf befestigten Freilandflächen angewandt werden.", "Verbot", "Anwender", "nicht anwenden", "Pflanzenschutzmittel", "befestigte Freilandflächen", "", "Flächendokumentation", "Business Rule"),
            req("PFLSCHG-012-002-002", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 2 Satz 1 PflSchG", "nicht auf sonstigen Freilandflächen", "Pflanzenschutzmittel dürfen nicht auf sonstigen Freilandflächen angewandt werden, die weder landwirtschaftlich noch forstwirtschaftlich noch gärtnerisch genutzt werden.", "Verbot", "Anwender", "nicht anwenden", "Pflanzenschutzmittel", "sonstige nicht landwirtschaftlich, forstwirtschaftlich oder gärtnerisch genutzte Freilandflächen", "", "Flächendokumentation", "Business Rule"),
            req("PFLSCHG-012-002-003", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 2 Satz 2 PflSchG", "nicht in oder unmittelbar an oberirdischen Gewässern", "Pflanzenschutzmittel dürfen nicht in oder unmittelbar an oberirdischen Gewässern angewandt werden.", "Verbot", "Anwender", "nicht anwenden", "Pflanzenschutzmittel", "oberirdische Gewässer", "", "Flächen-/Gewässerabstandsdokumentation", "Business Rule"),
            req("PFLSCHG-012-002-004", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 2 Satz 2 PflSchG", "nicht ... an Küstengewässern", "Pflanzenschutzmittel dürfen nicht in oder unmittelbar an Küstengewässern angewandt werden.", "Verbot", "Anwender", "nicht anwenden", "Pflanzenschutzmittel", "Küstengewässer", "", "Flächen-/Gewässerabstandsdokumentation", "Business Rule"),
            req("PFLSCHG-012-003-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 3 Satz 1 PflSchG", "nur durch Personen ... sachkundig", "Pflanzenschutzmittel, die nur für berufliche Anwender zugelassen sind, dürfen nur durch sachkundige Personen angewandt werden.", "Sachkundepflicht", "beruflicher Anwender", "anwenden", "Pflanzenschutzmittel für berufliche Anwender", "außer den Ausnahmen nach § 9 Abs. 5 Nr. 2 und 3", "", "Sachkundenachweis", "Gateway; Task"),
            req("PFLSCHG-012-004-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 4 Satz 2 PflSchG", "nur nach den ... Anwendungsbestimmungen", "Pflanzenschutzmittel mit Genehmigung nach Artikel 53 oder Artikel 54 der Verordnung (EG) Nr. 1107/2009 dürfen nur nach den in der Genehmigung festgesetzten Anwendungsbestimmungen angewandt werden.", "Anwendungsvorgabe", "Anwender", "anwenden", "Pflanzenschutzmittel mit Notfall- oder Versuchsgenehmigung", "Genehmigung nach Artikel 53 oder Artikel 54", "", "Genehmigung / Anwendungsbestimmungen", "Business Rule"),
            req("PFLSCHG-012-004-002", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 4 Satz 2 PflSchG", "nur nach den ... Anwendungsgebieten", "Pflanzenschutzmittel mit Genehmigung nach Artikel 53 oder Artikel 54 der Verordnung (EG) Nr. 1107/2009 dürfen nur in den in der Genehmigung festgesetzten Anwendungsgebieten angewandt werden.", "Anwendungsvorgabe", "Anwender", "anwenden", "Pflanzenschutzmittel mit Notfall- oder Versuchsgenehmigung", "Genehmigung nach Artikel 53 oder Artikel 54", "", "Genehmigung / Anwendungsgebiete", "Business Rule"),
            req("PFLSCHG-012-006-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 12 Abs. 6 PflSchG", "wenn die zuständige Behörde eine Genehmigung ... erteilt hat", "Zugelassene Pflanzenschutzmittel dürfen in einem anderen als dem zugelassenen Anwendungsgebiet nur angewandt werden, wenn die zuständige Behörde eine Genehmigung nach § 22 Abs. 2 PflSchG erteilt hat.", "Bedingte Erlaubnis / Genehmigungspflicht", "Anwender", "anwenden", "Pflanzenschutzmittel", "anderes als zugelassenes Anwendungsgebiet", "", "Genehmigung", "Gateway; Task"),
        ],
    )

    write_job(
        "JOB_LINK_0054_SEC_0013",
        [
            req("PFLSCHG-013-001-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 13 Abs. 1 Nr. 1 PflSchG", "schädliche Auswirkungen auf die Gesundheit", "Pflanzenschutzmittel dürfen nicht angewandt werden, wenn der Anwender damit rechnen muss, dass die Anwendung schädliche Auswirkungen auf die Gesundheit von Mensch oder Tier oder auf das Grundwasser hat.", "Verbot / Risikoprüfung", "Anwender", "nicht anwenden", "Pflanzenschutzmittel", "erwartbare schädliche Auswirkungen auf Mensch, Tier oder Grundwasser", "", "Risikoprüfung / Anwendungsdokumentation", "Gateway; Business Rule"),
            req("PFLSCHG-013-001-002", DC_PFLSCHG, SRC_PFLSCHG, "§ 13 Abs. 1 Nr. 2 PflSchG", "sonstige erhebliche schädliche Auswirkungen", "Pflanzenschutzmittel dürfen nicht angewandt werden, wenn der Anwender mit sonstigen erheblichen schädlichen Auswirkungen, insbesondere auf den Naturhaushalt, rechnen muss.", "Verbot / Risikoprüfung", "Anwender", "nicht anwenden", "Pflanzenschutzmittel", "erwartbare erhebliche schädliche Auswirkungen auf den Naturhaushalt", "", "Risikoprüfung / Anwendungsdokumentation", "Gateway; Business Rule"),
            req("PFLSCHG-013-002-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 13 Abs. 2 Satz 1 Nr. 1 PflSchG", "nachzustellen, sie zu fangen, zu verletzen oder zu töten", "Bei der Anwendung von Pflanzenschutzmitteln ist es verboten, wild lebenden Tieren besonders geschützter Arten nachzustellen, sie zu fangen, zu verletzen oder zu töten.", "Verbot / Artenschutz", "Anwender", "unterlassen", "Einwirkung auf besonders geschützte wild lebende Tiere", "bei Anwendung von Pflanzenschutzmitteln", "", "Risikoprüfung / Flächendokumentation", "Business Rule"),
            req("PFLSCHG-013-002-002", DC_PFLSCHG, SRC_PFLSCHG, "§ 13 Abs. 2 Satz 1 Nr. 1 PflSchG", "Entwicklungsformen ... zu entnehmen, zu beschädigen oder zu zerstören", "Bei der Anwendung von Pflanzenschutzmitteln ist es verboten, Entwicklungsformen wild lebender Tiere besonders geschützter Arten aus der Natur zu entnehmen, zu beschädigen oder zu zerstören.", "Verbot / Artenschutz", "Anwender", "unterlassen", "Entwicklungsformen besonders geschützter wild lebender Tiere", "bei Anwendung von Pflanzenschutzmitteln", "", "Risikoprüfung / Flächendokumentation", "Business Rule"),
            req("PFLSCHG-013-002-003", DC_PFLSCHG, SRC_PFLSCHG, "§ 13 Abs. 2 Satz 1 Nr. 2 PflSchG", "erheblich zu stören", "Bei der Anwendung von Pflanzenschutzmitteln ist es verboten, wild lebende Tiere streng geschützter Arten und europäischer Vogelarten während sensibler Zeiten erheblich zu stören.", "Verbot / Artenschutz", "Anwender", "unterlassen", "erhebliche Störung streng geschützter Arten und europäischer Vogelarten", "Fortpflanzungs-, Aufzucht-, Mauser-, Überwinterungs- und Wanderungszeiten", "", "Risikoprüfung / Flächendokumentation", "Business Rule"),
            req("PFLSCHG-013-002-004", DC_PFLSCHG, SRC_PFLSCHG, "§ 13 Abs. 2 Satz 1 Nr. 3 PflSchG", "Fortpflanzungs- oder Ruhestätten ... zu beschädigen oder zu zerstören", "Bei der Anwendung von Pflanzenschutzmitteln ist es verboten, Fortpflanzungs- oder Ruhestätten wild lebender Tiere besonders geschützter Arten zu entnehmen, zu beschädigen oder zu zerstören.", "Verbot / Artenschutz", "Anwender", "unterlassen", "Fortpflanzungs- oder Ruhestätten besonders geschützter wild lebender Tiere", "bei Anwendung von Pflanzenschutzmitteln", "", "Risikoprüfung / Flächendokumentation", "Business Rule"),
            req("PFLSCHG-013-002-005", DC_PFLSCHG, SRC_PFLSCHG, "§ 13 Abs. 2 Satz 1 Nr. 4 PflSchG", "Pflanzen ... zu entnehmen ... Standorte zu beschädigen", "Bei der Anwendung von Pflanzenschutzmitteln ist es verboten, wild lebende Pflanzen besonders geschützter Arten oder ihre Entwicklungsformen zu entnehmen, sie oder ihre Standorte zu beschädigen oder zu zerstören.", "Verbot / Artenschutz", "Anwender", "unterlassen", "wild lebende Pflanzen besonders geschützter Arten", "bei Anwendung von Pflanzenschutzmitteln", "", "Risikoprüfung / Flächendokumentation", "Business Rule"),
        ],
    )

    write_job(
        "JOB_LINK_0054_SEC_0017",
        [
            req("PFLSCHG-017-001-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 17 Abs. 1 Satz 1 PflSchG", "nur ein zugelassenes Pflanzenschutzmittel", "Auf Flächen, die für die Allgemeinheit bestimmt sind, darf nur ein Pflanzenschutzmittel angewandt werden, das eine der Voraussetzungen nach § 17 Abs. 1 Nr. 1 bis 3 PflSchG erfüllt.", "Bedingtes Verbot / Anwendungsvorgabe", "Anwender", "anwenden", "Pflanzenschutzmittel", "Flächen, die für die Allgemeinheit bestimmt sind", "", "Zulassung / Genehmigung / Flächenstatus", "Gateway; Business Rule"),
            req("PFLSCHG-017-006-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 17 Abs. 6 Satz 1 PflSchG", "Bei Gefahr im Verzug ... Ausnahmen", "Bei Gefahr im Verzug darf von § 17 Abs. 1 Satz 1 nur abgewichen werden, wenn die zuständige Behörde eine Ausnahme genehmigt und Maßnahmen getroffen werden, um eine Gefährdung der Allgemeinheit auszuschließen.", "Bedingte Erlaubnis / Genehmigungspflicht", "Anwender / Antragsteller", "beantragen und Schutzmaßnahmen treffen", "Ausnahme für Pflanzenschutzmittelanwendung", "Gefahr im Verzug; Fläche für die Allgemeinheit", "", "Ausnahmegenehmigung / Schutzmaßnahmen", "Gateway; Task"),
        ],
    )

    write_job(
        "JOB_LINK_0054_SEC_0018",
        [
            req("PFLSCHG-018-001-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 18 Abs. 1 PflSchG", "ohne Genehmigung ... verboten", "Die Anwendung von Pflanzenschutzmitteln mit Luftfahrzeugen ist ohne Genehmigung verboten.", "Verbot / Genehmigungspflicht", "Anwender", "nicht anwenden", "Pflanzenschutzmittel mit Luftfahrzeugen", "keine Genehmigung nach § 18 Abs. 2 PflSchG", "", "Genehmigung", "Gateway; Business Rule"),
            req("PFLSCHG-018-002-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 18 Abs. 2 Satz 2 PflSchG", "soll nur erteilt werden ... im Weinbau in Steillagen", "Eine Genehmigung zur Anwendung von Pflanzenschutzmitteln mit Luftfahrzeugen soll nur zur Bekämpfung von Schadorganismen im Weinbau in Steillagen oder im Kronenbereich von Wäldern erteilt werden.", "Bedingung / Genehmigung", "Antragsteller / Anwender", "beantragen", "Genehmigung für Luftfahrzeuganwendung", "Schadorganismenbekämpfung; insbesondere Weinbau in Steillagen oder Kronenbereich von Wäldern", "", "Antrag / Flächenstatus", "Gateway; Task"),
            req("PFLSCHG-018-002-002", DC_PFLSCHG, SRC_PFLSCHG, "§ 18 Abs. 2 Satz 3 PflSchG", "verbindet die Genehmigung mit den Auflagen", "Der Anwender muss die Auflagen einhalten, die mit der Genehmigung zur Anwendung von Pflanzenschutzmitteln mit Luftfahrzeugen verbunden sind.", "Auflagenpflicht", "Anwender", "einhalten", "Genehmigungsauflagen", "Genehmigung nach § 18 Abs. 2 PflSchG", "", "Genehmigungsbescheid / Anwendungsdokumentation", "Task"),
            req("PFLSCHG-018-003-001", DC_PFLSCHG, SRC_PFLSCHG, "§ 18 Abs. 3 PflSchG", "nur für die Anwendung eines Pflanzenschutzmittels", "Eine Genehmigung zur Anwendung mit Luftfahrzeugen darf nur für Pflanzenschutzmittel genutzt werden, die für die Anwendung mit Luftfahrzeugen zugelassen oder genehmigt sind.", "Anwendungsvorgabe / Genehmigung", "Anwender", "anwenden", "Pflanzenschutzmittel mit Luftfahrzeugen", "Genehmigung nach § 18 Abs. 2 PflSchG", "", "Zulassung / Genehmigung", "Gateway; Business Rule"),
        ],
    )

    empty_job(
        "JOB_LINK_0054_SEC_0021",
        "§ 21 PflSchG regelt vor allem Zuständigkeiten und Datenerhebung durch das Julius Kühn-Institut und Länderbehörden. Aus diesem Abschnitt wurde in diesem Batch keine direkte Pflicht für Landwirte oder Anwender extrahiert.",
    )

    write_job(
        "JOB_LINK_0052_SEC_0014",
        [
            req("DUEV-013A-002-001", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 1 DüV", "Gesamtsumme ... um 20 Prozent zu verringern", "In ausgewiesenen Gebieten muss der Betriebsinhaber den Stickstoffdüngebedarf für betroffene Flächen bis zum 31. März zu einer jährlichen betrieblichen Gesamtsumme zusammenfassen und aufzeichnen.", "Dokumentationspflicht / Frist", "Betriebsinhaber", "zusammenfassen und aufzeichnen", "Stickstoffdüngebedarf", "Flächen liegen in ausgewiesenen Gebieten nach § 13a Abs. 1 Nr. 1 bis 3 DüV", "bis 31. März des laufenden Düngejahres", "Düngebedarfsermittlung / Aufzeichnung", "Task; Timer Event"),
            req("DUEV-013A-002-002", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 1 DüV", "um 20 Prozent zu verringern", "In ausgewiesenen Gebieten muss der Betriebsinhaber die jährliche betriebliche Gesamtsumme des Stickstoffdüngebedarfs um 20 Prozent verringern.", "Grenzwert / Reduktionspflicht", "Betriebsinhaber", "verringern", "Gesamtsumme des Stickstoffdüngebedarfs", "Flächen liegen in ausgewiesenen Gebieten nach § 13a Abs. 1 Nr. 1 bis 3 DüV; keine Ausnahme greift", "laufendes Düngejahr", "Düngebedarfsermittlung / Aufzeichnung", "Business Rule"),
            req("DUEV-013A-002-003", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 1 DüV", "darf ... nicht überschritten werden", "In ausgewiesenen Gebieten darf der Betriebsinhaber bei Düngungsmaßnahmen im laufenden Düngejahr die verringerte Gesamtsumme des Stickstoffdüngebedarfs nicht überschreiten.", "Grenzwert / Verbot", "Betriebsinhaber", "nicht überschreiten", "verringerte Gesamtsumme des Stickstoffdüngebedarfs", "Flächen liegen in ausgewiesenen Gebieten nach § 13a Abs. 1 Nr. 1 bis 3 DüV; keine Ausnahme greift", "laufendes Düngejahr", "Düngedokumentation / Düngebedarfsermittlung", "Business Rule"),
            req("DUEV-013A-002-004", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 2 DüV", "170 Kilogramm ... je Schlag", "In ausgewiesenen Gebieten dürfen Nährstoffe aus organischen und organisch-mineralischen Düngemitteln je Schlag, Bewirtschaftungseinheit oder zusammengefasster Fläche höchstens bis 170 Kilogramm Gesamtstickstoff je Hektar und Jahr aufgebracht werden.", "Grenzwert / Verbot", "Betriebsinhaber", "begrenzen", "Gesamtstickstoff aus organischen und organisch-mineralischen Düngemitteln", "Flächen liegen in ausgewiesenen Gebieten nach § 13a Abs. 1 Nr. 1 bis 3 DüV; keine Ausnahme greift", "je Hektar und Jahr", "Düngedokumentation / Flächenberechnung", "Business Rule"),
            req("DUEV-013A-002-005", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 3 DüV", "1. Oktober bis ... 31. Januar", "In ausgewiesenen Gebieten dürfen Düngemittel mit wesentlichem Stickstoffgehalt auf Grünland, Dauergrünland und Ackerland mit mehrjährigem Feldfutterbau vom 1. Oktober bis 31. Januar nicht aufgebracht werden.", "Verbot / Sperrfrist", "Anwender / Betriebsinhaber", "nicht aufbringen", "stickstoffhaltige Düngemittel", "Flächen nach § 6 Abs. 8 Satz 1 Nr. 2 in ausgewiesenen Gebieten", "1. Oktober bis 31. Januar", "Düngedokumentation / Flächenstatus", "Business Rule; Timer Event"),
            req("DUEV-013A-002-006", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 4 DüV", "1. November bis ... 31. Januar", "In ausgewiesenen Gebieten dürfen Festmist von Huftieren oder Klauentieren und Kompost vom 1. November bis 31. Januar nicht aufgebracht werden.", "Verbot / Sperrfrist", "Anwender / Betriebsinhaber", "nicht aufbringen", "Festmist von Huftieren oder Klauentieren und Kompost", "ausgewiesene Gebiete nach § 13a DüV", "1. November bis 31. Januar", "Düngedokumentation", "Business Rule; Timer Event"),
            req("DUEV-013A-002-007", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 5 DüV", "Winterraps, Wintergerste und Zwischenfrüchten ohne Futternutzung nicht aufgebracht", "In ausgewiesenen Gebieten dürfen Düngemittel mit wesentlichem Stickstoffgehalt zu Winterraps, Wintergerste und Zwischenfrüchten ohne Futternutzung grundsätzlich nicht aufgebracht werden.", "Verbot / Ausnahme", "Anwender / Betriebsinhaber", "nicht aufbringen", "stickstoffhaltige Düngemittel", "Winterraps, Wintergerste oder Zwischenfrüchte ohne Futternutzung in ausgewiesenen Gebieten; Ausnahmen können greifen", "", "Düngedokumentation / ggf. Bodenprobe", "Gateway; Business Rule"),
            req("DUEV-013A-002-008", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 5 DüV", "Bodenprobe ... 45 Kilogramm", "Bei Winterraps gilt das Aufbringungsverbot in ausgewiesenen Gebieten nicht, wenn eine repräsentative Bodenprobe nachweist, dass die verfügbare Stickstoffmenge höchstens 45 Kilogramm je Hektar beträgt.", "Ausnahmebedingung / Nachweis", "Betriebsinhaber", "nachweisen", "verfügbare Stickstoffmenge im Boden", "Winterraps in ausgewiesenen Gebieten; Inanspruchnahme der Ausnahme", "", "repräsentative Bodenprobe", "Gateway; Data Object"),
            req("DUEV-013A-002-009", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 5 DüV", "nicht mehr als 120 Kilogramm Gesamtstickstoff", "Bei Zwischenfrüchten ohne Futternutzung gilt die Ausnahme für Festmist von Huftieren oder Klauentieren oder Kompost nur, wenn nicht mehr als 120 Kilogramm Gesamtstickstoff je Hektar aufgebracht werden.", "Grenzwert / Ausnahmebedingung", "Anwender / Betriebsinhaber", "begrenzen", "Gesamtstickstoff", "Zwischenfrüchte ohne Futternutzung in ausgewiesenen Gebieten; Festmist oder Kompost", "", "Düngedokumentation", "Business Rule"),
            req("DUEV-013A-002-010", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 6 DüV", "nicht mehr als 60 Kilogramm Gesamtstickstoff je Hektar", "In ausgewiesenen Gebieten dürfen auf Grünland, Dauergrünland und Ackerland mit mehrjährigem Feldfutterbau vom 1. September bis zum Beginn des Verbotszeitraums mit flüssigen organischen oder flüssigen organisch-mineralischen Düngemitteln höchstens 60 Kilogramm Gesamtstickstoff je Hektar aufgebracht werden.", "Grenzwert / Zeitraum", "Anwender / Betriebsinhaber", "begrenzen", "Gesamtstickstoff aus flüssigen organischen oder flüssigen organisch-mineralischen Düngemitteln", "ausgewiesene Gebiete; wesentlicher Gehalt an verfügbarem Stickstoff oder Ammoniumstickstoff", "1. September bis Beginn des Verbotszeitraums", "Düngedokumentation", "Business Rule; Timer Event"),
            req("DUEV-013A-002-011", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 7 DüV", "nur ... wenn ... Zwischenfrucht angebaut wurde", "Bei Kulturen mit Aussaat oder Pflanzung nach dem 1. Februar dürfen in ausgewiesenen Gebieten Düngemittel mit wesentlichem Stickstoffgehalt nur aufgebracht werden, wenn im Herbst des Vorjahres eine Zwischenfrucht angebaut wurde.", "Bedingte Anwendungsvorgabe", "Anwender / Betriebsinhaber", "aufbringen", "stickstoffhaltige Düngemittel", "Kultur mit Aussaat oder Pflanzung nach dem 1. Februar in ausgewiesenen Gebieten; keine Ausnahme greift", "", "Anbau-/Flächendokumentation", "Gateway; Business Rule"),
            req("DUEV-013A-002-012", DC_DUEV, SRC_DUEV, "§ 13a Abs. 2 Nr. 7 DüV", "nicht vor dem 15. Januar umgebrochen", "Die Zwischenfrucht nach § 13a Abs. 2 Nr. 7 DüV darf nicht vor dem 15. Januar umgebrochen worden sein.", "Bedingung / Frist", "Betriebsinhaber", "nicht umbrechen", "Zwischenfrucht", "Inanspruchnahme der Düngung bei Kulturen mit Aussaat oder Pflanzung nach dem 1. Februar in ausgewiesenen Gebieten", "nicht vor dem 15. Januar", "Anbau-/Flächendokumentation", "Business Rule; Timer Event"),
        ],
    )

    print("Second batch extraction drafts written.")


if __name__ == "__main__":
    main()
