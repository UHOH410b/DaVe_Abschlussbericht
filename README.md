# DaVe-Abschlussbericht – digitale Anlagen

Dieses Repository enthält die finalen digitalen Anlagen zum DaVe-Abschlussbericht. Es bündelt die für Nachvollziehbarkeit, Prüfung und spätere Weiterverwendung relevanten Ergebnisartefakte; Arbeitskopien, Zugangsdaten und urheberrechtlich geschützte Quelldokumente sind nicht enthalten.

## Inhalt

### 1. Ergebnisse der Forschungsarbeiten

Ordner: [`01_Ergebnisse`](01_Ergebnisse/)

- elf BPMN-Diagrammexporte: eine Gesamtprozesslandkarte und zehn Einzelprozesse
- zwei weiterbearbeitbare BPMN-2.0-Quelldateien
- finaler Metadatenkatalog mit 78 Datenerhebungen und vollständigem Linkverzeichnis
- finale Kostenanalyse für QZBW und BioZBW
- Sankey-Diagramme und zugehörige SankeyMATIC-Quelldateien

### 2. Agrardatenkatalog BW

Ordner: [`02_Agrardatenkatalog_Base44`](02_Agrardatenkatalog_Base44/)

- Datenmodell und konsolidierter Anforderungskatalog
- Architektur- und Übergabedokumentation des Base44-Forschungsdemonstrators
- eigenständiger Next.js-Nachbau der Suchoberfläche einschließlich serverseitiger Weaviate-Anbindung
- lokale Verarbeitungspipeline zur Erzeugung, Prüfung und Bereitstellung des Anforderungskatalogs

## Zentrale Ergebnisse der Kostenanalyse

Die finale enge Kostenrechnung umfasst ausschließlich zertifizierungsspezifische administrative Zusatzaufwände:

- QZBW: 1.336,25 Euro pro Jahr, 43 Tätigkeiten
- BioZBW: 1.316,25 Euro pro Jahr, 44 Tätigkeiten
- Differenz QZBW – BioZBW: 20,00 Euro

Die Rechenlogik, Annahmen, Quellen und SankeyMATIC-Codes sind in der finalen Arbeitsmappe dokumentiert.

## Nutzungshinweise

- BPMN-Dateien lassen sich beispielsweise mit Signavio, Camunda Modeler oder bpmn.io öffnen.
- Die Excel-Arbeitsmappen sind als finale Veröffentlichungsfassungen strukturiert; interne Protokoll- und Zwischenblätter wurden entfernt.
- Die App benötigt für die Live-Suche einen erreichbaren Weaviate-Cluster und lokale Umgebungsvariablen. Eine Beispieldatei ohne Zugangsdaten ist enthalten.

## Abgrenzung

Der Agrardatenkatalog BW ist ein Forschungs- und Demonstrationsprototyp. Die strukturierten Anforderungen und Datenerhebungen dienen Forschung, Nachvollziehbarkeit und Evaluation; sie ersetzen keine rechtliche, fachaufsichtliche oder zertifizierungsbezogene Einzelfallprüfung.
