# Architekturuebersicht

## Kurzbeschreibung

Der Prototyp besteht aus drei Ebenen:

1. Lokale Verarbeitung von Dokumenten und Metadaten
2. Suchindex in Weaviate
3. Nutzeroberflaeche in Base44

Die App selbst beantwortet Fragen nicht aus frei erfundenem Wissen, sondern sucht in einem Katalog aus quellengebundenen Objekten. Dadurch bleiben Quelle, Fundstelle und Originalkontext sichtbar.

## Komponenten

```mermaid
flowchart TB
    subgraph Input["Eingangsdaten"]
        M["Metadatenkatalog: Datenerhebungen und Quellen"]
        P["PDFs und HTML-Quellen"]
    end

    subgraph Local["Lokale KI-/ETL-Pipeline"]
        S1["Dokumentsegmentierung"]
        S2["Extraktion atomarer Anforderungen"]
        S3["Normalisierung und IDs"]
        S4["Kategorien und Aehnlichkeitskandidaten"]
        S5["Export nach JSONL"]
    end

    subgraph Index["Weaviate"]
        W["Collection: AtomicRequirement"]
        R1["record_type = atomic_requirement"]
        R2["record_type = data_collection"]
        R3["record_type = source_document"]
    end

    subgraph App["Base44-App"]
        Q["Anforderungssuche"]
        D["Quellendokumente"]
        I["Import neuer Quellen"]
    end

    M --> S1
    P --> S1
    S1 --> S2 --> S3 --> S4 --> S5 --> W
    W --> R1
    W --> R2
    W --> R3
    W --> Q
    W --> D
    I -. geplanter Flow .-> S1
```

## Datenmodell im Suchindex

```mermaid
erDiagram
    SOURCE_DOCUMENT ||--o{ ATOMIC_REQUIREMENT : "liefert"
    SOURCE_DOCUMENT ||--o{ DATA_COLLECTION : "begruendet"
    DATA_COLLECTION ||--o{ ATOMIC_REQUIREMENT : "kann betreffen"

    SOURCE_DOCUMENT {
      string source_document_id
      string source_display
      string source_title
      string document_type
      string source_url
      string source_format
      string description
    }

    ATOMIC_REQUIREMENT {
      string requirement_id
      string source_document_id
      string source_reference
      string text
      string original_text
      string actor
      string action
      string object
      string condition
      string evidence_required
    }

    DATA_COLLECTION {
      string data_collection_id
      string short_title
      string description
      string data_sender
      string data_receiver
      string frequency
      string format
    }
```

## Suchlogik in der App

```mermaid
flowchart LR
    A["Nutzer waehlt Quellen"] --> B["Nutzer stellt Frage"]
    B --> C{"Breite Quellenfrage?"}
    C -- ja --> D["Liste Anforderungen aus ausgewaehlter Quelle in Dokumentreihenfolge"]
    C -- nein --> E["Relevanzsuche in Weaviate"]
    E --> F["Filter: record_type = atomic_requirement"]
    F --> G["Gruppierung nach Quelle und Relevanz"]
    D --> H["Antworttabelle mit Fundstellen"]
    G --> H
```

## Warum Weaviate?

Weaviate dient als zentraler Suchraum fuer heterogene Objekte. Aktuell wird BM25/Textsuche genutzt. Spaeter kann ein echter Vektorindex mit Embeddings ergaenzt werden, um semantische Aehnlichkeit robuster abzubilden.

## Warum Base44?

Base44 liefert eine schnelle Weboberflaeche fuer den Prototyp:

- keine lokale Installation fuer Testnutzer
- schnelle Anpassung der UI
- einfache Demonstration im Abschlussbericht
- gute Trennung zwischen Datenkatalog, Anforderungssuche und Importseite

## Grenzen des Prototyps

- Bioland und ECOVIN wurden regelbasiert importiert und muessen fachlich geprueft werden.
- Nicht alle Dokumente sind vollstaendig extrahiert.
- Der PDF-Import in der App ist als Zielbild vorbereitet, aber noch nicht als vollautomatischer Produktionsdienst umgesetzt.
- Echte API-Keys und urheberrechtlich geschuetzte PDFs gehoeren nicht in das GitLab.
