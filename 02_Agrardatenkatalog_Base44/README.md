# 02 Agrardatenkatalog BW

Dieser Ordner dokumentiert den Forschungsdemonstrator **Agrardatenkatalog BW** und stellt seine fachlichen Daten, die Verarbeitungspipeline sowie einen eigenständigen Nachbau der Suchoberfläche bereit.

## Inhalt

- [`Datenmodell`](Datenmodell/): konsolidierter Anforderungskatalog, Datenerhebungen und Quellendokumente
- [`Dokumentation`](Dokumentation/): Architektur, Base44-Einordnung, Migration und Weaviate-Anbindung
- [`Pipeline`](Pipeline/): lokale Python-Skripte und Spezifikationen zur Aufbereitung, Prüfung und Bereitstellung der Daten
- [`App_Code`](App_Code/): Next.js-Nachbau der Oberfläche mit serverseitiger Weaviate-Anbindung

## Einordnung der beiden App-Fassungen

Die im Projekt eingesetzte Base44-App ist der ursprüngliche, interaktiv erprobte Demonstrator. Da Base44 keinen vollständigen klassischen Quellcodeexport der Anwendung bereitstellt, enthält dieses Repository zusätzlich einen eigenständigen Next.js-Nachbau der zentralen Funktionen. Dieser Code bildet insbesondere Quellenfilter, Anforderungssuche, Trefferansicht und Quellendokumentübersicht ab und dient der technischen Reproduzierbarkeit sowie einer möglichen Migration.

## Voraussetzungen für eine Live-Suche

Für die lokale oder gehostete Ausführung werden ein erreichbarer Weaviate-Cluster und die in den Beispieldateien beschriebenen Umgebungsvariablen benötigt. Echte Zugangsdaten sind nicht enthalten. Ohne aktiven Suchindex bleiben Code, Datenmodell und Dokumentation vollständig nachvollziehbar, die dynamische Suche ist dann jedoch nicht ausführbar.

## Qualitätshinweis

Der Prototyp unterstützt Forschung und Evaluation. Er ist weder ein produktives Zertifizierungssystem noch eine rechtsverbindliche Auskunft.
