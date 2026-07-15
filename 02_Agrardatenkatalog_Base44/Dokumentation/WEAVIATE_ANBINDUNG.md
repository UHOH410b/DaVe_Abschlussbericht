# Weaviate-Anbindung

## Aktueller Stand

Der Prototyp nutzt Weaviate als Suchspeicher fuer den Agrardatenkatalog. Wegen des aktuellen Weaviate-Tarifs arbeiten wir mit einer Collection:

`AtomicRequirement`

In dieser Collection liegen drei Arten von Eintraegen. Sie werden ueber das Feld `record_type` unterschieden:

- `atomic_requirement`: atomare Anforderungen aus Gesetzen, Standards und Richtlinien
- `source_document`: Quellendokumente, also z. B. Gesetze, Verordnungen, Standards oder Richtlinien
- `data_collection`: Datenerhebungen aus dem Metadatenkatalog

Damit koennen wir trotzdem getrennt suchen und anzeigen, ohne mehrere Collections anlegen zu muessen.

## Lokale Konfiguration

Die Zugangsdaten werden lokal in einer Datei `.env` im Ordner `work/ki-flow-anforderungskatalog/` gespeichert.

Beispiel:

```env
WEAVIATE_URL="https://dein-cluster.weaviate.cloud"
WEAVIATE_API_KEY="dein-weaviate-api-key"
WEAVIATE_REQUIREMENT_COLLECTION="AtomicRequirement"
WEAVIATE_SECTION_COLLECTION="DocumentSection"
WEAVIATE_VECTORIZER="none"
```

Die Vorlage liegt in `.env.example`.

Wichtig: Der echte API-Key gehoert nicht ins GitLab, nicht in Screenshots und nicht in den Abschlussbericht.

## Wichtige Felder

Fuer atomare Anforderungen sind vor allem diese Felder wichtig:

- `record_type`
- `requirement_id`
- `source_document_id`
- `source_display`
- `source_reference`
- `requirement_text`
- `literal_quote`
- `requirement_type`
- `actor`
- `action`
- `object`
- `condition`
- `deadline_or_frequency`
- `evidence_required`
- `source_type`

Fuer Quellendokumente sind vor allem diese Felder wichtig:

- `record_type`
- `source_document_id`
- `short_title`
- `full_title`
- `source_display`
- `source_type`
- `description`
- `version`
- `url`

## Befehle

Verbindung testen:

```powershell
& "C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "work\ki-flow-anforderungskatalog\scripts\weaviate_smoke_test.py"
```

Trockenlauf fuer Upload:

```powershell
& "C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "work\ki-flow-anforderungskatalog\scripts\weaviate_upload.py" --dry-run
```

Echter Upload:

```powershell
& "C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "work\ki-flow-anforderungskatalog\scripts\weaviate_upload.py"
```

Suche testen:

```powershell
& "C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "work\ki-flow-anforderungskatalog\scripts\weaviate_search.py" --query "Stickstoff Hektar"
```

## Spaetere Erweiterung

Wenn ein Weaviate-Tarif mit mehreren Collections genutzt wird, koennen `source_document`, `data_collection` und `atomic_requirement` in eigene Collections getrennt werden. Fuer den aktuellen Prototyp ist die Trennung ueber `record_type` ausreichend und einfacher zu betreiben.
