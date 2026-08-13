import { NextResponse } from "next/server";
import { buildSourcesQuery, collectionRows, weaviateGraphql } from "@/lib/weaviate";

export async function GET() {
  const result = await weaviateGraphql(buildSourcesQuery());

  if (!result.ok) {
    return NextResponse.json(
      {
        error: result.error,
        details: result.details || null,
        sources: []
      },
      { status: result.status || 500 }
    );
  }

  const sources = collectionRows(result.data)
    .map((row) => ({
      id: row.source_document_id || row.object_id,
      title: row.source_display || row.source_short_title || row.source_title || row.object_id,
      fullTitle: row.source_long_name || row.source_title || "",
      url: row.source_url || "",
      format: row.source_format || "",
      type: row.document_type || "",
      description: row.description || ""
    }))
    .filter((row) => row.id)
    .sort((a, b) => a.title.localeCompare(b.title, "de"));

  return NextResponse.json({ sources });
}
