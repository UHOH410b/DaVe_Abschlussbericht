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

DC_DZ = "DC_002_DIREKTZAHLUNGEN_EINKOMMENSGRUNDSTUTZUNG_EG"
SRC_GAPINVEKOSV = "SRC_GESETZ_ZUR_DURCHFUHRUNG_DER_IM_RAHMEN_DER_"


def req(
    requirement_id: str,
    source_reference: str,
    original_text: str,
    atomic_requirement: str,
    requirement_type: str,
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
        "Requirement_ID": requirement_id,
        "Data_Collection_ID": DC_DZ,
        "Source_Document_ID": SRC_GAPINVEKOSV,
        "Source_Reference": source_reference,
        "Original_Text": original_text,
        "Atomic_Requirement": atomic_requirement,
        "Requirement_Type": requirement_type,
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


def write_job(job_name: str, rows: list[dict]) -> None:
    out = JOBS / job_name / "atomic_requirements_output.csv"
    pd.DataFrame(rows, columns=COLUMNS).to_csv(out, index=False, encoding="utf-8-sig")


def main() -> None:
    write_job(
        "JOB_LINK_0003_SEC_0007",
        [
            req(
                "GAPINVEKOSV-007-001-001",
                "§ 7 Abs. 1 GAPInVeKoSV",
                "Der Betriebsinhaber hat im Sammelantrag anzugeben, welche Direktzahlungen er beantragt.",
                "Der Betriebsinhaber muss im Sammelantrag angeben, welche Direktzahlungen er beantragt.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "beantragte Direktzahlungen",
                "Sammelantrag auf Direktzahlungen",
            ),
            req(
                "GAPINVEKOSV-007-001-002",
                "§ 7 Abs. 1 GAPInVeKoSV",
                "Der Betriebsinhaber hat hierzu die in den nachfolgenden Vorschriften festgelegten Angaben zu machen.",
                "Der Betriebsinhaber muss im Sammelantrag die in den nachfolgenden Vorschriften festgelegten Angaben machen.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "festgelegte Antragsangaben",
                "Sammelantrag auf Direktzahlungen",
            ),
            req(
                "GAPINVEKOSV-007-002-001",
                "§ 7 Abs. 2 GAPInVeKoSV",
                "Der Sammelantrag soll die ... erforderlichen Nachweise oder Belege enthalten.",
                "Der Betriebsinhaber soll die für die Prüfung der Förderfähigkeit oder Konditionalität erforderlichen Nachweise oder Belege mit dem Sammelantrag einreichen.",
                "Nachweispflicht",
                "Betriebsinhaber",
                "einreichen",
                "Nachweise oder Belege",
                "Prüfung der Förderfähigkeit oder Konditionalität",
                "mit dem Sammelantrag; späterer Termin möglich",
                "Nachweise oder Belege",
            ),
            req(
                "GAPINVEKOSV-007-003-001",
                "§ 7 Abs. 3 GAPInVeKoSV",
                "Die zuständige Behörde kann weitere Angaben fordern, soweit dies zur Überprüfung der Antragsangaben erforderlich ist.",
                "Der Betriebsinhaber muss weitere Angaben machen, wenn die zuständige Behörde diese zur Überprüfung der Antragsangaben fordert.",
                "Angabepflicht",
                "Betriebsinhaber",
                "nachreichen",
                "weitere Angaben",
                "Anforderung durch zuständige Behörde zur Überprüfung der Antragsangaben",
                "",
                "behördlich geforderte Angaben",
            ),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0008",
        [
            req(
                "GAPINVEKOSV-008-003-001",
                "§ 8 Abs. 3 Satz 1 Nr. 1 GAPInVeKoSV",
                "alle Flächen, für die der Betriebsinhaber Direktzahlungen beantragt",
                "Der Betriebsinhaber muss im Sammelantrag alle Flächen angeben, für die er Direktzahlungen beantragt.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "angemeldete Flächen",
                "Beantragung von Direktzahlungen für Flächen",
            ),
            req(
                "GAPINVEKOSV-008-003-002",
                "§ 8 Abs. 3 Satz 1 Nr. 2 GAPInVeKoSV",
                "alle Tiere, für die der Betriebsinhaber Direktzahlungen beantragt",
                "Der Betriebsinhaber muss im Sammelantrag alle Tiere angeben, für die er Direktzahlungen beantragt.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "angemeldete Tiere",
                "Beantragung von Direktzahlungen für Tiere",
            ),
            req(
                "GAPINVEKOSV-008-003-003",
                "§ 8 Abs. 3 Satz 2 GAPInVeKoSV",
                "unzutreffende oder nicht mehr zutreffende Angaben zu berichtigen",
                "Der Betriebsinhaber muss im geodatenbasierten und tierbezogenen Antragssystem unzutreffende oder nicht mehr zutreffende Angaben berichtigen.",
                "Korrekturpflicht",
                "Betriebsinhaber",
                "berichtigen",
                "unzutreffende oder nicht mehr zutreffende Angaben",
                "Sammelantrag über geodatenbasiertes oder tierbezogenes Antragssystem",
                "",
                "korrigierte Antragsdaten",
            ),
            req(
                "GAPINVEKOSV-008-003-004",
                "§ 8 Abs. 3 Satz 2 GAPInVeKoSV",
                "unvollständige Angaben zu vervollständigen und die übrigen Angaben zu bestätigen",
                "Der Betriebsinhaber muss im geodatenbasierten und tierbezogenen Antragssystem unvollständige Angaben vervollständigen und die übrigen Angaben bestätigen.",
                "Angabepflicht",
                "Betriebsinhaber",
                "vervollständigen und bestätigen",
                "Antragsangaben",
                "Sammelantrag über geodatenbasiertes oder tierbezogenes Antragssystem",
                "",
                "bestätigte Antragsdaten",
            ),
            req(
                "GAPINVEKOSV-008-004-001",
                "§ 8 Abs. 4 GAPInVeKoSV",
                "Eine unbillige Härte liegt insbesondere vor, wenn der Antragssteller glaubhaft darlegt ...",
                "Der Antragsteller muss die Gründe für eine unbillige Härte glaubhaft und abschließend darlegen, wenn er die Antragssysteme nicht verwenden kann.",
                "Nachweispflicht",
                "Antragsteller",
                "darlegen",
                "Gründe für unbillige Härte",
                "Sammelantrag kann nicht über die vorgesehenen Antragssysteme eingereicht werden",
                "",
                "Darlegung / Glaubhaftmachung",
                "Gateway; Task",
            ),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0009",
        [
            req(
                "GAPINVEKOSV-009-001-001",
                "§ 9 Nr. 1 bis 7 GAPInVeKoSV",
                "Der Betriebsinhaber hat im Sammelantrag anzugeben: den Vor- und Nachnamen oder die Firma ...",
                "Der Betriebsinhaber muss im Sammelantrag seine Identitäts- und Kontaktdaten angeben.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "Identitäts- und Kontaktdaten",
                "Sammelantrag",
            ),
            req(
                "GAPINVEKOSV-009-001-002",
                "§ 9 Nr. 8 bis 10 GAPInVeKoSV",
                "die Betriebsnummer ... die Bankverbindung ... das zuständige Finanzamt",
                "Der Betriebsinhaber muss im Sammelantrag Betriebsnummer, Bankverbindung und zuständiges Finanzamt angeben.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "Betriebsnummer, Bankverbindung und Finanzamt",
                "Sammelantrag",
            ),
            req(
                "GAPINVEKOSV-009-001-003",
                "§ 9 Nr. 11 GAPInVeKoSV",
                "im Falle mehrerer Betriebsstätten den Namen, die Anschrift und die ... Registriernummern dieser Betriebsstätten",
                "Der Betriebsinhaber muss bei mehreren Betriebsstätten deren Namen, Anschriften und Registriernummern im Sammelantrag angeben.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "Betriebsstättendaten",
                "mehrere Betriebsstätten",
            ),
            req(
                "GAPINVEKOSV-009-001-004",
                "§ 9 Nr. 12 GAPInVeKoSV",
                "im Falle einer Bevollmächtigung den Namen und die Anschrift ... des Bevollmächtigten",
                "Der Betriebsinhaber muss bei einer Bevollmächtigung die Daten des Bevollmächtigten im Sammelantrag angeben.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "Daten des Bevollmächtigten",
                "Bevollmächtigung",
            ),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0010",
        [
            req(
                "GAPINVEKOSV-010-001-001",
                "§ 10 Abs. 1 GAPInVeKoSV",
                "Der Betriebsinhaber hat im Sammelantrag mindestens einen ... Fällen anzugeben",
                "Der Betriebsinhaber muss im Sammelantrag angeben, nach welchem Fall er zum Zeitpunkt der Antragstellung aktiver Betriebsinhaber ist.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "Fall des aktiven Betriebsinhabers",
                "Sammelantrag",
            ),
            req(
                "GAPINVEKOSV-010-001-002",
                "§ 10 Abs. 1 GAPInVeKoSV",
                "Bei dem erstmaligen Antrag auf Direktzahlungen ist zusätzlich das Datum anzugeben ...",
                "Der Betriebsinhaber muss beim erstmaligen Antrag auf Direktzahlungen das Datum der Gründung oder Übernahme des Betriebs angeben.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "Datum der Gründung oder Übernahme",
                "erstmaliger Antrag auf Direktzahlungen",
            ),
            req(
                "GAPINVEKOSV-010-002-001",
                "§ 10 Abs. 2 Satz 1 Nr. 1 bis 3 GAPInVeKoSV",
                "Der Betriebsinhaber hat im Antrag des Weiteren anzugeben ...",
                "Der Betriebsinhaber muss je nach Fall des aktiven Betriebsinhabers die zusätzlich vorgeschriebenen Angaben zur Unfallversicherung, zum zuständigen Staat oder zur Direktzahlungsgrenze machen.",
                "Angabepflicht",
                "Betriebsinhaber",
                "angeben",
                "Zusatzangaben zum aktiven Betriebsinhaber",
                "Angabe eines Falls nach § 8 GAP-Direktzahlungen-Verordnung",
            ),
            req(
                "GAPINVEKOSV-010-002-002",
                "§ 10 Abs. 2 Satz 2 GAPInVeKoSV",
                "ist ein geeigneter Nachweis ... vorzulegen",
                "Der Betriebsinhaber muss einen geeigneten Nachweis über das Vorliegen des angegebenen Falls als aktiver Betriebsinhaber vorlegen, sofern dieser Nachweis der zuständigen Behörde nicht bereits vorliegt.",
                "Nachweispflicht",
                "Betriebsinhaber",
                "vorlegen",
                "Nachweis aktiver Betriebsinhaber",
                "Nachweis liegt der zuständigen Behörde noch nicht vor",
                "zum Zeitpunkt der Antragstellung",
                "geeigneter Nachweis; z. B. Beitragszahlungsbeleg oder Beleg über Beginn der Unfallversicherungszuständigkeit",
            ),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0011",
        [
            req("GAPINVEKOSV-011-001-001", "§ 11 Abs. 1 Satz 1 GAPInVeKoSV", "alle landwirtschaftlichen Parzellen des Betriebes", "Der Betriebsinhaber muss im Sammelantrag alle landwirtschaftlichen Parzellen des Betriebs mit den vorgesehenen Nutzungscodes angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "landwirtschaftliche Parzellen", "Sammelantrag", "", "geodatenbasierte Flächenangaben"),
            req("GAPINVEKOSV-011-001-002", "§ 11 Abs. 1 Satz 2 Nr. 1 GAPInVeKoSV", "Flächen, die für den Anbau von Hanf genutzt werden, unter Angabe der Saatgutsorte und der verwendeten Saatgutmengen", "Der Betriebsinhaber muss Hanfflächen im Sammelantrag besonders bezeichnen und Saatgutsorte sowie Saatgutmenge je Hektar angeben.", "Angabepflicht", "Betriebsinhaber", "besonders bezeichnen und angeben", "Hanfflächen, Saatgutsorte und Saatgutmenge", "Hanfanbau", "", "Saatgutangaben"),
            req("GAPINVEKOSV-011-001-003", "§ 11 Abs. 1 Satz 2 Nr. 2 bis 8 GAPInVeKoSV", "Dauergrünlandflächen ... Flächen mit ökologischem Landbau ... Agri-Photovoltaik-Anlagen", "Der Betriebsinhaber muss die in § 11 Abs. 1 Satz 2 Nr. 2 bis 8 genannten besonderen Flächenarten im Sammelantrag besonders bezeichnen.", "Angabepflicht", "Betriebsinhaber", "besonders bezeichnen", "besondere Flächenarten", "Sammelantrag", "", "Flächenangaben"),
            req("GAPINVEKOSV-011-001-004", "§ 11 Abs. 1 Satz 2 Nr. 9 GAPInVeKoSV", "mit anderen Betriebsinhabern gemeinsam genutzte Flächen unter Angabe seines Anteils an der Nutzung", "Der Betriebsinhaber muss gemeinsam genutzte Flächen im Sammelantrag besonders bezeichnen und seinen Nutzungsanteil angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "gemeinsam genutzte Flächen und Nutzungsanteil", "gemeinsame Flächennutzung"),
            req("GAPINVEKOSV-011-002-001", "§ 11 Abs. 2 GAPInVeKoSV", "auch für eine nichtlandwirtschaftliche Tätigkeit ... Art ... Beginn und Ende", "Der Betriebsinhaber muss bei nichtlandwirtschaftlicher Nutzung einer beantragten Fläche Art, Beginn und Ende der nichtlandwirtschaftlichen Tätigkeit im Sammelantrag angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "nichtlandwirtschaftliche Tätigkeit auf beantragter Fläche", "nichtlandwirtschaftliche Tätigkeit vor Antragstellung begonnen oder stattgefunden"),
            req("GAPINVEKOSV-011-004-001", "§ 11 Abs. 4 GAPInVeKoSV", "ist ein geeigneter Nachweis vorzulegen ... Agri-Photovoltaik-Anlage", "Der Betriebsinhaber muss einen geeigneten Nachweis vorlegen, wenn er geltend macht, dass eine Anlage zur Nutzung solarer Strahlungsenergie eine Agri-Photovoltaik-Anlage ist.", "Nachweispflicht", "Betriebsinhaber", "vorlegen", "Nachweis Agri-Photovoltaik-Anlage", "beantragte Fläche wird mit Anlage zur Nutzung solarer Strahlungsenergie genutzt", "", "geeigneter Nachweis"),
            req("GAPINVEKOSV-011-005-001", "§ 11 Abs. 5 GAPInVeKoSV", "hat der Betriebsinhaber ... Landschaftselemente ... zuzuordnen", "Der Betriebsinhaber muss Landschaftselemente oder Teile von Landschaftselementen der jeweils angrenzenden Dauergrünlandfläche, Dauerkulturfläche oder Ackerfläche im Sammelantrag zuordnen.", "Angabepflicht", "Betriebsinhaber", "zuordnen", "Landschaftselemente", "Landschaftselement grenzt an mehrere Flächenarten desselben Betriebsinhabers"),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0013",
        [
            req("GAPINVEKOSV-013-001-001", "§ 13 Satz 1 Nr. 1 GAPInVeKoSV", "eine Erklärung, zur Einhaltung welcher Öko-Regelung ...", "Der Betriebsinhaber muss bei Beantragung von Öko-Regelungen erklären, zur Einhaltung welcher Öko-Regelung oder Öko-Regelungen er sich verpflichtet.", "Erklärungspflicht", "Betriebsinhaber", "erklären", "Verpflichtung zur Einhaltung von Öko-Regelungen", "Antrag auf Zahlungen für Öko-Regelungen", "", "Erklärung im Sammelantrag"),
            req("GAPINVEKOSV-013-001-002", "§ 13 Satz 1 Nr. 2 Buchst. a bis d GAPInVeKoSV", "Flächen nach Lage und Größe ... Blühflächen ... Altgrasstreifen", "Der Betriebsinhaber muss für die genannten Öko-Regelungen die betreffenden Flächen nach Lage und Größe im Sammelantrag angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "Flächen nach Lage und Größe", "Antrag auf flächenbezogene Öko-Regelungen"),
            req("GAPINVEKOSV-013-001-003", "§ 13 Satz 1 Nr. 2 Buchst. b und c GAPInVeKoSV", "Angabe des Jahres der Aussaat sowie der Kategorie der Saatgutmischung", "Der Betriebsinhaber muss bei Blühflächen und Blühstreifen das Jahr der Aussaat und die Kategorie der Saatgutmischung angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "Aussaatjahr und Saatgutmischungskategorie", "Antrag auf entsprechende Öko-Regelung"),
            req("GAPINVEKOSV-013-001-004", "§ 13 Satz 1 Nr. 2 Buchst. e GAPInVeKoSV", "für das gesamte Ackerland ... die Kulturarten nach Nutzungscode ... Hauptfruchtart", "Der Betriebsinhaber muss für das gesamte relevante Ackerland Kulturarten nach Nutzungscode, Hauptfruchtart im Zeitraum 1. Juni bis 15. Juli sowie Lage und Größe der Flächen angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "Kulturarten, Hauptfruchtart, Lage und Größe", "Antrag auf Öko-Regelung nach § 20 Abs. 1 Nr. 2 GAP-Direktzahlungen-Gesetz", "Zeitraum 1. Juni bis 15. Juli des Antragsjahres"),
            req("GAPINVEKOSV-013-001-005", "§ 13 Satz 1 Nr. 2 Buchst. g GAPInVeKoSV", "voraussichtliche durchschnittliche Tierzahl je raufutterfressender Tierart ...", "Der Betriebsinhaber muss die voraussichtliche durchschnittliche Tierzahl je raufutterfressender Tierart im Gesamtbetrieb sowie die Dauergrünlandflächen nach Lage und Größe angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "Tierzahl und Dauergrünlandflächen", "Antrag auf Öko-Regelung nach § 20 Abs. 1 Nr. 4 GAP-Direktzahlungen-Gesetz"),
            req("GAPINVEKOSV-013-001-006", "§ 13 Satz 1 Nr. 2 Buchst. h GAPInVeKoSV", "Erklärung, dass mindestens vier der zulässigen Pflanzenarten oder Artengruppen ... vorkommen", "Der Betriebsinhaber muss bei der entsprechenden Öko-Regelung erklären, dass mindestens vier zulässige Pflanzenarten oder Artengruppen des artenreichen Grünlands auf den Flächen vorkommen.", "Erklärungspflicht", "Betriebsinhaber", "erklären", "Vorkommen von mindestens vier Kennarten oder Kennartengruppen", "Antrag auf Öko-Regelung nach § 20 Abs. 1 Nr. 5 GAP-Direktzahlungen-Gesetz", "", "Erklärung im Sammelantrag"),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0014",
        [
            req("GAPINVEKOSV-014-001-001", "§ 14 Abs. 1 GAPInVeKoSV", "Anzahl ... Identifikation ... Aufenthaltsort ... Erklärung", "Der Betriebsinhaber muss bei Beantragung der Zahlung für Mutterschafe und -ziegen Anzahl, Identifikation und Aufenthaltsort der beantragten Tiere angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "Anzahl, Identifikation und Aufenthaltsort von Mutterschafen und -ziegen", "Antrag auf gekoppelte Einkommensstützung für Mutterschafe und -ziegen"),
            req("GAPINVEKOSV-014-001-002", "§ 14 Abs. 1 Nr. 4 GAPInVeKoSV", "die Erklärung, dass die Tiere ... im Betrieb gehalten ... Kennzeichnung und Registrierung eingehalten werden", "Der Betriebsinhaber muss erklären, dass die beantragten Mutterschafe und -ziegen im Haltungszeitraum im Betrieb gehalten werden und die Kennzeichnungs- und Registrierungspflichten eingehalten werden.", "Erklärungspflicht", "Betriebsinhaber", "erklären", "Haltung sowie Kennzeichnung und Registrierung", "Antrag auf gekoppelte Einkommensstützung für Mutterschafe und -ziegen", "Haltungszeitraum", "Erklärung im Sammelantrag"),
            req("GAPINVEKOSV-014-002-001", "§ 14 Abs. 2 Nr. 1 GAPInVeKoSV", "Angabe der Ohrmarkennummern der Mutterkühe", "Der Betriebsinhaber muss bei Beantragung der Zahlung für Mutterkühe die Ohrmarkennummern der beantragten Mutterkühe angeben.", "Angabepflicht", "Betriebsinhaber", "angeben", "Ohrmarkennummern der Mutterkühe", "Antrag auf gekoppelte Einkommensstützung für Mutterkühe"),
            req("GAPINVEKOSV-014-002-002", "§ 14 Abs. 2 Nr. 2 GAPInVeKoSV", "die Erklärung, dass im Antragsjahr keine Kuhmilch oder Kuhmilcherzeugnisse aus Selbsterzeugung abgegeben werden", "Der Betriebsinhaber muss erklären, dass im Antragsjahr keine Kuhmilch oder Kuhmilcherzeugnisse aus Selbsterzeugung abgegeben werden.", "Erklärungspflicht", "Betriebsinhaber", "erklären", "keine Abgabe von Kuhmilch oder Kuhmilcherzeugnissen aus Selbsterzeugung", "Antrag auf gekoppelte Einkommensstützung für Mutterkühe", "Antragsjahr", "Erklärung im Sammelantrag"),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0015",
        [
            req("GAPINVEKOSV-015-001-001", "§ 15 Abs. 1 GAPInVeKoSV", "hat er einzureichen: das amtliche Etikett ...", "Der Betriebsinhaber muss bei Beantragung von Direktzahlungen für Hanfflächen das amtliche Saatgutetikett oder bei Erhaltungssorten das entsprechende Etikett einreichen.", "Nachweispflicht", "Betriebsinhaber", "einreichen", "Saatgutetikett", "Direktzahlungen für Hanfflächen", "", "amtliches Saatgutetikett oder Etikett nach Erhaltungssortenverordnung"),
            req("GAPINVEKOSV-015-002-001", "§ 15 Abs. 2 GAPInVeKoSV", "Bei einer Aussaat des Hanfs nach dem 30. Juni ... bis spätestens zum 1. September", "Der Betriebsinhaber muss bei Hanfaussaat nach dem 30. Juni das Saatgutetikett spätestens bis zum 1. September des Antragsjahres einreichen.", "Nachweispflicht", "Betriebsinhaber", "einreichen", "Saatgutetikett", "Hanfaussaat nach dem 30. Juni des Antragsjahres", "spätestens 1. September des Antragsjahres", "Saatgutetikett"),
            req("GAPINVEKOSV-015-003-001", "§ 15 Abs. 3 GAPInVeKoSV", "ist von jedem der Betriebsinhaber zugleich eine Erklärung über die Aufteilung des Saatguts vorzulegen", "Jeder betroffene Betriebsinhaber muss eine Erklärung über die Aufteilung des Saatguts vorlegen, wenn dasselbe Saatgutetikett für Saatgut mehrerer Betriebsinhaber gilt.", "Erklärungspflicht", "Betriebsinhaber", "vorlegen", "Erklärung über Saatgutaufteilung", "Saatgut wurde von mehreren Betriebsinhabern verwendet", "", "Erklärung über die Aufteilung des Saatguts"),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0016",
        [
            req("GAPINVEKOSV-016-001-001", "§ 16 Nr. 1 GAPInVeKoSV", "ob und welcher anerkannten Hopfenerzeugerorganisation er angehört", "Der Hopfenerzeuger muss im Sammelantrag angeben, ob und welcher anerkannten Hopfenerzeugerorganisation er angehört.", "Angabepflicht", "Hopfenerzeuger", "angeben", "Mitgliedschaft in Hopfenerzeugerorganisation", "Hopfenerzeuger"),
            req("GAPINVEKOSV-016-001-002", "§ 16 Nr. 2 GAPInVeKoSV", "für jede Fläche, auf der Hopfen angebaut wird, welche Hopfensorten er anbaut", "Der Hopfenerzeuger muss im Sammelantrag für jede Hopfenfläche die angebauten Hopfensorten angeben.", "Angabepflicht", "Hopfenerzeuger", "angeben", "Hopfensorten je Hopfenfläche", "Hopfenanbau"),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0019",
        [
            req("GAPINVEKOSV-019-001-001", "§ 19 Abs. 1 Nr. 1 GAPInVeKoSV", "im Sammelantrag zu erklären, dass er ...", "Der natürliche Betriebsinhaber muss bei erstmaliger Beantragung der Junglandwirte-Einkommensstützung die in § 19 Abs. 1 Nr. 1 genannten Erklärungen abgeben.", "Erklärungspflicht", "natürlicher Betriebsinhaber", "erklären", "Nichtbezug früherer Junglandwirte-Unterstützung und Nichtberücksichtigung für andere Betriebsinhaber", "erstmalige Beantragung der Junglandwirte-Einkommensstützung"),
            req("GAPINVEKOSV-019-001-002", "§ 19 Abs. 1 Nr. 2 GAPInVeKoSV", "den Zeitpunkt anzugeben, zu dem er sich erstmals ... als Betriebsleiter niedergelassen hat", "Der natürliche Betriebsinhaber muss den Zeitpunkt angeben, zu dem er sich erstmals in einem landwirtschaftlichen Betrieb als Betriebsleiter niedergelassen hat.", "Angabepflicht", "natürlicher Betriebsinhaber", "angeben", "Zeitpunkt der erstmaligen Niederlassung als Betriebsleiter", "erstmalige Beantragung der Junglandwirte-Einkommensstützung"),
            req("GAPINVEKOSV-019-001-003", "§ 19 Abs. 1 Nr. 3 und 4 GAPInVeKoSV", "anzugeben, welche ... Ausbildung oder Qualifikation vorliegt ... nachzuweisen", "Der natürliche Betriebsinhaber muss die erforderliche Ausbildung oder Qualifikation angeben und zum Zeitpunkt der Antragstellung nachweisen.", "Angabe- und Nachweispflicht", "natürlicher Betriebsinhaber", "angeben und nachweisen", "Ausbildung oder Qualifikation", "erstmalige Beantragung der Junglandwirte-Einkommensstützung", "zum Zeitpunkt der Antragstellung", "Abschlusszeugnisse, Teilnahmebescheinigungen, Arbeitsverträge, Gesellschaftsverträge oder Belege"),
            req("GAPINVEKOSV-019-002-001", "§ 19 Abs. 2 Nr. 1 bis 4 GAPInVeKoSV", "Sofern der Betriebsinhaber keine natürliche Person ist ...", "Ein nicht natürlicher Betriebsinhaber muss bei Beantragung der Junglandwirte-Einkommensstützung die in § 19 Abs. 2 Nr. 1 bis 4 genannten Erklärungen, Angaben und Darlegungen im Sammelantrag machen.", "Angabe- und Erklärungspflicht", "nicht natürlicher Betriebsinhaber", "angeben, erklären und darlegen", "Voraussetzungen der Junglandwirte-Einkommensstützung", "Beantragung der Junglandwirte-Einkommensstützung durch nicht natürliche Person"),
            req("GAPINVEKOSV-019-002-002", "§ 19 Abs. 2 Nr. 5 und 6 GAPInVeKoSV", "nachzuweisen ... durch geeignete Nachweise zu belegen", "Ein nicht natürlicher Betriebsinhaber muss Ausbildung oder Qualifikation sowie die rechtlichen und tatsächlichen Voraussetzungen der Junglandwirte-Einkommensstützung durch geeignete Nachweise belegen.", "Nachweispflicht", "nicht natürlicher Betriebsinhaber", "belegen", "Voraussetzungen und Qualifikation", "Beantragung der Junglandwirte-Einkommensstützung durch nicht natürliche Person", "zum Zeitpunkt der Antragstellung", "Abschlusszeugnisse, Teilnahmebescheinigungen, Arbeitsverträge, Gesellschaftsverträge, Registerauszüge oder vergleichbare Nachweise"),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0020",
        [
            req("GAPINVEKOSV-020-001-001", "§ 20 Abs. 1 GAPInVeKoSV", "hat er dies ... anzugeben", "Der Betriebsinhaber muss bei Beantragung der Junglandwirte-Einkommensstützung für den verbleibenden Zeitraum angeben, dass er zuvor Junglandwirte-Unterstützung nach der früheren EU-Regelung erhalten hat.", "Angabepflicht", "Betriebsinhaber", "angeben", "früherer Bezug von Junglandwirte-Unterstützung", "Beantragung für verbleibenden Zeitraum"),
            req("GAPINVEKOSV-020-001-002", "§ 20 Abs. 1 GAPInVeKoSV", "zusätzlich zu bestätigen, dass er nicht ... für einen anderen Betriebsinhaber ... berücksichtigt wird", "Der Betriebsinhaber muss bestätigen, dass er nicht als natürliche Person für einen anderen Betriebsinhaber bei der Junglandwirte-Einkommensstützung berücksichtigt wird oder früher berücksichtigt wurde.", "Erklärungspflicht", "Betriebsinhaber", "bestätigen", "Nichtberücksichtigung für andere Betriebsinhaber", "Beantragung für verbleibenden Zeitraum"),
            req("GAPINVEKOSV-020-002-001", "§ 20 Abs. 2 GAPInVeKoSV", "anzugeben, welche natürliche Person ... weiterhin den Betriebsinhaber kontrolliert", "Ein nicht natürlicher Betriebsinhaber muss angeben, welche natürliche Person oder Personen ihn weiterhin kontrollieren.", "Angabepflicht", "nicht natürlicher Betriebsinhaber", "angeben", "kontrollierende natürliche Personen", "Beantragung der Junglandwirte-Einkommensstützung für verbleibenden Zeitraum"),
            req("GAPINVEKOSV-020-002-002", "§ 20 Abs. 2 Nr. 2 GAPInVeKoSV", "geeignete Nachweise vorzulegen", "Ein nicht natürlicher Betriebsinhaber muss für die Angaben zu den kontrollierenden natürlichen Personen geeignete Nachweise vorlegen.", "Nachweispflicht", "nicht natürlicher Betriebsinhaber", "vorlegen", "Nachweise zu kontrollierenden Personen", "Beantragung der Junglandwirte-Einkommensstützung für verbleibenden Zeitraum", "", "geeignete Nachweise"),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0024",
        [
            req("GAPINVEKOSV-024-001-001", "§ 24 GAPInVeKoSV", "Die anerkannten Erzeugerorganisationen ... dürfen diese Daten ausschließlich ... verwenden.", "Anerkannte Erzeugerorganisationen im Hopfensektor dürfen die übermittelten Hopfenflächendaten ausschließlich zur Identifizierung landwirtschaftlicher Parzellen im Rahmen der Antragstellung verwenden.", "Zweckbindung",
                "anerkannte Erzeugerorganisation im Hopfensektor", "verwenden", "Hopfenflächendaten", "übermittelte Angaben nach § 16 GAPInVeKoSV", "", "Datenverwendungsnachweis", "Gateway; Task"),
        ],
    )

    write_job(
        "JOB_LINK_0003_SEC_0040",
        [
            req("GAPINVEKOSV-040-001-001", "§ 40 Abs. 1 Nr. 1 GAPInVeKoSV", "amtlichen Saatgutetiketten ... oder ... geeignete Nachweise", "Der Betriebsinhaber muss für bestimmte Öko-Regelungen Saatgutetiketten der ausgesäten Saatgutmischungen oder geeignete Ersatznachweise vorhalten.", "Aufbewahrungs-/Vorhaltepflicht", "Betriebsinhaber", "vorhalten", "Saatgutetiketten oder Ersatznachweise", "Kontrolle bestimmter Öko-Regelungen", "", "amtliche Saatgutetiketten oder geeignete Nachweise, insbesondere Rückstellproben"),
            req("GAPINVEKOSV-040-001-002", "§ 40 Abs. 1 Nr. 2 GAPInVeKoSV", "geeignete Aufzeichnungen zum Nachweis des Viehbesatzes ...", "Der Betriebsinhaber muss für die Öko-Regelung zum Dauergrünland geeignete Aufzeichnungen zum Viehbesatz je Hektar förderfähigem Dauergrünland vorhalten.", "Aufbewahrungs-/Vorhaltepflicht", "Betriebsinhaber", "vorhalten", "Aufzeichnungen zum Viehbesatz", "Kontrolle der Öko-Regelung nach § 20 Abs. 1 Nr. 4 GAP-Direktzahlungen-Gesetz", "Antragsjahr", "Aufzeichnungen zum Viehbesatz"),
            req("GAPINVEKOSV-040-001-003", "§ 40 Abs. 1 Nr. 2 GAPInVeKoSV", "schlagbezogene Aufzeichnungen und Nachweise über die Verwendung von Düngemitteln ...", "Der Betriebsinhaber muss für das Dauergrünland schlagbezogene Aufzeichnungen und Nachweise über die Verwendung von Düngemitteln einschließlich Wirtschaftsdüngern vorhalten.", "Aufbewahrungs-/Vorhaltepflicht", "Betriebsinhaber", "vorhalten", "schlagbezogene Düngemittelaufzeichnungen und Nachweise", "Kontrolle der Öko-Regelung nach § 20 Abs. 1 Nr. 4 GAP-Direktzahlungen-Gesetz", "", "schlagbezogene Aufzeichnungen und Düngemittelnachweise"),
            req("GAPINVEKOSV-040-001-004", "§ 40 Abs. 1 Nr. 2 GAPInVeKoSV", "gegebenenfalls Ausnahmegenehmigungen zum Einsatz von Pflanzenschutzmitteln", "Der Betriebsinhaber muss gegebenenfalls Ausnahmegenehmigungen zum Einsatz von Pflanzenschutzmitteln vorhalten.", "Aufbewahrungs-/Vorhaltepflicht", "Betriebsinhaber", "vorhalten", "Ausnahmegenehmigungen zum Pflanzenschutzmitteleinsatz", "Kontrolle der Öko-Regelung nach § 20 Abs. 1 Nr. 4 GAP-Direktzahlungen-Gesetz", "", "Ausnahmegenehmigungen"),
            req("GAPINVEKOSV-040-001-005", "§ 40 Abs. 1 Nr. 3 GAPInVeKoSV", "Nachweise über das Vorkommen von mindestens vier Pflanzenarten oder Artengruppen ...", "Der Betriebsinhaber muss für die Öko-Regelung zum artenreichen Grünland Nachweise über das Vorkommen von mindestens vier Kennarten oder Kennartengruppen vorhalten, soweit keine entsprechende Mitteilung an die zuständige Behörde erfolgt ist.", "Aufbewahrungs-/Vorhaltepflicht", "Betriebsinhaber", "vorhalten", "Kennarten-Nachweise", "Kontrolle der Öko-Regelung nach § 20 Abs. 1 Nr. 5 GAP-Direktzahlungen-Gesetz", "", "Nachweise nach der landesrechtlich festgelegten Methode"),
            req("GAPINVEKOSV-040-001-006", "§ 40 Abs. 1 Nr. 4 GAPInVeKoSV", "geeignete Nachweise bei Anwendung von Pflanzenschutzmitteln", "Der Betriebsinhaber muss für die Öko-Regelung nach § 20 Abs. 1 Nr. 6 GAP-Direktzahlungen-Gesetz geeignete Nachweise bei Anwendung von Pflanzenschutzmitteln vorhalten.", "Aufbewahrungs-/Vorhaltepflicht", "Betriebsinhaber", "vorhalten", "Nachweise zur Pflanzenschutzmittelanwendung", "Kontrolle der Öko-Regelung nach § 20 Abs. 1 Nr. 6 GAP-Direktzahlungen-Gesetz", "", "geeignete Nachweise"),
            req("GAPINVEKOSV-040-002-001", "§ 40 Abs. 2 GAPInVeKoSV", "Nachweise vorzuhalten für: die Förderfähigkeit von Ersatztieren ...", "Der Betriebsinhaber muss zur Kontrolle der gekoppelten Einkommensstützung Nachweise zur Förderfähigkeit von Ersatztieren vorhalten.", "Aufbewahrungs-/Vorhaltepflicht", "Betriebsinhaber", "vorhalten", "Nachweise zur Förderfähigkeit von Ersatztieren", "Kontrolle der gekoppelten Einkommensstützung", "", "Nachweise zu Ersatztieren"),
            req("GAPINVEKOSV-040-002-002", "§ 40 Abs. 2 GAPInVeKoSV", "den Zeitpunkt des Ausscheidens und des Ersatzes von Tieren ...", "Der Betriebsinhaber muss zur Kontrolle der gekoppelten Einkommensstützung Nachweise zum Zeitpunkt des Ausscheidens und des Ersatzes beantragter Tiere vorhalten.", "Aufbewahrungs-/Vorhaltepflicht", "Betriebsinhaber", "vorhalten", "Nachweise zum Ausscheiden und Ersatz von Tieren", "Kontrolle der gekoppelten Einkommensstützung", "", "Nachweise zum Zeitpunkt des Ausscheidens und Ersatzes"),
        ],
    )

    print("Fifth batch extraction drafts written.")


if __name__ == "__main__":
    main()
