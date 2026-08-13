# Flow-Spezifikation v0.1

## Ziel

Der KI-Flow konvertiert Fliesstext aus Standards, Fachrecht, Foerderrichtlinien und weiteren Grundlagendokumenten in einen mehrquellenfaehigen Katalog atomarer Anforderungen. Jede Anforderung bleibt quellengebunden, rueckverfolgbar und fuer BPMN-Level-2-Prozessmodellierung nutzbar.

## Input

Primaerer Einstiegspunkt ist der Metadatenkatalog:

- `Source_Document_ID` oder ersatzweise stabile Zeilen-ID
- Kurztitel
- Langtitel / Grundlagendokument Titel
- URL Grundlagendokument
- Datengebende Stelle
- Datenempfangende Stelle
- Zugehoeriger Prozess
- Beschreibung
- Datenquelle
- Format
- Datenstruktur
- Uebermittlungsart
- URL Uebermittlung / Vorlagen / Online-Programm
- Frequenz

## Kern-Workflow

1. Metadatenkatalog lesen und jede Datenerhebung als potenzielle Quelle behandeln.
2. Grundlagendokument oder lokale Datei oeffnen.
3. Dokument in stabile Abschnitte segmentieren.
4. Pro Abschnitt normative Aussagen erkennen.
5. Normative Aussagen in atomare Anforderungen zerlegen.
6. Kontextvererbung anwenden, damit ausloesende Bedingungen nicht verloren gehen.
7. Anforderungen mit Source-Dokument, Prozess, Datengeber, Datenempfaenger und Frequenz verknuepfen.
8. Begriffe, Parameter und Datenobjekte in eigene Kataloge auslagern.
9. Aehnlichkeiten, Redundanzen und potenzielle Konflikte mit bestehenden Anforderungen markieren.
10. Ergebnisse als Review-Vorschlaege ausgeben, nicht blind finalisieren.

## Agentenrollen

- `Metadata Agent`: liest und validiert den Metadatenkatalog.
- `Document Access Agent`: oeffnet URLs oder lokale Dateien und extrahiert Text.
- `Segmentation Agent`: zerlegt Dokumente in Kapitel, Abschnitte, Tabellen und Saetze mit Quellenreferenz.
- `Requirement Extraction Agent`: erkennt Pflichten, Verbote, Bedingungen, Ausnahmen, Fristen und Dokumentationspflichten.
- `Atomization Agent`: zerlegt zusammengesetzte Aussagen in einzelne pruefbare Anforderungen.
- `Context Preservation Agent`: ergaenzt vererbten Kontext aus vorherigen Saetzen oder Absaetzen.
- `Semantic Catalog Agent`: sammelt interne Begriffe, Parameter, Datenobjekte und spaetere AGROVOC-Kandidaten.
- `BPMN Mapping Agent`: ordnet Tasks, Gateways, Events, Data Objects, Message Flows und Control Points vor.
- `Relation Agent`: markiert identische, aehnliche, ueberlappende oder widerspruechliche Anforderungen.
- `QA Agent`: prueft Vollstaendigkeit gegen den Originaltext und markiert Unsicherheiten.

## Zentrale Extraktionsregeln

Eine atomare Anforderung enthaelt genau eine pruefbare Pflicht, ein Verbot, eine Bedingung, eine Ausnahme, eine Frist, einen Grenzwert oder eine Dokumentationspflicht.

Zusammengesetzte Listen muessen aufgespalten werden. Beispiel: "Art und Menge" wird zu einer Anforderung fuer die Art und einer Anforderung fuer die Menge.

Grenzwerte, Fristen und Einheiten werden nicht nur im Fliesstext belassen, sondern zusaetzlich im Parameterkatalog erfasst.

Dokumentationspflichten erzeugen immer ein Datenobjekt oder einen Nachweis im Datenobjektkatalog.

## Kontextvererbungsregel

Wenn eine Anforderung auf einen zuvor beschriebenen Zustand verweist, muss der fachlich relevante Kontext in der atomaren Anforderung erhalten bleiben.

Signalwoerter sind unter anderem:

- diese Flächen
- diesen Flächen
- davon
- daraus
- solche
- betroffene
- beeinträchtigte
- dort
- hier beschrieben
- daraus bereitete Erzeugnisse

Der Flow darf nicht nur schreiben: "Erzeugnis stammt von beeintraechtigter Flaeche." Er muss den ausloesenden Kontext mitfuehren, etwa: "Erzeugnis stammt von einer Parzelle, die durch Pestizideinsatz oder Hubschrauberabdrift mit nicht Bioland-konformen Pflanzenschutzmitteln als beeintraechtigt gilt."

## Redundanzregel

Redundante Anforderungen werden nicht geloescht. Jede quellengebundene Anforderung bleibt erhalten. Zusaetzlich werden semantische Beziehungen erfasst:

- identisch
- aehnlich
- teilweise ueberlappend
- allgemeiner als
- konkreter als
- widerspruechlich

Diese Beziehungen sind Forschungsoutput.

## AGROVOC-Regel

AGROVOC wird nicht direkt in jeder Anforderungszeile hart vergeben. Stattdessen wird zuerst ein interner Begriffskatalog aufgebaut:

- Document_Term
- Normalized_Term
- Term_Type
- Candidate_AGROVOC_Label
- Candidate_AGROVOC_URI
- Mapping_Status
- Mapping_Confidence

AGROVOC-Zuordnungen bleiben zunaechst Kandidaten und werden spaeter validiert.

## URL- und Formatregel fuer den Metadatenkatalog

Die Spalte `URL Uebermittlung / Vorlagen / Online-Programm` enthaelt nur URLs oder bleibt leer. Kein Begleittext.

Die Spalte `Format` verwendet moeglichst knappe, DCAT/DCT-nahe Formatlabels, zum Beispiel:

- HTML
- PDF
- CSV
- XLSX
- XML
- Upload-Datei

Wenn das exakte technische Format nicht belegt ist, darf aus Datenstruktur und Uebermittlungsart konservativ geschlossen werden. Unsichere Faelle sollen spaeter in einem QA-Protokoll markiert werden.

## Human Review

Alle KI-Ergebnisse erhalten einen Review-Status:

- raw_extracted
- needs_review
- reviewed
- approved
- rejected

Unklare Begriffe, weiche Pflichten und interpretative Anforderungen werden nicht geglaettet, sondern markiert.
