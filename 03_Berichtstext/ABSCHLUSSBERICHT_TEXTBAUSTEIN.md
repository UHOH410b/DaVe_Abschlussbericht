# Textbaustein fuer den Abschlussbericht

## Prototyp: Agrardatenkatalog BW

Im Projekt wurde ein webbasiertes Demonstrationssystem entwickelt, das agrarische Grundlagendokumente, Standards und rechtliche Vorgaben in einen durchsuchbaren Anforderungskatalog ueberfuehrt. Ziel des Prototyps ist es, textuelle Regelwerke nicht nur als Dokumente bereitzustellen, sondern einzelne Pflichten, Verbote, Nachweis- und Dokumentationsanforderungen als atomare, quellengebundene Anforderungen verfuegbar zu machen.

Die technische Loesung besteht aus drei Teilen. Erstens werden Quellendokumente und Metadaten lokal verarbeitet. Dabei werden Dokumente segmentiert, relevante Textstellen erkannt und in atomare Anforderungen ueberfuehrt. Jede Anforderung enthaelt eine ID, den Anforderungstext, die Quelle, die Fundstelle, den betroffenen Akteur, Handlung, Objekt, Bedingung und soweit erkennbar Nachweis- oder Fristangaben. Zweitens werden die Ergebnisse in einer Weaviate-Collection gespeichert. Dort liegen atomare Anforderungen, Datenerhebungen und Quellendokumente als getrennte Objekttypen vor. Drittens greift eine Base44-Webanwendung auf diesen Suchraum zu und stellt eine nutzerfreundliche Anforderungssuche bereit.

Der lauffaehige Demonstrator wird als Base44-App bereitgestellt und kann ueber einen Link im Abschlussbericht aufgerufen werden. Er dient der praktischen Erprobung durch Projektbeteiligte und Expertinnen und Experten. Ergaenzend wird ein oeffentliches GitHub-Repository bereitgestellt. Dieses enthaelt nicht den vollstaendigen Base44-App-Code, sondern die fuer Nachvollziehbarkeit und spaetere Weiterentwicklung zentralen Artefakte: BPMN-Modell, Metadatenkatalog, Masterkatalog, Architekturunterlagen, Weaviate-Anbindungsdokumentation und zentrale Pipeline-Skripte. Damit ist die Base44-App der lauffaehige Prototyp, waehrend GitHub die technische Dokumentation und Uebergabe fuer einen moeglichen spaeteren Neuaufbau darstellt.

Die App erlaubt es Nutzerinnen und Nutzern, vor einer Suche konkrete Quellendokumente auszuwaehlen. Dadurch kann beispielsweise nur in den Bioland-Richtlinien oder nur in einer bestimmten Kombination aus Standard und Fachrecht gesucht werden. Bei breiten Fragen wie "Was muss ich bei Bioland beachten?" zeigt die App eine quellenbezogene Liste der Anforderungen in Dokumentreihenfolge. Bei engeren Fachfragen, etwa zu Hopfenanbau und Abstaenden zu konventionellen Flaechen, werden die relevantesten Anforderungen priorisiert. Die Ergebnisse enthalten neben dem Anforderungstext auch die Quelle und Fundstelle, sodass die Antwort nachvollziehbar bleibt.

Zum aktuellen Stand enthaelt der Prototyp 878 atomare Anforderungen, 70 Datenerhebungen und 46 Quellendokumente. Die Bioland-Richtlinien wurden regelbasiert in 554 atomare Rohanforderungen ueberfuehrt, die ECOVIN-Richtlinie in 44 Rohanforderungen. Weitere Anforderungen stammen unter anderem aus duengerechtlichen, pflanzenschutzrechtlichen, GAP-bezogenen und weinrechtlichen Quellen. Die Extraktion aus langen Standards ist als Rohimport zu verstehen und bedarf vor produktiver Nutzung einer fachlichen Qualitaetspruefung.

Der Prototyp zeigt, wie heterogene Agrardokumente in einen gemeinsamen Daten- und Suchraum ueberfuehrt werden koennen. Gleichzeitig bleiben Redundanzen zwischen Dokumenten erhalten. Dies ist fachlich relevant, weil ueberschneidende Anforderungen zwischen Fachrecht, Foerderung und privaten Standards nicht als Fehler geloescht werden, sondern als Forschungsbefund sichtbar bleiben koennen.

## Was die App demonstriert

- Auswahl konkreter Quellendokumente vor der Suche
- Suche nach atomaren Anforderungen in natuerlicher Sprache
- Anzeige von Quelle, Fundstelle und Anforderungstext
- breite Quellenabfragen mit Trefferanzahl und Dokumentreihenfolge
- Trennung von atomaren Anforderungen, Datenerhebungen und Quellendokumenten
- vorbereiteter Import-Flow fuer neue PDF-Quellen

## Einordnung

Die App ist kein rechtsverbindliches Beratungssystem, sondern ein Forschungs- und Demonstrationsprototyp. Sie zeigt, wie KI-gestuetzte Inhaltsanalyse, strukturierte Metadaten und Suchtechnologien kombiniert werden koennen, um agrarische Anforderungen auffindbar und vergleichbar zu machen.

## Vorschlag fuer Abbildungsunterschriften

1. "Architektur des Prototyps: Von Quellendokumenten und Metadaten ueber lokale Extraktion und Weaviate bis zur Base44-Webanwendung."
2. "Anforderungssuche mit Quellenfilter: Nutzerinnen und Nutzer koennen vor der Suche festlegen, in welchen Standards oder Rechtsquellen gesucht werden soll."
3. "Ergebnisansicht einer natuerlichen Frage: Atomare Anforderungen werden mit Quelle, Fundstelle und Anforderungstext angezeigt."
4. "Quellendokumente im Katalog: Uebersicht ueber die im Suchraum enthaltenen Standards, Gesetze und Richtlinien."
