# Vektorindex-Architektur v0.1

## Was ist ein Vektorindex?

Ein Vektorindex ist ein semantisches Suchregister. Texte werden nicht nur als Zeichenketten gespeichert, sondern zusaetzlich als numerische Vektoren. Texte mit aehnlicher Bedeutung liegen im Vektorraum nah beieinander.

Beispiel:

- `N-Bilanz bei Neuansaaten`
- `aufgebrachte Menge an Gesamtstickstoff`
- `jährliche betriebliche Gesamtsumme des Nährstoffeinsatzes`

Diese Texte enthalten nicht exakt dieselben Woerter, koennen aber semantisch nah beieinander liegen. Ein Vektorindex hilft, solche Naehe zu finden.

## Warum reicht eine Tabelle nicht?

Die Tabelle ist fuer Nachvollziehbarkeit, Filter und Export unverzichtbar:

- IDs
- Quellen
- Versionen
- Paragraphen
- Akteure
- Fristen
- BPMN-Zuordnung
- Review-Status

Der Vektorindex ist fuer semantische Aufgaben zustaendig:

- aehnliche Anforderungen finden
- Redundanzen zwischen Dokumenten erkennen
- Chatbot-Kontext abrufen
- Kategorien vorschlagen
- Begriffe und Synonyme zusammenfuehren

Beides wird kombiniert.

## Empfohlene hybride Struktur

### Dokumentbezogene Indizes

Pro Dokument bzw. Grundlagendokument wird ein Abschnittsindex aufgebaut.

Beispiele:

- `doc_SRC_BIOLAND_STD_2025_03_sections`
- `doc_SRC_DUEV_sections`
- `doc_SRC_PFLSCHG_sections`

Zweck:

- Suche nur in einem konkreten Dokument
- Auditierbarer Ruecksprung zum Originaltext
- einfaches Neuberechnen bei Versionswechsel

### Globale Indizes

Zusaetzlich gibt es globale Indizes ueber alle Quellen hinweg.

- `global_document_sections`
- `global_atomic_requirements`
- `global_terms`
- `global_data_objects`
- `global_categories`

Zweck:

- quellenuebergreifende Suche
- Redundanzanalyse
- Forschungsfragen
- Chatbot-Antworten ueber mehrere Standards hinweg

## Warum nicht nur ein Index pro Dokument?

Nur dokumentbezogene Indizes waeren fuer Einzelsuchen gut, aber fuer dein Forschungsziel zu schwach. Du willst gerade erkennen, ob Anforderungen in mehreren Dokumenten gleich, aehnlich, ueberlappend oder widerspruechlich sind. Dafuer braucht der Flow einen globalen Requirements-Index.

## Minimale erste Umsetzung

In dieser Arbeitsumgebung wird zunaechst eine vorbereitende Indexstruktur erzeugt:

- `vector_index/manifest.json`
- JSONL-Dateien mit indexierbaren Textobjekten
- stabile IDs fuer spaetere Embeddings

Die eigentlichen Embeddings koennen spaeter mit einer geeigneten Embedding-API oder einer lokalen Modellinfrastruktur erzeugt werden.

## Indexierbare Objekte

Jeder Indexeintrag sollte enthalten:

- `object_id`
- `object_type`
- `source_document_id`
- `data_collection_id`
- `source_reference`
- `text`
- `metadata`

## Spaetere technische Optionen

Moegliche Vektordatenbanken:

- Qdrant
- Chroma
- Weaviate
- pgvector/PostgreSQL
- OpenSearch Vector Search
- Cloud-native Vektorindizes

Fuer den Prototyp reicht eine JSONL-Struktur als Zwischenschritt. Das haelt die Architektur portabel.
