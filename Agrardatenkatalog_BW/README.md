# Agrardatenkatalog BW

Dieser Ordner enthält die fachlichen und technischen Ergebnisartefakte des Forschungsdemonstrators **Agrardatenkatalog BW**.

## Inhalt

- [`Datenmodell`](Datenmodell/): konsolidierter Anforderungskatalog, Datenerhebungen und Quellendokumente
- [`Dokumentation`](Dokumentation/): Architektur, Base44-Einordnung, Migration und Weaviate-Anbindung
- [`Pipeline`](Pipeline/): lokale Python-Skripte und Spezifikationen zur Aufbereitung, Prüfung und Bereitstellung der Daten
- [`App_Code`](App_Code/): eigenständiger Next.js-Nachbau der Suchoberfläche mit serverseitiger Weaviate-Anbindung

## Einordnung der App-Fassungen

Die im Projekt eingesetzte Base44-App ist der ursprünglich erprobte Demonstrator. Da Base44 keinen vollständigen klassischen Quellcodeexport bereitstellt, enthält dieses Repository zusätzlich einen eigenständigen Next.js-Nachbau der zentralen Such- und Recherchefunktionen. Der Nachbau dient der technischen Reproduzierbarkeit und einer möglichen Migration; er ist kein automatischer Export der proprietären Base44-Anwendung.

## Voraussetzungen für eine Live-Suche

Für die lokale oder gehostete Ausführung werden ein erreichbarer Weaviate-Cluster und die in den Beispieldateien beschriebenen Umgebungsvariablen benötigt. Echte Zugangsdaten sind nicht enthalten. Ohne aktiven Suchindex bleiben Code, Datenmodell und Dokumentation nachvollziehbar, die dynamische Suche ist dann jedoch nicht ausführbar.

## Qualitätshinweis

Der Prototyp unterstützt Forschung und Evaluation. Er ist weder ein produktives Zertifizierungssystem noch eine rechtsverbindliche Auskunft.
