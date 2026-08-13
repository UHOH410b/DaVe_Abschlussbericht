import { NextResponse } from "next/server";
import { buildAtomicRequirementQuery, collectionRows, weaviateGraphql } from "@/lib/weaviate";

export async function POST(request) {
  const body = await request.json().catch(() => ({}));
  const query = String(body.query || "").trim();
  const sourceIds = Array.isArray(body.sourceIds) ? body.sourceIds : [];
  const limit = Number(body.limit || process.env.SEARCH_LIMIT_DEFAULT || 30);

  if (!query) {
    return NextResponse.json({ error: "Bitte eine Suchfrage eingeben.", results: [] }, { status: 400 });
  }

  const result = await weaviateGraphql(buildAtomicRequirementQuery({ query, sourceIds, limit }));

  if (!result.ok) {
    return NextResponse.json(
      {
        error: result.error,
        details: result.details || null,
        results: []
      },
      { status: result.status || 500 }
    );
  }

  const results = collectionRows(result.data).map((row) => ({
    id: row.object_id,
    score: row._additional?.score || null,
    sourceId: row.source_document_id || "",
    source: row.source_display || row.source_short_title || row.source_title || "-",
    sourceFullTitle: row.source_long_name || row.source_title || "",
    sourceUrl: row.source_url || "",
    citation: row.source_citation || row.source_reference || "",
    reference: row.source_reference || "",
    text: row.text || "",
    originalText: row.original_text || "",
    requirementType: row.requirement_type || "",
    documentType: row.document_type || "",
    actor: row.actor || "",
    action: row.action || "",
    object: row.object || "",
    condition: row.condition || "",
    deadline: row.deadline_or_frequency || "",
    evidence: row.evidence_required || ""
  }));

  return NextResponse.json({ results });
}
