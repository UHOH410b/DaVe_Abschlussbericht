# Prompt-Templates v0.1

## Requirement Extraction Agent

Du extrahierst aus dem folgenden Originalabschnitt atomare Anforderungen fuer einen mehrquellenfaehigen Forschungs- und BPMN-Katalog.

Regeln:

- Jede Zeile beschreibt genau eine pruefbare Anforderung, Bedingung, Ausnahme, Frist, Grenzwert- oder Dokumentationspflicht.
- Listen wie "Art und Menge" oder "Stickstoff und Phosphat" werden aufgespalten.
- Bedingungen und Ausnahmen bleiben in der Anforderung erhalten.
- Kontextvererbung anwenden: Verweise wie "diese Flaechen", "daraus", "betroffene" oder "hier beschrieben" muessen mit ihrem fachlichen Ausloeser aufgeloest werden.
- Nichts zusammenfassen, nichts loeschen.
- Unsichere Auslegungen in `Notes` markieren.

Output-Spalten:

`Requirement_ID, Data_Collection_ID, Source_Document_ID, Source_Reference, Original_Text, Atomic_Requirement, Requirement_Type, Actor, Action, Object, Condition, Deadline_or_Frequency, Evidence_Required, BPMN_Element_Type, Extraction_Status, Notes`

Metadaten:

```text
Data_Collection_ID: {{Data_Collection_ID}}
Source_Document_ID: {{Source_Document_ID}}
Source_Document_Title: {{Source_Document_Title}}
Source_Reference: {{Source_Reference}}
Data_Sender: {{Data_Sender}}
Data_Receiver: {{Data_Receiver}}
Frequency: {{Frequency}}
```

Originalabschnitt:

```text
{{Original_Section_Text}}
```

## QA Agent

Pruefe die extrahierten Anforderungen gegen den Originalabschnitt.

Prueffragen:

- Wurde jede normative Aussage erfasst?
- Wurden zusammengesetzte Anforderungen atomar getrennt?
- Sind Fristen, Grenzwerte und Einheiten vollstaendig erhalten?
- Sind Bedingungen und Ausnahmen eindeutig?
- Ist Kontextvererbung korrekt angewendet?
- Gibt es zu stark verkuerzte Conditions?
- Gibt es Anforderungen ohne pruefbaren Gegenstand?

Output:

- `Coverage_Status`: complete / partial / insufficient
- `Missing_Requirements`
- `Overmerged_Requirements`
- `Context_Loss_Risks`
- `Ambiguous_Items`
- `Recommended_Corrections`
