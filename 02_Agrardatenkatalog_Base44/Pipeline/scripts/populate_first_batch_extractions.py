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


def write_job(job_name: str, rows: list[dict]) -> None:
    job_dir = JOBS / job_name
    job_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows, columns=COLUMNS)
    df.to_csv(job_dir / "atomic_requirements_output.csv", index=False, encoding="utf-8-sig")


def empty_job(job_name: str, note: str) -> None:
    write_job(job_name, [])
    (JOBS / job_name / "extraction_notes.md").write_text(note, encoding="utf-8")


def req(
    rid: str,
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
        "Data_Collection_ID": DC_DUEV,
        "Source_Document_ID": SRC_DUEV,
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


def duev_3_rows() -> list[dict]:
    ref = "§ 3 DüV"
    return [
        req("DUEV-003-001-001", ref, "§ 3 Abs. 1 Satz 1", "Der Betriebsinhaber muss die Anwendung von Düngemitteln, Bodenhilfsstoffen, Kultursubstraten und Pflanzenhilfsmitteln unter Berücksichtigung der Standortbedingungen auf ein Gleichgewicht zwischen voraussichtlichem Nährstoffbedarf der Pflanzen und Nährstoffversorgung aus Boden und Düngung ausrichten.", "Bewirtschaftungspflicht", "Betriebsinhaber", "ausrichten", "Anwendung von Düngemitteln, Bodenhilfsstoffen, Kultursubstraten und Pflanzenhilfsmitteln", evidence="Düngeplanung / Düngebedarfsermittlung"),
        req("DUEV-003-001-002", ref, "§ 3 Abs. 1 Satz 2", "Der Betriebsinhaber muss Aufbringungszeitpunkt und Aufbringungsmenge so wählen, dass verfügbare oder verfügbar werdende Nährstoffe den Pflanzen zeitgerecht zur Verfügung stehen.", "Bewirtschaftungspflicht", "Betriebsinhaber", "wählen", "Aufbringungszeitpunkt und Aufbringungsmenge", evidence="Düngeplanung / Düngedokumentation"),
        req("DUEV-003-001-003", ref, "§ 3 Abs. 1 Satz 2", "Der Betriebsinhaber muss Aufbringungszeitpunkt und Aufbringungsmenge so wählen, dass die Nährstoffmenge dem Nährstoffbedarf der Pflanzen entspricht.", "Bewirtschaftungspflicht", "Betriebsinhaber", "wählen", "Aufbringungsmenge", evidence="Düngebedarfsermittlung / Düngedokumentation"),
        req("DUEV-003-001-004", ref, "§ 3 Abs. 1 Satz 2", "Der Betriebsinhaber muss Aufbringungszeitpunkt und Aufbringungsmenge so wählen, dass Einträge in oberirdische Gewässer und das Grundwasser vermieden werden.", "Schutzpflicht", "Betriebsinhaber", "vermeiden", "Einträge in oberirdische Gewässer und Grundwasser", evidence="Düngeplanung / Flächen- und Gewässerabstandsdokumentation"),
        req("DUEV-003-001-005", ref, "§ 3 Abs. 1 Satz 4", "Der Betriebsinhaber muss Erfordernisse für die Erhaltung der standortbezogenen Bodenfruchtbarkeit zusätzlich berücksichtigen.", "Bewirtschaftungspflicht", "Betriebsinhaber", "berücksichtigen", "standortbezogene Bodenfruchtbarkeit", evidence="Düngeplanung / Bodeninformationen"),
        req("DUEV-003-002-001", ref, "§ 3 Abs. 2 Satz 1", "Der Betriebsinhaber muss vor dem Aufbringen wesentlicher Nährstoffmengen an Stickstoff mit Düngemitteln, Bodenhilfsstoffen, Kultursubstraten oder Pflanzenhilfsmitteln den Düngebedarf der Kultur für jeden Schlag oder jede Bewirtschaftungseinheit nach § 4 DüV ermitteln.", "Dokumentationspflicht / Frist", "Betriebsinhaber", "ermitteln", "Düngebedarf der Kultur", "Vor Aufbringen wesentlicher Nährstoffmengen an Stickstoff", "vor dem Aufbringen", "Düngebedarfsermittlung", "Task; Timer Event; Data Object"),
        req("DUEV-003-002-002", ref, "§ 3 Abs. 2 Satz 1", "Der Betriebsinhaber muss vor dem Aufbringen wesentlicher Nährstoffmengen an Phosphat mit Düngemitteln, Bodenhilfsstoffen, Kultursubstraten oder Pflanzenhilfsmitteln den Düngebedarf der Kultur für jeden Schlag oder jede Bewirtschaftungseinheit nach § 4 DüV ermitteln.", "Dokumentationspflicht / Frist", "Betriebsinhaber", "ermitteln", "Düngebedarf der Kultur", "Vor Aufbringen wesentlicher Nährstoffmengen an Phosphat", "vor dem Aufbringen", "Düngebedarfsermittlung", "Task; Timer Event; Data Object"),
        req("DUEV-003-002-003", ref, "§ 3 Abs. 2 Satz 2", "Die Pflicht zur Düngebedarfsermittlung nach § 3 Abs. 2 Satz 1 DüV gilt nicht für die in § 10 Abs. 3 DüV genannten Flächen und Betriebe.", "Ausnahme", "Betriebsinhaber", "prüfen", "Ausnahme von der Düngebedarfsermittlung", "Fläche oder Betrieb fällt unter § 10 Abs. 3 DüV", evidence="Nachweis Ausnahmevoraussetzungen", notes="Ausnahme bleibt als eigene Regel erhalten."),
        req("DUEV-003-002-004", ref, "§ 3 Abs. 2 Satz 2", "Die Pflicht zur Düngebedarfsermittlung für Phosphat gilt nicht für Schläge, die kleiner als ein Hektar sind.", "Ausnahme", "Betriebsinhaber", "prüfen", "Ausnahme von der Phosphat-Düngebedarfsermittlung", "Schlag ist kleiner als 1 Hektar", evidence="Flächennachweis"),
        req("DUEV-003-002-005", ref, "§ 3 Abs. 2 Satz 3", "Beim Anbau von Gemüse- und Erdbeerkulturen darf der Betriebsinhaber mehrere Schläge und Bewirtschaftungseinheiten, die jeweils kleiner als 0,5 Hektar sind, für die Stickstoff-Düngebedarfsermittlung zusammenfassen.", "Erlaubnis / Option", "Betriebsinhaber", "zusammenfassen", "Schläge und Bewirtschaftungseinheiten", "Gemüse- oder Erdbeerkulturen; Einzelflächen jeweils kleiner als 0,5 Hektar", evidence="Flächennachweis / Düngebedarfsermittlung"),
        req("DUEV-003-002-006", ref, "§ 3 Abs. 2 Satz 3", "Die zusammengefasste Fläche für die Stickstoff-Düngebedarfsermittlung bei Gemüse- und Erdbeerkulturen darf höchstens zwei Hektar betragen.", "Grenzwert", "Betriebsinhaber", "einhalten", "zusammengefasste Fläche", "Zusammenfassung kleiner Schläge und Bewirtschaftungseinheiten", evidence="Flächennachweis / Düngebedarfsermittlung"),
        req("DUEV-003-002-007", ref, "§ 3 Abs. 2 Satz 4", "Bei satzweisem Anbau von Gemüsekulturen muss der Betriebsinhaber bis zu drei Düngebedarfsermittlungen im Abstand von höchstens jeweils sechs Wochen durchführen.", "Dokumentationspflicht / Frist", "Betriebsinhaber", "durchführen", "Düngebedarfsermittlungen", "satzweiser Anbau von Gemüsekulturen", "Abstand höchstens jeweils sechs Wochen", "Düngebedarfsermittlung", "Task; Timer Event; Data Object"),
        req("DUEV-003-002-008", ref, "§ 3 Abs. 2 Satz 4", "Bei satzweisem Anbau auf zusammengefassten Flächen muss der Betriebsinhaber mindestens für eine der satzweise angebauten Gemüsekulturen eine Düngebedarfsermittlung durchführen.", "Dokumentationspflicht", "Betriebsinhaber", "durchführen", "Düngebedarfsermittlung", "satzweiser Anbau auf zusammengefassten Flächen", evidence="Düngebedarfsermittlung"),
        req("DUEV-003-003-001", ref, "§ 3 Abs. 3 Satz 1", "Der Betriebsinhaber darf den nach § 3 Abs. 2 Satz 1 DüV ermittelten Düngebedarf im Rahmen der geplanten Düngungsmaßnahme nicht überschreiten.", "Verbot / Grenzwert", "Betriebsinhaber", "nicht überschreiten", "ermittelter Düngebedarf", "geplante Düngungsmaßnahme", evidence="Düngebedarfsermittlung / Düngedokumentation"),
        req("DUEV-003-003-002", ref, "§ 3 Abs. 3 Satz 3", "Der Betriebsinhaber darf den ermittelten Düngebedarf um höchstens 10 Prozent überschreiten, wenn auf Grund nachträglich eintretender Umstände ein höherer Düngebedarf besteht.", "Bedingte Erlaubnis / Grenzwert", "Betriebsinhaber", "überschreiten", "ermittelter Düngebedarf", "nachträglich eintretende Umstände, insbesondere Bestandsentwicklung oder Witterungsereignisse", evidence="Dokumentation höherer Düngebedarf / Düngedokumentation"),
        req("DUEV-003-003-003", ref, "§ 3 Abs. 3 Satz 4 Nr. 1", "Vor einer Überschreitung des Düngebedarfs nach § 3 Abs. 3 Satz 3 DüV muss der Betriebsinhaber den Düngebedarf der Kultur für jeden Schlag oder jede Bewirtschaftungseinheit erneut nach § 4 DüV ermitteln.", "Dokumentationspflicht / Frist", "Betriebsinhaber", "erneut ermitteln", "Düngebedarf der Kultur", "Überschreitung nach § 3 Abs. 3 Satz 3 DüV", "vor dem Aufbringen", "erneute Düngebedarfsermittlung", "Task; Timer Event; Data Object"),
        req("DUEV-003-003-004", ref, "§ 3 Abs. 3 Satz 4 Nr. 2", "Vor einer Überschreitung des Düngebedarfs nach § 3 Abs. 3 Satz 3 DüV muss der Betriebsinhaber den Düngebedarf nach Maßgabe der nach Landesrecht zuständigen Stelle erneut ermitteln.", "Dokumentationspflicht / Frist", "Betriebsinhaber", "erneut ermitteln", "Düngebedarf", "Überschreitung nach § 3 Abs. 3 Satz 3 DüV", "vor dem Aufbringen", "erneute Düngebedarfsermittlung / Vorgaben zuständige Stelle"),
        req("DUEV-003-004-001", ref, "§ 3 Abs. 4 Satz 1", "Der Betriebsinhaber darf Düngemittel, Bodenhilfsstoffe, Kultursubstrate oder Pflanzenhilfsmittel nur aufbringen, wenn ihm vor dem Aufbringen die Gehalte an Gesamtstickstoff, verfügbarem Stickstoff oder Ammoniumstickstoff und Gesamtphosphat bekannt sind oder von ihm ermittelt oder festgestellt wurden.", "Bedingte Erlaubnis / Dokumentationspflicht", "Betriebsinhaber", "prüfen", "Nährstoffgehalte", "vor dem Aufbringen", "vor dem Aufbringen", "Kennzeichnung / Daten zuständige Stelle / Messnachweis", "Task; Timer Event; Data Object"),
        req("DUEV-003-004-002", ref, "§ 3 Abs. 4 Satz 2", "Bei der Ermittlung der Nährstoffgehalte auf Grundlage von Daten der zuständigen Stelle muss der Betriebsinhaber für Wirtschaftsdünger tierischer Herkunft mindestens die Werte nach Anlage 1 und Anlage 2 Zeile 5 bis 9 Spalte 2 und 3 heranziehen.", "Dokumentationspflicht", "Betriebsinhaber", "heranziehen", "Mindestwerte für Wirtschaftsdünger tierischer Herkunft", "Ermittlung nach § 3 Abs. 4 Satz 1 Nr. 2 DüV", evidence="Nährstoffgehaltsermittlung"),
        req("DUEV-003-004-003", ref, "§ 3 Abs. 4 Satz 2", "Bei der Ermittlung der Nährstoffgehalte auf Grundlage von Daten der zuständigen Stelle muss der Betriebsinhaber für Gärrückstände aus dem Betrieb einer Biogasanlage mindestens die Werte nach Anlage 1 und Anlage 2 Zeile 5 bis 9 Spalte 2 und 3 heranziehen.", "Dokumentationspflicht", "Betriebsinhaber", "heranziehen", "Mindestwerte für Gärrückstände", "Ermittlung nach § 3 Abs. 4 Satz 1 Nr. 2 DüV", evidence="Nährstoffgehaltsermittlung"),
        req("DUEV-003-005-001", ref, "§ 3 Abs. 5 Satz 1 Nr. 1", "Der Betriebsinhaber muss bei mineralischen Düngemitteln die darin enthaltenen Stickstoffmengen im Jahr des Aufbringens in voller Höhe für die Ausnutzung des Stickstoffs ansetzen.", "Berechnungspflicht", "Betriebsinhaber", "ansetzen", "Stickstoffmengen mineralischer Düngemittel", "im Jahr des Aufbringens", evidence="Düngeberechnung"),
        req("DUEV-003-005-002", ref, "§ 3 Abs. 5 Satz 1 Nr. 2", "Der Betriebsinhaber muss bei organischen oder organisch-mineralischen Düngemitteln im Jahr des Aufbringens die Werte nach Anlage 3 für die Ausnutzung des Stickstoffs ansetzen.", "Berechnungspflicht", "Betriebsinhaber", "ansetzen", "Werte nach Anlage 3", "organische oder organisch-mineralische Düngemittel", evidence="Düngeberechnung"),
        req("DUEV-003-005-003", ref, "§ 3 Abs. 5 Satz 1 Nr. 2", "Der Betriebsinhaber muss bei organischen oder organisch-mineralischen Düngemitteln mindestens den nach § 3 Abs. 4 DüV ermittelten Gehalt an verfügbarem Stickstoff oder Ammoniumstickstoff ansetzen.", "Berechnungspflicht / Mindestwert", "Betriebsinhaber", "ansetzen", "verfügbarer Stickstoff oder Ammoniumstickstoff", "organische oder organisch-mineralische Düngemittel", evidence="Düngeberechnung / Nährstoffgehaltsermittlung"),
        req("DUEV-003-005-004", ref, "§ 3 Abs. 5 Satz 2", "Für in Anlage 3 nicht genannte Düngemittel muss der Betriebsinhaber die anzusetzenden Werte bei der nach Landesrecht zuständigen Stelle erfragen.", "Informationspflicht", "Betriebsinhaber", "erfragen", "anzusetzende Werte", "Düngemittel ist nicht in Anlage 3 genannt", evidence="Auskunft zuständige Stelle / Düngeberechnung"),
        req("DUEV-003-006-001", ref, "§ 3 Abs. 6 Satz 1", "Auf Schlägen mit erhöhtem Phosphatgehalt darf der Betriebsinhaber phosphathaltige Düngemittel höchstens bis zur Höhe der voraussichtlichen Phosphatabfuhr aufbringen.", "Verbot / Grenzwert", "Betriebsinhaber", "begrenzen", "Aufbringung phosphathaltiger Düngemittel", "Phosphatgehalt überschreitet einen Schwellenwert nach CAL-, DL- oder EUF-Verfahren", evidence="Bodenuntersuchung / Phosphatabfuhrermittlung"),
        req("DUEV-003-006-002", ref, "§ 3 Abs. 6 Satz 1", "Der Betriebsinhaber darf die voraussichtliche Phosphatabfuhr im Rahmen einer Fruchtfolge für höchstens drei Jahre zugrunde legen.", "Grenzwert / Berechnungspflicht", "Betriebsinhaber", "zugrunde legen", "voraussichtliche Phosphatabfuhr", "Berechnung im Rahmen einer Fruchtfolge", "höchstens drei Jahre", "Phosphatabfuhrermittlung"),
        req("DUEV-003-006-003", ref, "§ 3 Abs. 6 Satz 2", "Bei der Ermittlung der Phosphatabfuhr muss der Betriebsinhaber die Phosphatgehalte pflanzlicher Erzeugnisse nach Anlage 7 Tabelle 1 bis 3 heranziehen.", "Berechnungspflicht", "Betriebsinhaber", "heranziehen", "Phosphatgehalte pflanzlicher Erzeugnisse", "Ermittlung der Phosphatabfuhr", evidence="Phosphatabfuhrermittlung"),
    ]


def duev_5_rows() -> list[dict]:
    ref = "§ 5 DüV"
    return [
        req("DUEV-005-001-001", ref, "§ 5 Abs. 1 Satz 1", "Der Betriebsinhaber darf stickstoff- oder phosphathaltige Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel nicht aufbringen, wenn der Boden überschwemmt ist.", "Verbot", "Betriebsinhaber", "nicht aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Boden ist überschwemmt", evidence="Flächen-/Witterungsdokumentation"),
        req("DUEV-005-001-002", ref, "§ 5 Abs. 1 Satz 1", "Der Betriebsinhaber darf stickstoff- oder phosphathaltige Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel nicht aufbringen, wenn der Boden wassergesättigt ist.", "Verbot", "Betriebsinhaber", "nicht aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Boden ist wassergesättigt", evidence="Flächen-/Witterungsdokumentation"),
        req("DUEV-005-001-003", ref, "§ 5 Abs. 1 Satz 1", "Der Betriebsinhaber darf stickstoff- oder phosphathaltige Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel nicht aufbringen, wenn der Boden gefroren ist.", "Verbot", "Betriebsinhaber", "nicht aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Boden ist gefroren", evidence="Flächen-/Witterungsdokumentation"),
        req("DUEV-005-001-004", ref, "§ 5 Abs. 1 Satz 1", "Der Betriebsinhaber darf stickstoff- oder phosphathaltige Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel nicht aufbringen, wenn der Boden schneebedeckt ist.", "Verbot", "Betriebsinhaber", "nicht aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Boden ist schneebedeckt", evidence="Flächen-/Witterungsdokumentation"),
        req("DUEV-005-001-005", ref, "§ 5 Abs. 1 Satz 2", "Der Betriebsinhaber darf Kalkdünger mit weniger als zwei Prozent Phosphat auf gefrorenen Boden aufbringen, soweit ein Abschwemmen in oberirdische Gewässer oder auf benachbarte Flächen nicht zu besorgen ist.", "Bedingte Erlaubnis", "Betriebsinhaber", "aufbringen", "Kalkdünger", "Kalkdünger enthält weniger als 2 Prozent Phosphat; Boden ist gefroren; kein Abschwemmen zu besorgen", evidence="Düngemittelkennzeichnung / Flächen- und Witterungsdokumentation"),
        req("DUEV-005-002-001", ref, "§ 5 Abs. 2 Satz 1 Nr. 1", "Beim Aufbringen stickstoff- oder phosphathaltiger Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel muss der Betriebsinhaber einen direkten Eintrag und ein Abschwemmen von Nährstoffen in oberirdische Gewässer vermeiden.", "Schutzpflicht", "Betriebsinhaber", "vermeiden", "Eintrag und Abschwemmen in oberirdische Gewässer", evidence="Flächen-/Gewässerabstandsdokumentation"),
        req("DUEV-005-002-002", ref, "§ 5 Abs. 2 Satz 1 Nr. 2", "Beim Aufbringen stickstoff- oder phosphathaltiger Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel muss der Betriebsinhaber dafür sorgen, dass kein direkter Eintrag und kein Abschwemmen von Nährstoffen auf benachbarte Flächen erfolgt.", "Schutzpflicht", "Betriebsinhaber", "verhindern", "Eintrag und Abschwemmen auf benachbarte Flächen", evidence="Flächen-/Abstandsdokumentation"),
        req("DUEV-005-002-003", ref, "§ 5 Abs. 2 Satz 1 Nr. 2", "Beim Aufbringen stickstoff- oder phosphathaltiger Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel muss der Betriebsinhaber insbesondere dafür sorgen, dass kein direkter Eintrag und kein Abschwemmen von Nährstoffen in schützenswerte natürliche Lebensräume erfolgt.", "Schutzpflicht", "Betriebsinhaber", "verhindern", "Eintrag und Abschwemmen in schützenswerte natürliche Lebensräume", evidence="Flächen-/Schutzgebietsdokumentation"),
        req("DUEV-005-002-004", ref, "§ 5 Abs. 2 Satz 2", "Der Betriebsinhaber muss zwischen dem Rand der durch die Streubreite bestimmten Aufbringungsfläche und der Böschungsoberkante des jeweiligen oberirdischen Gewässers einen Abstand von mindestens vier Metern einhalten.", "Abstandspflicht / Grenzwert", "Betriebsinhaber", "einhalten", "Gewässerabstand", "Aufbringen stickstoff- oder phosphathaltiger Stoffe", evidence="Flächen-/Gewässerabstandsdokumentation"),
        req("DUEV-005-002-005", ref, "§ 5 Abs. 2 Satz 3", "Der Betriebsinhaber muss beim Einsatz von Geräten, deren Streubreite der Arbeitsbreite entspricht oder die über eine Grenzstreueinrichtung verfügen, einen Abstand von mindestens einem Meter zur Böschungsoberkante des jeweiligen oberirdischen Gewässers einhalten.", "Abstandspflicht / Grenzwert", "Betriebsinhaber", "einhalten", "Gewässerabstand", "Gerät mit Streubreite gleich Arbeitsbreite oder Grenzstreueinrichtung", evidence="Maschinennachweis / Gewässerabstandsdokumentation"),
        req("DUEV-005-002-006", ref, "§ 5 Abs. 2 Satz 4", "Der Betriebsinhaber darf innerhalb eines Abstandes von einem Meter zur Böschungsoberkante eines oberirdischen Gewässers keine stickstoff- oder phosphathaltigen Düngemittel, Bodenhilfsstoffe, Kultursubstrate oder Pflanzenhilfsmittel aufbringen.", "Verbot / Abstandspflicht", "Betriebsinhaber", "nicht aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Abstand von einem Meter zur Böschungsoberkante eines oberirdischen Gewässers", evidence="Flächen-/Gewässerabstandsdokumentation"),
        req("DUEV-005-003-001", ref, "§ 5 Abs. 3 Satz 1 Nr. 1", "Der Betriebsinhaber darf stickstoff- oder phosphathaltige Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel nicht innerhalb von 3 Metern zur Böschungsoberkante eines oberirdischen Gewässers aufbringen, wenn die Fläche innerhalb von 20 Metern zur Böschungsoberkante eine durchschnittliche Hangneigung von mindestens 5 Prozent aufweist.", "Verbot / Abstandspflicht", "Betriebsinhaber", "nicht aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Hangneigung mindestens 5 Prozent innerhalb von 20 Metern zur Böschungsoberkante", evidence="Hangneigungs-/Gewässerabstandsdokumentation"),
        req("DUEV-005-003-002", ref, "§ 5 Abs. 3 Satz 1 Nr. 2", "Der Betriebsinhaber darf stickstoff- oder phosphathaltige Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel nicht innerhalb von 5 Metern zur Böschungsoberkante eines oberirdischen Gewässers aufbringen, wenn die Fläche innerhalb von 20 Metern zur Böschungsoberkante eine durchschnittliche Hangneigung von mindestens 10 Prozent aufweist.", "Verbot / Abstandspflicht", "Betriebsinhaber", "nicht aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Hangneigung mindestens 10 Prozent innerhalb von 20 Metern zur Böschungsoberkante", evidence="Hangneigungs-/Gewässerabstandsdokumentation"),
        req("DUEV-005-003-003", ref, "§ 5 Abs. 3 Satz 1 Nr. 3", "Der Betriebsinhaber darf stickstoff- oder phosphathaltige Düngemittel, Bodenhilfsstoffe, Kultursubstrate und Pflanzenhilfsmittel nicht innerhalb von 10 Metern zur Böschungsoberkante eines oberirdischen Gewässers aufbringen, wenn die Fläche innerhalb von 30 Metern zur Böschungsoberkante eine durchschnittliche Hangneigung von mindestens 15 Prozent aufweist.", "Verbot / Abstandspflicht", "Betriebsinhaber", "nicht aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Hangneigung mindestens 15 Prozent innerhalb von 30 Metern zur Böschungsoberkante", evidence="Hangneigungs-/Gewässerabstandsdokumentation"),
        req("DUEV-005-003-004", ref, "§ 5 Abs. 3 Satz 2 Nr. 1", "Auf unbestellten Ackerflächen in den hangneigungsbezogenen Abstandsbereichen nach § 5 Abs. 3 Satz 2 DüV darf der Betriebsinhaber die genannten Stoffe vor der Aussaat oder Pflanzung nur bei sofortiger Einarbeitung aufbringen.", "Bedingte Erlaubnis", "Betriebsinhaber", "aufbringen", "stickstoff- oder phosphathaltige Stoffe", "unbestellte Ackerfläche im hangneigungsbezogenen Abstandsbereich", evidence="Düngedokumentation / Einarbeitungsnachweis"),
        req("DUEV-005-003-005", ref, "§ 5 Abs. 3 Satz 2 Nr. 2 Buchst. a", "Auf bestellten Ackerflächen mit Reihenkultur mit einem Reihenabstand von 45 Zentimetern und mehr in den hangneigungsbezogenen Abstandsbereichen darf der Betriebsinhaber die genannten Stoffe nur bei entwickelter Untersaat oder bei sofortiger Einarbeitung aufbringen.", "Bedingte Erlaubnis", "Betriebsinhaber", "aufbringen", "stickstoff- oder phosphathaltige Stoffe", "bestellte Ackerfläche mit Reihenkultur; Reihenabstand mindestens 45 Zentimeter; hangneigungsbezogener Abstandsbereich", evidence="Flächen-/Kultur-/Einarbeitungsdokumentation"),
        req("DUEV-005-003-006", ref, "§ 5 Abs. 3 Satz 2 Nr. 2 Buchst. b", "Auf bestellten Ackerflächen ohne Reihenkultur nach § 5 Abs. 3 Satz 2 Nr. 2 Buchst. a DüV darf der Betriebsinhaber die genannten Stoffe nur bei hinreichender Bestandsentwicklung aufbringen.", "Bedingte Erlaubnis", "Betriebsinhaber", "aufbringen", "stickstoff- oder phosphathaltige Stoffe", "bestellte Ackerfläche ohne entsprechende Reihenkultur; hangneigungsbezogener Abstandsbereich", evidence="Bestandsdokumentation"),
        req("DUEV-005-003-007", ref, "§ 5 Abs. 3 Satz 2 Nr. 2 Buchst. c", "Auf bestellten Ackerflächen in den hangneigungsbezogenen Abstandsbereichen darf der Betriebsinhaber die genannten Stoffe nach Anwendung von Mulchsaat- oder Direktsaatverfahren aufbringen.", "Bedingte Erlaubnis", "Betriebsinhaber", "aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Mulchsaat- oder Direktsaatverfahren; hangneigungsbezogener Abstandsbereich", evidence="Verfahrensdokumentation"),
        req("DUEV-005-003-008", ref, "§ 5 Abs. 3 Satz 3", "Auf Ackerflächen mit einer Hangneigung nach § 5 Abs. 3 Satz 1 Nr. 3 DüV, die unbestellt sind oder keinen hinreichend entwickelten Pflanzenbestand haben, darf der Betriebsinhaber die genannten Stoffe nur bei sofortiger Einarbeitung auf der gesamten Ackerfläche des Schlages aufbringen.", "Bedingte Erlaubnis", "Betriebsinhaber", "aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Hangneigung mindestens 15 Prozent; Ackerfläche unbestellt oder ohne hinreichend entwickelten Pflanzenbestand", evidence="Hangneigungs-/Bestands-/Einarbeitungsdokumentation"),
        req("DUEV-005-003-009", ref, "§ 5 Abs. 3 Satz 4", "Auf Flächen mit einer Hangneigung nach § 5 Abs. 3 Satz 1 Nr. 2 oder 3 DüV und einem ermittelten Düngebedarf von mehr als 80 Kilogramm Gesamtstickstoff je Hektar darf der Betriebsinhaber die genannten Stoffe nur in Teilgaben aufbringen.", "Bedingte Erlaubnis / Grenzwert", "Betriebsinhaber", "in Teilgaben aufbringen", "stickstoff- oder phosphathaltige Stoffe", "Hangneigung mindestens 10 Prozent oder 15 Prozent; Düngebedarf mehr als 80 kg Gesamtstickstoff je Hektar", evidence="Düngebedarfsermittlung / Hangneigungsdokumentation"),
        req("DUEV-005-003-010", ref, "§ 5 Abs. 3 Satz 4", "Die einzelnen Teilgaben nach § 5 Abs. 3 Satz 4 DüV dürfen jeweils 80 Kilogramm Gesamtstickstoff je Hektar nicht überschreiten.", "Grenzwert", "Betriebsinhaber", "nicht überschreiten", "Teilgabe Gesamtstickstoff", "Teilgabe auf Flächen mit Hangneigung nach § 5 Abs. 3 Satz 1 Nr. 2 oder 3 DüV", evidence="Düngedokumentation"),
        req("DUEV-005-004-001", ref, "§ 5 Abs. 4", "Die Abstands- und Hangneigungsregelungen nach § 5 Abs. 2 und 3 DüV gelten nicht für Gewässer, die nach § 2 Abs. 2 Wasserhaushaltsgesetz von dessen Anwendung ausgenommen sind.", "Ausnahme", "Betriebsinhaber", "prüfen", "Ausnahme von Abstands- und Hangneigungsregelungen", "Gewässer ist nach § 2 Abs. 2 WHG ausgenommen", evidence="Gewässerstatus / Flächendokumentation"),
    ]


def main() -> None:
    write_job("JOB_LINK_0052_SEC_0003", duev_3_rows())
    write_job("JOB_LINK_0052_SEC_0005", duev_5_rows())
    empty_job(
        "JOB_LINK_0052_SEC_0024",
        "# Extraction Notes\n\nAnlage 8 listet Geräte, die nicht den allgemein anerkannten Regeln der Technik entsprechen. Die direkte Pflicht ergibt sich aus § 11 Satz 2 DüV; die Anlage wird als Referenzmaterial behandelt und hier nicht als eigenständige Landwirtspflicht atomisiert.\n",
    )
    empty_job(
        "JOB_LINK_0001_SEC_0020",
        "# Extraction Notes\n\n§ 19 GAPDZG regelt Mittel für Öko-Regelungen und richtet sich an staatliche Stellen. Keine direkte Pflicht des Landwirts auf Betriebsebene extrahiert.\n",
    )
    empty_job(
        "JOB_LINK_0002_SEC_0015",
        "# Extraction Notes\n\n§ 15 GAPDZV regelt Mittel für Öko-Regelungen und richtet sich nicht unmittelbar als Betriebspflicht an den Landwirt. Keine direkte Pflicht des Landwirts extrahiert.\n",
    )
    print("first batch populated")


if __name__ == "__main__":
    main()
