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

DC_SACHK = "DC_017_PFLANZENSCHUTZ_SACHKUNDEVERORDNUNG_PFLSCHS"
SRC_SACHK = "SRC_PFLANZENSCHUTZ_SACHKUNDEVERORDNUNG_PFLSCHSACHKV"
DC_WEIN = "DC_018_WEINBAUKARTEI"
SRC_WEING = "SRC_WEINGESETZ"
SRC_WEINUEV = "SRC_WEIN_UEBERWACHUNGSVERORDNUNG"


def write_job(job_name: str, rows: list[dict]) -> None:
    job_dir = JOBS / job_name
    job_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=COLUMNS).to_csv(
        job_dir / "atomic_requirements_output.csv",
        index=False,
        encoding="utf-8-sig",
    )


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


def main() -> None:
    write_job(
        "JOB_LINK_0056_SEC_0001",
        [
            req("PFLSCHSACHK-001-001-001", DC_SACHK, SRC_SACHK, "§ 1 Abs. 1 PflSchSachkV", "Mit dem Antrag ... ist der Nachweis ... zu erbringen", "Wer einen Sachkundenachweis für Tätigkeiten nach § 9 Abs. 1 Nr. 1 bis 3 PflSchG beantragt, muss mit dem Antrag die erforderlichen fachlichen Kenntnisse und praktischen Fertigkeiten nachweisen.", "Nachweispflicht / Antrag", "Antragsteller", "nachweisen", "fachliche Kenntnisse und praktische Fertigkeiten", "Antrag auf Ausstellung eines Sachkundenachweises für Tätigkeiten nach § 9 Abs. 1 Nr. 1 bis 3 PflSchG", "mit dem Antrag", "Zeugnis, Bescheinigung oder gleichwertiger Nachweis", "Task; Data Object"),
            req("PFLSCHSACHK-001-001-002", DC_SACHK, SRC_SACHK, "§ 1 Abs. 1 Nr. 1 PflSchSachkV", "Vorlage eines Zeugnisses", "Der Antragsteller kann den Nachweis für Tätigkeiten nach § 9 Abs. 1 Nr. 1 bis 3 PflSchG durch Vorlage eines Zeugnisses über eine erfolgreich abgeschlossene Prüfung nach § 3 PflSchSachkV erbringen.", "Nachweisoption", "Antragsteller", "vorlegen", "Zeugnis über erfolgreich abgeschlossene Prüfung", "Sachkundenachweis für Tätigkeiten nach § 9 Abs. 1 Nr. 1 bis 3 PflSchG", "mit dem Antrag", "Prüfungszeugnis", "Data Object"),
            req("PFLSCHSACHK-001-001-003", DC_SACHK, SRC_SACHK, "§ 1 Abs. 1 Nr. 2 PflSchSachkV", "Berufsausbildung nach Anlage 2 Teil A", "Der Antragsteller kann den Nachweis für Tätigkeiten nach § 9 Abs. 1 Nr. 1 bis 3 PflSchG durch Vorlage eines Zeugnisses über eine mit Prüfung abgeschlossene Berufsausbildung nach Anlage 2 Teil A erbringen.", "Nachweisoption", "Antragsteller", "vorlegen", "Zeugnis über abgeschlossene Berufsausbildung", "Sachkundenachweis für Tätigkeiten nach § 9 Abs. 1 Nr. 1 bis 3 PflSchG", "mit dem Antrag", "Ausbildungszeugnis", "Data Object"),
            req("PFLSCHSACHK-001-002-001", DC_SACHK, SRC_SACHK, "§ 1 Abs. 2 PflSchSachkV", "Mit dem Antrag ... Tätigkeit im Sinne ... Nummer 4 und 5", "Wer einen Sachkundenachweis für Tätigkeiten nach § 9 Abs. 1 Nr. 4 und 5 PflSchG beantragt, muss mit dem Antrag die erforderlichen fachlichen Kenntnisse und praktischen Fertigkeiten nachweisen.", "Nachweispflicht / Antrag", "Antragsteller", "nachweisen", "fachliche Kenntnisse und praktische Fertigkeiten", "Antrag auf Ausstellung eines Sachkundenachweises für Tätigkeiten nach § 9 Abs. 1 Nr. 4 und 5 PflSchG", "mit dem Antrag", "Zeugnis, Bescheinigung oder gleichwertiger Nachweis", "Task; Data Object"),
            req("PFLSCHSACHK-001-005-001", DC_SACHK, SRC_SACHK, "§ 1 Abs. 5 PflSchSachkV", "zusätzlich durch die Teilnahme ... nachzuweisen", "Wenn ein relevantes Zeugnis nach dem 14. Februar 2012, aber mehr als drei Jahre vor Antragstellung ausgestellt wurde, muss der Antragsteller die erforderlichen fachlichen Kenntnisse zusätzlich durch Teilnahme an einer Fort- oder Weiterbildungsmaßnahme innerhalb der letzten drei Jahre nachweisen.", "Nachweispflicht / Frist", "Antragsteller", "nachweisen", "Teilnahme an Fort- oder Weiterbildungsmaßnahme", "Zeugnis nach § 1 Abs. 1 Nr. 2 oder 3 oder Abs. 2 Nr. 2 oder 3; Ausstellung mehr als drei Jahre vor Antragstellung", "innerhalb der letzten drei Jahre", "Teilnahmebescheinigung Fort-/Weiterbildung", "Gateway; Task; Data Object"),
        ],
    )

    write_job(
        "JOB_LINK_0056_SEC_0002",
        [
            req("PFLSCHSACHK-002-001-001", DC_SACHK, SRC_SACHK, "§ 2 Abs. 1 PflSchSachkV", "Sachkundenachweis ... enthält folgende Angaben", "Der Sachkundenachweis muss die in § 2 Abs. 1 Nr. 1 bis 7 PflSchSachkV genannten Angaben enthalten.", "Datenanforderung", "zuständige Behörde", "angeben", "Angaben im Sachkundenachweis", "Ausstellung eines Sachkundenachweises", "", "Sachkundenachweis", "Data Object", "Behördenpflicht; für Katalog relevant als Datenstruktur des Nachweises."),
        ],
    )

    write_job(
        "JOB_LINK_0056_SEC_0005",
        [
            req("PFLSCHSACHK-005-001-001", DC_SACHK, SRC_SACHK, "§ 5 Abs. 1 PflSchSachkV", "wenn der Antragsteller eine Prüfung nach § 3 bestanden hat", "Nach Entzug des Sachkundenachweises wird ein neuer Sachkundenachweis nur ausgestellt, wenn der Antragsteller eine Prüfung nach § 3 PflSchSachkV bestanden hat und künftig die erforderliche Zuverlässigkeit erwartet werden kann.", "Bedingung / Wiedererlangung", "Antragsteller", "bestehen", "Prüfung nach § 3 PflSchSachkV", "Wiedererlangung der Sachkunde nach Entzug", "", "Prüfungszeugnis / Zuverlässigkeitsprüfung", "Gateway; Data Object"),
            req("PFLSCHSACHK-005-002-001", DC_SACHK, SRC_SACHK, "§ 5 Abs. 2 PflSchSachkV", "frühestens sechs Monate vor Ablauf ...", "Wenn dem Antragsteller auch die Abgabe von Pflanzenschutzmitteln untersagt wurde, darf er die Prüfung nach § 3 frühestens sechs Monate vor Ablauf der Sperrfrist ablegen.", "Frist / Sperrfrist", "Antragsteller", "ablegen", "Prüfung nach § 3 PflSchSachkV", "Untersagung der Abgabe von Pflanzenschutzmitteln nach § 23 Abs. 5 PflSchG", "frühestens sechs Monate vor Ablauf der Sperrfrist", "Sperrfristbescheid / Prüfungsnachweis", "Timer Event; Gateway"),
        ],
    )

    write_job(
        "JOB_LINK_0056_SEC_0008",
        [
            req("PFLSCHSACHK-008-001-001", DC_SACHK, SRC_SACHK, "§ 8 Satz 2 PflSchSachkV", "Diese Bescheinigung dient als Nachweis", "Die Teilnahmebescheinigung über eine Fort- oder Weiterbildungsmaßnahme dient als Nachweis im Sinne des § 9 Abs. 4 Satz 2 PflSchG.", "Nachweis", "Teilnehmer / sachkundige Person", "aufbewahren/vorlegen", "Teilnahmebescheinigung", "Fort- oder Weiterbildungsmaßnahme zur Sachkunde im Pflanzenschutz", "", "Teilnahmebescheinigung", "Data Object", "Der Abschnitt formuliert die Nachweisfunktion; die Aufbewahrungs-/Vorlagepflicht ergibt sich aus dem Kontrollkontext."),
        ],
    )

    write_job(
        "JOB_LINK_0058_SEC_0053",
        [
            req("WEING-033-001-001", DC_WEIN, SRC_WEING, "§ 33 Abs. 1 Nr. 1 Weingesetz", "Vorhaben ... zu melden sind", "Vorhaben, Rebflächen zu roden, aufzugeben, wiederzubepflanzen oder neu anzupflanzen, können den zuständigen Behörden meldepflichtig sein, soweit dies durch Rechtsverordnung vorgeschrieben ist.", "Bedingte Meldepflicht", "Betrieb / Bewirtschafter", "melden", "Vorhaben zu Rebflächen", "soweit durch Rechtsverordnung nach § 33 Weingesetz vorgeschrieben", "", "Meldung an zuständige Behörde", "Task"),
            req("WEING-033-001-002", DC_WEIN, SRC_WEING, "§ 33 Abs. 1 Nr. 2 Weingesetz", "Rebflächen ... Erntemenge ... zu melden sind", "Rebflächen des Betriebes, Ertragsrebflächen, Erntemengen nach Rebsorten und Herkunft sowie die vorgesehene Differenzierung der Weine können meldepflichtig sein, soweit dies durch Rechtsverordnung vorgeschrieben ist.", "Bedingte Meldepflicht", "Betrieb / Bewirtschafter", "melden", "Rebflächen, Ertragsrebflächen, Erntemengen und Weindifferenzierung", "soweit durch Rechtsverordnung nach § 33 Weingesetz vorgeschrieben", "", "Weinbaukartei-/Erntemeldung", "Task"),
            req("WEING-033-001-003", DC_WEIN, SRC_WEING, "§ 33 Abs. 1 Nr. 3 Weingesetz", "Ernte, Erzeugung und Bestand ... zu melden", "Ernte, Erzeugung und Bestand an Weinbauerzeugnissen können meldepflichtig sein, soweit dies durch Rechtsverordnung vorgeschrieben ist.", "Bedingte Meldepflicht", "Betrieb / Lebensmittelunternehmer", "melden", "Ernte, Erzeugung und Bestand", "soweit durch Rechtsverordnung nach § 33 Weingesetz vorgeschrieben", "", "Ernte-/Erzeugungs-/Bestandsmeldung", "Task"),
            req("WEING-033-001-004", DC_WEIN, SRC_WEING, "§ 33 Abs. 1a Nr. 1 Weingesetz", "darüber und über die Maßnahmen zu unterrichten", "Wer Grund zu der Annahme hat, dass ein von ihm hergestelltes, behandeltes, eingeführtes oder in Verkehr gebrachtes Erzeugnis nicht den einschlägigen weinrechtlichen Vorschriften entspricht, kann verpflichtet sein, die Überwachungsbehörde über den Sachverhalt und Maßnahmen zur Abwehr einer Gesundheitsgefahr zu unterrichten, soweit dies durch Rechtsverordnung vorgeschrieben ist.", "Bedingte Unterrichtungspflicht", "Hersteller / Behandler / Einführer / Inverkehrbringer", "unterrichten", "nicht rechtskonformes Erzeugnis und Maßnahmen", "Grund zur Annahme der Nichtkonformität; soweit durch Rechtsverordnung vorgeschrieben", "", "Unterrichtung an Überwachungsbehörde", "Gateway; Task"),
            req("WEING-033-001-005", DC_WEIN, SRC_WEING, "§ 33 Abs. 1a Nr. 2 Weingesetz", "über Maßnahmen ... zurückzurufen", "Wer Grund zu der Annahme hat, dass ein betroffenes Erzeugnis nicht den einschlägigen weinrechtlichen Vorschriften entspricht, kann verpflichtet sein, die Überwachungsbehörde über Rückrufmaßnahmen zu unterrichten, soweit dies durch Rechtsverordnung vorgeschrieben ist.", "Bedingte Unterrichtungspflicht", "Hersteller / Behandler / Einführer / Inverkehrbringer", "unterrichten", "Rückrufmaßnahmen", "Grund zur Annahme der Nichtkonformität; soweit durch Rechtsverordnung vorgeschrieben", "", "Unterrichtung an Überwachungsbehörde", "Gateway; Task"),
        ],
    )

    write_job(
        "JOB_LINK_0058_SEC_0054",
        [
            req("WEING-034-003-001", DC_WEIN, SRC_WEING, "§ 34 Abs. 3 Satz 2 Weingesetz", "auf Antrag Auskunft", "Eine Person, die für gemeinschaftliche Maßnahmen zum Pflanzenschutz oder zur Qualitätssicherung verantwortlich ist, muss für Auskunft aus der Weinbaukartei einen Antrag stellen und ein berechtigtes Interesse glaubhaft machen.", "Antragspflicht / Nachweis", "verantwortliche Person für gemeinschaftliche Maßnahme", "beantragen und glaubhaft machen", "Auskunft aus der Weinbaukartei", "gemeinschaftliche Maßnahme zum Pflanzenschutz oder zur Qualitätssicherung", "", "Antrag / Nachweis berechtigtes Interesse", "Task; Data Object"),
            req("WEING-034-003-002", DC_WEIN, SRC_WEING, "§ 34 Abs. 3 Satz 3 Weingesetz", "verpflichtet sich ... die Daten nur für den Zweck", "Die antragstellende Person muss sich gegenüber der zuständigen Stelle verpflichten, die aus der Weinbaukartei übermittelten Daten nur für den Zweck zu verarbeiten, zu dessen Erfüllung sie übermittelt wurden.", "Zweckbindung / Verpflichtung", "antragstellende Person", "verpflichten", "übermittelte Daten aus der Weinbaukartei", "Auskunft nach § 34 Abs. 3 Satz 2 Weingesetz", "", "Verpflichtungserklärung", "Task; Data Object"),
        ],
    )

    write_job(
        "JOB_LINK_0059_SEC_0029",
        [
            req("WEINUEV-029-001-001", DC_WEIN, SRC_WEINUEV, "§ 29 Abs. 1 WeinÜV", "Erntemeldung, Erzeugungsmeldung und Bestandsmeldung ... zu erstatten", "Die Erntemeldung, Erzeugungsmeldung und Bestandsmeldung sind den zuständigen Stellen auf den von diesen ausgegebenen Vordrucken zu erstatten.", "Meldepflicht", "meldepflichtiger Betrieb", "erstatten", "Erntemeldung, Erzeugungsmeldung und Bestandsmeldung", "nach Verordnung (EG) Nr. 436/2009", "", "amtlicher Vordruck / Meldung", "Task"),
            req("WEINUEV-029-001-002", DC_WEIN, SRC_WEINUEV, "§ 29 Abs. 1 Satz 2 WeinÜV", "Ausdrucke ... sämtliche erforderlichen Angaben", "Wenn Ausdrucke der elektronischen Datenverarbeitung verwendet werden, müssen diese sämtliche erforderlichen Angaben enthalten.", "Datenanforderung", "meldepflichtiger Betrieb", "angeben", "Ausdrucke elektronischer Datenverarbeitung", "Verwendung von EDV-Ausdrucken für Meldungen; Gestattung durch zuständige Stelle", "", "vollständiger EDV-Ausdruck", "Data Object"),
            req("WEINUEV-029-002-001", DC_WEIN, SRC_WEINUEV, "§ 29 Abs. 2 WeinÜV", "Von der Erntemeldung sind Traubenerzeuger befreit", "Traubenerzeuger sind von der Erntemeldung befreit, wenn sie ihre gesamte Ernte selbst verarbeiten oder auf ihre Rechnung verarbeiten lassen.", "Ausnahme", "Traubenerzeuger", "nicht melden", "Erntemeldung", "gesamte Ernte wird selbst verarbeitet oder auf Rechnung verarbeitet", "", "Verarbeitungsnachweis", "Gateway"),
            req("WEINUEV-029-002-002", DC_WEIN, SRC_WEINUEV, "§ 29 Abs. 2 WeinÜV", "Mitglieder einer Genossenschaftskellerei", "Traubenerzeuger sind von der Erntemeldung befreit, wenn sie Mitglied einer Genossenschaftskellerei oder Erzeugergemeinschaft sind und ihre gesamte Ernte als Trauben oder Most abliefern.", "Ausnahme", "Traubenerzeuger", "nicht melden", "Erntemeldung", "Mitgliedschaft in Genossenschaftskellerei oder Erzeugergemeinschaft; gesamte Ernte wird als Trauben oder Most abgeliefert", "", "Ablieferungs-/Mitgliedschaftsnachweis", "Gateway"),
            req("WEINUEV-029-003-001", DC_WEIN, SRC_WEINUEV, "§ 29 Abs. 3 Nr. 1 WeinÜV", "Aufgaben, Rodungen, Wiederbepflanzungen oder Neuanpflanzungen", "Beabsichtigte oder vorgenommene Aufgaben, Rodungen, Wiederbepflanzungen oder Neuanpflanzungen können meldepflichtig sein, soweit eine Landesrechtsverordnung dies vorschreibt.", "Bedingte Meldepflicht", "Betrieb / Bewirtschafter", "melden", "Aufgaben, Rodungen, Wiederbepflanzungen oder Neuanpflanzungen", "soweit durch Landesrechtsverordnung vorgeschrieben", "", "Meldung an zuständige Stelle", "Task"),
            req("WEINUEV-029-003-002", DC_WEIN, SRC_WEINUEV, "§ 29 Abs. 3 Nr. 2 WeinÜV", "Rebflächen ... Erntemenge ... Bestand", "Rebflächen, Ertragsrebflächen, Erntemengen nach Rebsorten und Herkunft, vorgesehene Weindifferenzierung oder Bestände können meldepflichtig sein, soweit eine Landesrechtsverordnung dies vorschreibt.", "Bedingte Meldepflicht", "Betrieb / Bewirtschafter", "melden", "Rebflächen, Erntemenge, Weindifferenzierung und Bestand", "soweit durch Landesrechtsverordnung vorgeschrieben", "", "Weinbaukartei-/Ernte-/Bestandsmeldung", "Task"),
        ],
    )

    write_job(
        "JOB_LINK_0059_SEC_0030",
        [
            req("WEINUEV-030-001-001", DC_WEIN, SRC_WEINUEV, "§ 30 Abs. 1 WeinÜV", "Zuständige Behörde für die Meldung", "Meldungen über Besitz an Saccharose, konzentriertem Traubenmost oder rektifiziertem Traubenmostkonzentrat sind bei der nach Landesrecht zuständigen Stelle zu erstatten.", "Meldepflicht / Zuständigkeit", "meldepflichtiger Betrieb", "melden", "Besitz an Saccharose, konzentriertem Traubenmost oder rektifiziertem Traubenmostkonzentrat", "wenn eine Meldung nach den genannten EU-Vorschriften erforderlich ist", "", "Meldung an zuständige Stelle", "Task"),
            req("WEINUEV-030-001-002", DC_WEIN, SRC_WEINUEV, "§ 30 Abs. 1 WeinÜV", "Erhöhung des Alkoholgehaltes, Entsäuerung oder Säuerung", "Meldungen über Erhöhung des Alkoholgehaltes, Entsäuerung oder Säuerung sind bei der nach Landesrecht zuständigen Stelle zu erstatten.", "Meldepflicht / Zuständigkeit", "meldepflichtiger Betrieb", "melden", "önologische Verfahren", "Erhöhung des Alkoholgehaltes, Entsäuerung oder Säuerung", "", "Meldung an zuständige Stelle", "Task"),
            req("WEINUEV-030-001-003", DC_WEIN, SRC_WEINUEV, "§ 30 Abs. 1 WeinÜV", "die Süßung", "Meldungen über die Süßung sind bei der nach Landesrecht zuständigen Stelle zu erstatten.", "Meldepflicht / Zuständigkeit", "meldepflichtiger Betrieb", "melden", "Süßung", "Süßung nach Verordnung (EG) Nr. 606/2009", "", "Meldung an zuständige Stelle", "Task"),
            req("WEINUEV-030-003-001", DC_WEIN, SRC_WEINUEV, "§ 30 Abs. 3 WeinÜV", "im Voraus erstattet wird", "Eine für mehrere Maßnahmen oder einen Zeitraum geltende Meldung über die Erhöhung des Alkoholgehaltes oder über Süßungsvorgänge kann im Voraus erstattet werden, soweit eine Landesrechtsverordnung dies zulässt.", "Bedingte Meldeoption", "meldepflichtiger Betrieb", "im Voraus melden", "Meldung über Alkoholgehaltserhöhung oder Süßung", "soweit durch Landesrechtsverordnung zugelassen", "im Voraus", "Vorausmeldung", "Gateway; Task"),
        ],
    )

    print("Third batch extraction drafts written.")


if __name__ == "__main__":
    main()
