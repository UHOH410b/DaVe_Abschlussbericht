# DaVe Abschlussbericht - digitale Anlagen

Dieses Repository enthaelt die ausgewaehlten digitalen Anlagen zum DaVe-Abschlussbericht.

Es ist bewusst schlank gehalten. Enthalten sind nur die Ergebnisse und Dokumente, die fuer den Bericht, die Nachvollziehbarkeit und eine spaetere Weiterentwicklung wichtig sind.

## Inhalt

### 1. Ergebnisse

Ordner: `01_Ergebnisse/`

Enthalten sind:

- BPMN-2.0-Prozessdiagramme
- bereinigter AP-2-Metadatenkatalog

Diese Dateien sind die zentralen Ergebnisartefakte fuer den Abschlussbericht.

### 2. Agrardatenkatalog BW / Base44-Prototyp

Ordner: `02_Agrardatenkatalog_Base44/`

Der lauffaehige Demonstrator **Agrardatenkatalog BW** bleibt zunaechst in Base44. Der Link zur Base44-App kann im Abschlussbericht angegeben werden, damit die App praktisch getestet werden kann.

Dieses Repository enthaelt dazu:

- Architektur des Prototyps
- Einordnung der Base44-App und Migrationsoptionen
- Weaviate-Anbindungsdokumentation
- zentrale Datenmodell-Dateien des Anforderungskatalogs

GitHub ist damit die technische Dokumentation und Uebergabe. Base44 ist der laufende Demonstrator.

### 3. Berichtstext

Ordner: `03_Berichtstext/`

Enthalten ist ein Textbaustein zur Beschreibung des Agrardatenkatalog-Prototyps im Abschlussbericht.

## Was bewusst nicht enthalten ist

Nicht enthalten sind:

- echte API-Keys
- `.env`-Dateien
- Original-PDFs aus Standards oder Rechtsquellen
- alte Arbeitskopien
- temporaere Pipeline-Zwischenstaende
- vollstaendiger Base44-App-Code

## Hinweis zur App

Die Base44-App ist ein lauffaehiger Forschungs- und Demonstrationsprototyp. Sie greift auf einen Weaviate-Suchindex zu. Die Live-Funktion kann davon abhaengen, ob der Weaviate-Zugang und die Base44-Umgebung weiterhin aktiv sind.

Fuer eine langfristige technische Verstetigung waere ein spaeterer Neuaufbau als eigenstaendige Web-App moeglich. Dieses Repository enthaelt dafuer die wichtigsten fachlichen und technischen Grundlagen.

## Qualitaetshinweis

Der Agrardatenkatalog ist ein Prototyp. Die extrahierten Anforderungen sind fuer Forschung, Demonstration und Expert:innen-Evaluation geeignet, ersetzen aber keine Rechtsberatung.
