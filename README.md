# DaVe-Abschlussbericht – digitale Anlagen

Dieses Repository enthält die finalen digitalen Anlagen zum DaVe-Abschlussbericht. Alle Verzeichnisse auf der obersten Ebene sind gleichrangige Ergebnisartefakte des Projekts. Arbeitskopien, Zugangsdaten und urheberrechtlich geschützte Quelldokumente sind nicht enthalten.

## Ergebnisartefakte

- [`BPMN`](BPMN/): eine Gesamtprozesslandkarte und zehn Einzelprozessdiagramme als hochauflösende PNG-Dateien sowie zwei weiterbearbeitbare BPMN-2.0-Modelle
- [`Metadatenkatalog`](Metadatenkatalog/): finale Excel-Fassung mit 78 Datenerhebungen, zwölf harmonisierten Metadatenfeldern und 297 aufrufbaren Links
- [`Kostenanalyse`](Kostenanalyse/): finale Kostenrechnung für QZBW und BIOZBW einschließlich Quellen, Annahmen, Sankey-Diagrammen und SankeyMATIC-Codes
- [`Agrardatenkatalog_BW`](Agrardatenkatalog_BW/): Datenmodell, Dokumentation, Verarbeitungspipeline und eigenständiger Next.js-Nachbau des Forschungsdemonstrators

## Zentrale Ergebnisse der Kostenanalyse

Die enge Kostenrechnung umfasst ausschließlich zertifizierungsspezifische administrative Zusatzaufwände:

- QZBW: 1.336,25 Euro pro Jahr, 42,125 Stunden und 43 Tätigkeiten
- BIOZBW: 1.316,25 Euro pro Jahr, 42,125 Stunden und 44 Tätigkeiten
- Differenz QZBW – BIOZBW: 20,00 Euro

Die Rechenlogik, Annahmen, Quellen und SankeyMATIC-Codes sind in der finalen Arbeitsmappe dokumentiert.

## Nutzungshinweise

- BPMN-Dateien lassen sich beispielsweise mit Signavio, Camunda Modeler oder bpmn.io öffnen.
- Die Excel-Arbeitsmappen sind bereinigte Veröffentlichungsfassungen; interne Protokoll- und Zwischenblätter wurden entfernt.
- Die Live-Suche des Agrardatenkatalogs benötigt einen erreichbaren Weaviate-Cluster und lokale Umgebungsvariablen. Beispieldateien ohne Zugangsdaten sind enthalten.

## Abgrenzung

Der Agrardatenkatalog BW ist ein Forschungs- und Demonstrationsprototyp. Die strukturierten Anforderungen und Datenerhebungen dienen Forschung, Nachvollziehbarkeit und Evaluation; sie ersetzen keine rechtliche, fachaufsichtliche oder zertifizierungsbezogene Einzelfallprüfung.
