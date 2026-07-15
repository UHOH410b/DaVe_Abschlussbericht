# DaVe Abschlussbericht - digitale Anlagen

Dieses Repository enthält die ausgewählten digitalen Anlagen zum DaVe-Abschlussbericht.

Es ist bewusst schlank gehalten. Enthalten sind nur die Ergebnisse und Dokumente, die für den Bericht, die Nachvollziehbarkeit und eine spätere Weiterentwicklung wichtig sind.

## Inhalt

### 1. Ergebnisse

Ordner: `01_Ergebnisse/`

Enthalten sind:

- BPMN-2.0-Prozessdiagramme
- bereinigter AP-2-Metadatenkatalog

Diese Dateien sind die zentralen Ergebnisartefakte für den Abschlussbericht.

### 2. Agrardatenkatalog BW / Base44-Prototyp

Ordner: `02_Agrardatenkatalog_Base44/`

Der lauffähige Demonstrator **Agrardatenkatalog BW** bleibt zunächst in Base44. Der Link zur Base44-App kann im Abschlussbericht angegeben werden, damit die App praktisch getestet werden kann.

Dieses Repository enthält dazu:

- Architektur des Prototyps
- Einordnung der Base44-App und Migrationsoptionen
- Weaviate-Anbindungsdokumentation
- zentrale Datenmodell-Dateien des Anforderungskatalogs

GitHub ist damit die technische Dokumentation und übergabe. Base44 ist der laufende Demonstrator.

### 3. Berichtstext

Ordner: `03_Berichtstext/`

Enthalten ist ein Textbaustein zur Beschreibung des Agrardatenkatalog-Prototyps im Abschlussbericht.

## Was bewusst nicht enthalten ist

Nicht enthalten sind:

- echte API-Keys
- `.env`-Dateien
- Original-PDFs aus Standards oder Rechtsqüllen
- alte Arbeitskopien
- temporäre Pipeline-Zwischenstände
- vollständiger Base44-App-Code

## Hinweis zur App

Die Base44-App ist ein lauffähiger Forschungs- und Demonstrationsprototyp. Sie greift auf einen Weaviate-Suchindex zu. Die Live-Funktion kann davon abhängen, ob der Weaviate-Zugang und die Base44-Umgebung weiterhin aktiv sind.

Für eine langfristige technische Verstetigung wäre ein späterer Neuaufbau als eigenständige Web-App möglich. Dieses Repository enthält dafür die wichtigsten fachlichen und technischen Grundlagen.

## Qualitätshinweis

Der Agrardatenkatalog ist ein Prototyp. Die extrahierten Anforderungen sind für Forschung, Demonstration und Expert:innen-Evaluation geeignet, ersetzen aber keine Rechtsberatung.
