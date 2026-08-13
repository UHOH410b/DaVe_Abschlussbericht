# Verarbeitungspipeline des Agrardatenkatalogs BW

Die Pipeline bereitet heterogene Rechts-, Förder- und Standarddokumente für den quellengebundenen Agrardatenkatalog BW auf. Sie unterstützt Import, Segmentierung, Extraktion atomarer Anforderungen, Katalogkonsolidierung, Qualitätsprüfung, Export und die optionale Bereitstellung in Weaviate.

## Bestandteile

- [`scripts`](scripts/): Python-Skripte für Import, Verarbeitung, Prüfung, Export und Weaviate-Anbindung
- [`spec`](spec/): Tabellenmodell, Kategorien, Relationstaxonomie, Promptvorlagen und technische Architektur
- [`.env.example`](.env.example): Konfigurationsbeispiel ohne Zugangsdaten

Die konsolidierten, für die Veröffentlichung ausgewählten Datenstände befinden sich im benachbarten Ordner [`../Datenmodell`](../Datenmodell/).

## Verarbeitungslogik

```mermaid
flowchart LR
    A["Quellendokumente und Metadaten"] --> B["Import und Segmentierung"]
    B --> C["Extraktion atomarer Anforderungen"]
    C --> D["Validierung und Katalogkonsolidierung"]
    D --> E["Tabellen- und JSONL-Exporte"]
    E --> F["optionaler Weaviate-Suchindex"]
    F --> G["Agrardatenkatalog BW"]
```

## Lokale Nutzung

Vorausgesetzt werden Python 3.11 oder neuer sowie die jeweils in den Skripten importierten Bibliotheken. Zentrale Einstiegspunkte sind:

```powershell
python scripts/run_local_pipeline.py
python scripts/validate_metadata_catalog.py
python scripts/build_master_catalog.py
python scripts/build_vector_index_inputs.py
```

Für Weaviate werden zusätzlich die Variablen aus `.env.example` benötigt. Die Verbindung kann vor einem Upload geprüft werden:

```powershell
python scripts/weaviate_smoke_test.py
python scripts/weaviate_upload.py --dry-run
```

## Reproduzierbarkeit und Grenzen

Urheberrechtlich geschützte Quelldokumente und Zugangsdaten sind nicht Bestandteil des öffentlichen Repositorys. Einige Verarbeitungsschritte setzen deshalb lokal vorhandene Ausgangsdokumente voraus. Automatisch oder regelbasiert extrahierte Anforderungen sind als Forschungsdaten zu verstehen und benötigen vor einer rechtsverbindlichen oder produktiven Verwendung eine fachliche Prüfung.

## Sicherheit

`.env`, API-Schlüssel, Clusterzugänge und nicht freigegebene Quelldokumente dürfen nicht versioniert werden. Die enthaltenen Beispieldateien verwenden ausschließlich Platzhalter.
