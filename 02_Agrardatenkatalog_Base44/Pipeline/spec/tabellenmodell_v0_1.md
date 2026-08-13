# Tabellenmodell v0.1

## Source_Document_Metadata

Quelle: `input/source_document_metadata.xlsx`

Wichtige Felder:

- `Source_Document_ID`
- `dct_title`
- `dct_type`
- `dct_source`
- `access_url`
- `jurisdiction_or_scope`
- `sector_scope`
- `data_sender`
- `data_receiver`
- `frequency`
- `format`
- `transmission_url`

## Atomic_Requirements

- `Requirement_ID`
- `Source_Document_ID`
- `Source_Reference`
- `Original_Text`
- `Atomic_Requirement`
- `Requirement_Type`
- `Normative_Trigger`
- `Actor`
- `Action`
- `Object`
- `Condition`
- `Exception`
- `Deadline_or_Frequency`
- `Evidence_Required`
- `Data_Object_IDs`
- `Parameter_IDs`
- `Term_IDs`
- `BPMN_Element_Type`
- `Suggested_Process`
- `Control_Point`
- `Ambiguity_Flag`
- `Extraction_Status`
- `Notes`

## Term_Catalog

- `Term_ID`
- `Document_Term`
- `Normalized_Term`
- `Term_Type`
- `Definition_Working`
- `Related_Requirement_IDs`
- `Candidate_AGROVOC_Label`
- `Candidate_AGROVOC_URI`
- `Mapping_Status`
- `Mapping_Confidence`
- `Notes`

## Data_Object_Catalog

- `Data_Object_ID`
- `Data_Object_Name`
- `Data_Object_Type`
- `Related_Requirement_IDs`
- `Likely_Data_Sender`
- `Likely_Data_Receiver`
- `Format`
- `Notes`

## Parameter_Catalog

- `Parameter_ID`
- `Parameter_Name`
- `Parameter_Value`
- `Parameter_Unit`
- `Threshold_Type`
- `Related_Requirement_IDs`
- `Notes`

## Requirement_Relations

- `Relation_ID`
- `Requirement_ID_A`
- `Requirement_ID_B`
- `Relation_Type`
- `Similarity_Rationale`
- `Confidence`
- `Reviewer_Notes`

## QA_Log

- `QA_ID`
- `Source_Document_ID`
- `Source_Reference`
- `Issue_Type`
- `Issue_Description`
- `Affected_IDs`
- `Reviewer`
- `Status`
