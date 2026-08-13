const DEFAULT_COLLECTION = "AtomicRequirement";

export function getWeaviateConfig() {
  const url = process.env.WEAVIATE_URL?.replace(/\/$/, "");
  const apiKey = process.env.WEAVIATE_API_KEY;
  const collection = process.env.WEAVIATE_COLLECTION || DEFAULT_COLLECTION;

  if (!url || !apiKey) {
    return {
      ok: false,
      error: "WEAVIATE_URL oder WEAVIATE_API_KEY fehlt.",
      collection
    };
  }

  return { ok: true, url, apiKey, collection };
}

export async function weaviateGraphql(query) {
  const cfg = getWeaviateConfig();

  if (!cfg.ok) {
    return {
      ok: false,
      status: 500,
      error: cfg.error
    };
  }

  const response = await fetch(`${cfg.url}/v1/graphql`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${cfg.apiKey}`
    },
    body: JSON.stringify({ query }),
    cache: "no-store"
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok || payload.errors) {
    return {
      ok: false,
      status: response.status,
      error: payload.errors?.[0]?.message || response.statusText || "Weaviate-Abfrage fehlgeschlagen.",
      details: payload.errors || payload
    };
  }

  return {
    ok: true,
    status: response.status,
    data: payload.data
  };
}

export function gqlString(value = "") {
  return String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

export function buildSourceFilter(sourceIds = []) {
  const clean = sourceIds.filter(Boolean);
  if (!clean.length) {
    return "";
  }

  const operands = clean
    .map((id) => `{ path: ["source_document_id"], operator: Equal, valueText: "${gqlString(id)}" }`)
    .join(", ");

  return `, where: { operator: And, operands: [
    { path: ["record_type"], operator: Equal, valueText: "atomic_requirement" },
    { operator: Or, operands: [${operands}] }
  ] }`;
}

export function buildAtomicRequirementQuery({ query, sourceIds = [], limit = 30 }) {
  const cfg = getWeaviateConfig();
  const where = sourceIds.length
    ? buildSourceFilter(sourceIds)
    : ', where: { path: ["record_type"], operator: Equal, valueText: "atomic_requirement" }';

  return `
  {
    Get {
      ${cfg.collection}(
        bm25: { query: "${gqlString(query)}" }
        limit: ${Number(limit) || 30}
        ${where}
      ) {
        object_id
        record_type
        source_document_id
        source_reference
        source_title
        source_short_title
        source_long_name
        source_display
        source_url
        source_citation
        original_text
        text
        requirement_type
        document_type
        actor
        action
        object
        condition
        deadline_or_frequency
        evidence_required
        _additional {
          score
        }
      }
    }
  }`;
}

export function buildSourcesQuery() {
  const cfg = getWeaviateConfig();
  return `
  {
    Get {
      ${cfg.collection}(
        where: { path: ["record_type"], operator: Equal, valueText: "source_document" }
        limit: 200
      ) {
        object_id
        record_type
        source_document_id
        source_title
        source_short_title
        source_long_name
        source_display
        source_url
        source_format
        document_type
        description
      }
    }
  }`;
}

export function collectionRows(data) {
  const cfg = getWeaviateConfig();
  return data?.Get?.[cfg.collection] || [];
}
