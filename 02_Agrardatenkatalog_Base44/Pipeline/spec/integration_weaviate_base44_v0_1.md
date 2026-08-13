# Integration Weaviate und Base44 v0.1

## Ziel

Der Anforderungskatalog soll später nicht nur als Excel-Datei existieren, sondern auch durchsuchbar und in einer App nutzbar sein. Dafür sind zwei Integrationen vorgesehen:

- Weaviate als Vektordatenbank für semantische Suche
- Base44 als Web-App für Dokumentenaufnahme, Suche, Review und Export

## Wann Weaviate sinnvoll ist

Weaviate sollte erst angebunden werden, wenn die Grundstruktur stabil ist:

1. Source Documents und Document Sections haben stabile IDs.
2. Atomic Requirements haben stabile IDs.
3. Kategorien und Relationen sind technisch erzeugbar.
4. Die Texte werden sauber mit Umlauten gespeichert.

Dann kann der Index jederzeit neu aufgebaut werden, ohne dass alte Testdaten stören.

## Geplante Weaviate-Objekte

### DocumentSection

Eine Textstelle aus einem Dokument.

Wichtige Felder:

- `document_section_id`
- `source_document_id`
- `source_title`
- `source_reference`
- `section_text`
- `url`
- `version`
- `retrieved_at`

### AtomicRequirement

Eine atomare Pflicht oder Regel.

Wichtige Felder:

- `requirement_id`
- `source_document_id`
- `source_reference`
- `atomic_requirement`
- `requirement_type`
- `actor`
- `action`
- `object`
- `condition`
- `deadline_or_frequency`
- `evidence_required`
- `primary_category`
- `secondary_categories`

## Was für die Weaviate-Anbindung benötigt wird

- Weaviate Cluster URL
- Weaviate API Key
- Entscheidung, welches Embedding-Modell genutzt wird
- Entscheidung, ob Embeddings in Weaviate erzeugt werden oder vorher durch unser Skript
- Name der Collections, z. B. `DocumentSection` und `AtomicRequirement`

## Base44-App: Grundidee

Die Base44-App soll später vier einfache Bereiche haben:

1. Dokumente hochladen oder URL eintragen
2. KI-Extraktion starten
3. Ergebnisse prüfen und freigeben
4. Katalog durchsuchen und exportieren

Die App sollte nicht direkt die Excel-Datei bearbeiten. Besser ist:

- Base44 schreibt neue Dokumente und Jobs in strukturierte Datentabellen.
- Ein Backend-Flow verarbeitet Dokumente abschnittsweise.
- Der Master-Katalog wird daraus neu erzeugt.
- Weaviate wird danach aktualisiert.

## Nächster technischer Schritt

Vor der echten App sollte ein lokaler Such-Prototyp entstehen. Dieser nutzt noch keine Weaviate-Datenbank, sondern sucht im aktuellen Master-Katalog. Wenn die Logik passt, wird dieselbe Struktur an Weaviate und Base44 angebunden.
