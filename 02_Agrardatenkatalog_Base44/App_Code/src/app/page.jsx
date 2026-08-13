"use client";

import { useEffect, useMemo, useState } from "react";
import { BookOpen, ChevronDown, ChevronRight, Database, FileText, Search } from "lucide-react";

const examples = [
  "Was muss ich im Bioland-Hopfenanbau zum Abstand zu konventionellen Hopfengärten beachten?",
  "Was muss ich beim Einsatz von Pflanzenschutzmitteln in der Nähe von Gewässern beachten?",
  "Welche Aufzeichnungspflichten bestehen bei der Düngung?",
  "Welche Anforderungen gelten für Traubenerzeuger?"
];

export default function HomePage() {
  const [query, setQuery] = useState("");
  const [sources, setSources] = useState([]);
  const [sourceError, setSourceError] = useState("");
  const [selectedSources, setSelectedSources] = useState([]);
  const [results, setResults] = useState([]);
  const [expanded, setExpanded] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [tab, setTab] = useState("search");

  useEffect(() => {
    fetch("/api/sources")
      .then((response) => response.json())
      .then((payload) => {
        if (payload.error) {
          setSourceError(payload.error);
        }
        setSources(payload.sources || []);
      })
      .catch((err) => setSourceError(err.message));
  }, []);

  const selectedSourceSet = useMemo(() => new Set(selectedSources), [selectedSources]);

  function toggleSource(id) {
    setSelectedSources((current) =>
      current.includes(id) ? current.filter((entry) => entry !== id) : [...current, id]
    );
  }

  async function runSearch(event) {
    event?.preventDefault();
    if (!query.trim()) {
      setError("Bitte eine Frage eingeben.");
      return;
    }

    setLoading(true);
    setError("");
    setExpanded({});

    try {
      const response = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          sourceIds: selectedSources,
          limit: 40
        })
      });
      const payload = await response.json();
      if (!response.ok || payload.error) {
        throw new Error(payload.error || "Suche fehlgeschlagen.");
      }
      setResults(payload.results || []);
      setTab("search");
    } catch (err) {
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <Database size={28} />
          <div>
            <strong>Agrardatenkatalog</strong>
            <span>Baden-Württemberg</span>
          </div>
        </div>

        <button className={tab === "search" ? "nav active" : "nav"} onClick={() => setTab("search")}>
          <Search size={18} />
          Anforderungssuche
        </button>
        <button className={tab === "sources" ? "nav active" : "nav"} onClick={() => setTab("sources")}>
          <BookOpen size={18} />
          Quellendokumente
        </button>
      </aside>

      <section className="content">
        {tab === "search" ? (
          <>
            <header className="pageHeader">
              <h1>Anforderungssuche</h1>
              <p>Durchsucht den Weaviate-Katalog nach atomaren Anforderungen.</p>
            </header>

            <form className="searchBox" onSubmit={runSearch}>
              <textarea
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
                    runSearch(event);
                  }
                }}
                placeholder="Stellen Sie eine Frage, z. B. Was muss ich bei Bioland-Hopfenanbau beachten?"
              />
              <div className="exampleRow">
                {examples.map((example) => (
                  <button key={example} type="button" onClick={() => setQuery(example)}>
                    {example}
                  </button>
                ))}
              </div>

              <details className="sourcePicker">
                <summary>Quellen eingrenzen ({selectedSources.length || "alle"})</summary>
                {sourceError ? <p className="notice error">{sourceError}</p> : null}
                <div className="sourceGrid">
                  {sources.map((source) => (
                    <label key={source.id}>
                      <input
                        type="checkbox"
                        checked={selectedSourceSet.has(source.id)}
                        onChange={() => toggleSource(source.id)}
                      />
                      <span>{source.title}</span>
                    </label>
                  ))}
                </div>
              </details>

              <div className="actions">
                <span>Strg/Cmd + Enter sucht ebenfalls.</span>
                <button type="submit" disabled={loading}>
                  <Search size={18} />
                  {loading ? "Suche läuft..." : "Antwort suchen"}
                </button>
              </div>
            </form>

            {error ? <p className="notice error">{error}</p> : null}

            <section className="resultPanel">
              <div className="resultHeader">
                <h2>Treffer</h2>
                <span>{results.length} Anforderungen</span>
              </div>
              {results.length === 0 ? (
                <p className="empty">Noch keine Treffer. Stellen Sie eine Frage oder wählen Sie Quellen aus.</p>
              ) : (
                <div className="table">
                  <div className="row head">
                    <span>Quelle</span>
                    <span>Anforderung</span>
                    <span>Fundstelle</span>
                  </div>
                  {results.map((result) => (
                    <article key={result.id} className="result">
                      <button
                        className="row"
                        onClick={() => setExpanded((state) => ({ ...state, [result.id]: !state[result.id] }))}
                      >
                        <span className="sourceName">{result.source}</span>
                        <span>{result.text}</span>
                        <span>{result.reference || result.citation || "-"}</span>
                        {expanded[result.id] ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
                      </button>
                      {expanded[result.id] ? (
                        <div className="details">
                          <Detail label="ID" value={result.id} />
                          <Detail label="Quellentyp" value={result.documentType} />
                          <Detail label="Anforderungstyp" value={result.requirementType} />
                          <Detail label="Akteur" value={result.actor} />
                          <Detail label="Handlung" value={result.action} />
                          <Detail label="Objekt" value={result.object} />
                          <Detail label="Bedingung" value={result.condition} />
                          <Detail label="Frist/Häufigkeit" value={result.deadline} />
                          <Detail label="Nachweis" value={result.evidence} />
                          <Detail label="Originalzitat" value={result.originalText} wide />
                          {result.sourceUrl ? (
                            <a href={result.sourceUrl} target="_blank" rel="noreferrer">
                              Quelle öffnen
                            </a>
                          ) : null}
                        </div>
                      ) : null}
                    </article>
                  ))}
                </div>
              )}
            </section>
          </>
        ) : (
          <SourcesView sources={sources} sourceError={sourceError} />
        )}
      </section>
    </main>
  );
}

function SourcesView({ sources, sourceError }) {
  return (
    <>
      <header className="pageHeader">
        <h1>Quellendokumente</h1>
        <p>Dokumente, aus denen Anforderungen und Katalogeinträge stammen.</p>
      </header>
      {sourceError ? <p className="notice error">{sourceError}</p> : null}
      <div className="cards">
        {sources.map((source) => (
          <article className="sourceCard" key={source.id}>
            <FileText size={20} />
            <div>
              <h2>{source.title}</h2>
              <p>{source.fullTitle || source.description || "Quellendokument im Agrardatenkatalog."}</p>
              <div className="meta">
                <span>{source.type || "Typ offen"}</span>
                <span>{source.format || "Format offen"}</span>
              </div>
              {source.url ? (
                <a href={source.url} target="_blank" rel="noreferrer">
                  Quelle öffnen
                </a>
              ) : null}
            </div>
          </article>
        ))}
      </div>
    </>
  );
}

function Detail({ label, value, wide = false }) {
  if (!value) {
    return null;
  }
  return (
    <div className={wide ? "detail wide" : "detail"}>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}
