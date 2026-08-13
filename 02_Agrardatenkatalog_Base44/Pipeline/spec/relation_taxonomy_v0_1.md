# Relationstypen v0.1

Diese Typen beschreiben Beziehungen zwischen atomaren Anforderungen aus unterschiedlichen Quellen.

## Echte Redundanz

Zwei Anforderungen meinen fachlich fast dasselbe.

Kriterien:

- gleicher Pflichttyp
- gleiches oder sehr ähnliches Objekt
- gleiche Bedingung oder gleicher Anwendungsfall
- keine relevanten abweichenden Grenzwerte, Fristen oder Ausnahmen

Beispiel: Zwei Standards verlangen dieselbe Aufzeichnung für denselben Vorgang.

## Teilweise Überlappung

Zwei Anforderungen überschneiden sich fachlich, sind aber nicht deckungsgleich.

Kriterien:

- gleicher Themenbereich
- ähnliche Handlung oder ähnliches Objekt
- aber anderer Umfang, andere Bedingung, andere Frist oder andere Detailtiefe

## Gleiches Pflichtmuster, anderes Objekt

Die Anforderungen haben dieselbe Art von Pflicht, betreffen aber unterschiedliche Dinge.

Beispiel:

- Düngeaufzeichnungen sieben Jahre aufbewahren
- Pflanzenschutzmittel-Aufzeichnungen aufbewahren

Das ist keine Redundanz. Es ist ein wiederkehrendes Muster.

## Gleiches Thema, andere Pflicht

Die Anforderungen liegen im selben Themenbereich, verlangen aber unterschiedliche Handlungen.

Beispiel:

- Stickstoffmenge aufzeichnen
- Stickstoffgrenzwert einhalten

## Konkretisiert

Anforderung A ist allgemeiner, Anforderung B macht sie konkreter.

Beispiel:

- Standard verlangt Nährstoffdokumentation.
- Fachrecht nennt genaue Felder und Fristen.

## Potenzieller Konflikt

Anforderungen betreffen denselben Gegenstand, enthalten aber unterschiedliche oder widersprüchliche Vorgaben.

Beispiel:

- unterschiedliche Grenzwerte
- unterschiedliche Fristen
- eine Quelle erlaubt etwas, eine andere verbietet es

## Nur Suchtreffer

Die Anforderungen teilen einzelne Wörter oder grobe Themen, sind aber fachlich nicht relevant verbunden.

Diese Treffer sollten nicht als Forschungsergebnis gewertet werden.

## Review-Regel

Automatisch erkannte Relationen sind Kandidaten. Sie brauchen einen Review-Status:

- `candidate`
- `reviewed_valid`
- `reviewed_invalid`
- `needs_domain_review`
