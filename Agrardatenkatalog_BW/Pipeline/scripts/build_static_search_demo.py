from __future__ import annotations

import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
SEED_JSON = BASE / "output" / "base44_seed" / "base44_requirement_seed.json"
OUT_DIR = BASE / "output" / "static_demo"
OUT_HTML = OUT_DIR / "anforderungssuche_demo.html"
OUT_STANDALONE_HTML = OUT_DIR / "anforderungssuche_demo_standalone.html"
OUT_DATA = OUT_DIR / "requirements_data.js"
REPORT = OUT_DIR / "static_demo_report.md"


HTML = r"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Anforderungssuche Demo</title>
  <style>
    :root {
      --bg: #f6f7f8;
      --surface: #ffffff;
      --line: #d9dee5;
      --text: #20242a;
      --muted: #64707d;
      --brand: #2f6f4e;
      --brand-dark: #24573d;
      --accent: #c67c22;
      --chip: #edf3ef;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
      line-height: 1.45;
    }
    header {
      background: var(--surface);
      border-bottom: 1px solid var(--line);
      padding: 18px 24px 16px;
    }
    h1 {
      margin: 0 0 4px;
      font-size: 22px;
      font-weight: 700;
      letter-spacing: 0;
    }
    .sub {
      margin: 0;
      color: var(--muted);
      max-width: 960px;
    }
    main {
      padding: 18px 24px 32px;
      max-width: 1500px;
      margin: 0 auto;
    }
    .toolbar {
      display: grid;
      grid-template-columns: minmax(260px, 1.6fr) minmax(160px, .7fr) minmax(160px, .7fr) minmax(160px, .7fr) auto;
      gap: 10px;
      align-items: end;
      margin-bottom: 14px;
    }
    label {
      display: grid;
      gap: 5px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }
    input, select, button {
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--surface);
      color: var(--text);
      padding: 0 10px;
      font: inherit;
    }
    button {
      background: var(--brand);
      color: white;
      border-color: var(--brand);
      font-weight: 700;
      cursor: pointer;
      padding: 0 14px;
    }
    button:hover { background: var(--brand-dark); }
    .stats {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin: 0 0 14px;
    }
    .stat {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px 10px;
      color: var(--muted);
    }
    .stat strong { color: var(--text); }
    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 430px;
      gap: 16px;
      align-items: start;
    }
    .tableWrap {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: auto;
      max-height: calc(100vh - 210px);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 1080px;
    }
    th, td {
      border-bottom: 1px solid var(--line);
      padding: 9px 10px;
      text-align: left;
      vertical-align: top;
    }
    th {
      position: sticky;
      top: 0;
      background: #f0f3f2;
      z-index: 1;
      font-size: 12px;
      color: #47515c;
    }
    tr { cursor: pointer; }
    tr:hover { background: #f7faf8; }
    tr.active { background: #edf3ef; }
    .req {
      max-width: 460px;
      font-weight: 600;
    }
    .muted { color: var(--muted); }
    .chip {
      display: inline-block;
      background: var(--chip);
      color: var(--brand-dark);
      border: 1px solid #cfdfd4;
      border-radius: 999px;
      padding: 2px 8px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }
    aside {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      position: sticky;
      top: 14px;
      max-height: calc(100vh - 42px);
      overflow: auto;
    }
    aside h2 {
      margin: 0 0 10px;
      font-size: 17px;
      letter-spacing: 0;
    }
    .detailBlock {
      border-top: 1px solid var(--line);
      padding-top: 10px;
      margin-top: 10px;
    }
    .detailBlock h3 {
      margin: 0 0 6px;
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0;
    }
    .detailBlock p { margin: 0; }
    a { color: var(--brand-dark); }
    .empty {
      background: var(--surface);
      border: 1px dashed var(--line);
      border-radius: 8px;
      padding: 24px;
      color: var(--muted);
    }
    @media (max-width: 1100px) {
      .toolbar { grid-template-columns: 1fr 1fr; }
      .layout { grid-template-columns: 1fr; }
      aside { position: static; }
    }
    @media (max-width: 640px) {
      header, main { padding-left: 14px; padding-right: 14px; }
      .toolbar { grid-template-columns: 1fr; }
      .tableWrap { max-height: none; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Anforderungssuche</h1>
    <p class="sub">Lokaler Prototyp für atomare Anforderungen aus Standards, Fachrecht und Förderrichtlinien.</p>
  </header>
  <main>
    <section class="toolbar">
      <label>Suche
        <input id="q" type="search" placeholder="z. B. Stickstoff Hektar, Aufbewahrung, Pflanzenschutz">
      </label>
      <label>Hauptkategorie
        <select id="category"></select>
      </label>
      <label>Quelle
        <select id="source"></select>
      </label>
      <label>Pflichttyp
        <select id="type"></select>
      </label>
      <button id="exportBtn" type="button">CSV exportieren</button>
    </section>

    <section class="stats" id="stats"></section>

    <section class="layout">
      <div id="results"></div>
      <aside id="detail">
        <h2>Detail</h2>
        <p class="muted">Wähle links eine Anforderung aus.</p>
      </aside>
    </section>
  </main>

  <script src="requirements_data.js"></script>
  <script>
    const requirementRecords = (window.REQUIREMENTS_DATA.atomic_requirements || []).map(r => ({
      ...r,
      record_type: 'atomic_requirement',
      display_id: r.requirement_id,
      display_title: r.atomic_requirement,
      display_subtitle: `${r.source_reference || ''} ${r.source_title || ''}`.trim(),
      display_category: r.primary_category || 'Anforderung',
      display_actor: r.actor || '',
      display_frequency: r.deadline_or_frequency || '',
      display_evidence: r.evidence_required || ''
    }));
    const dataCollectionRecords = (window.REQUIREMENTS_DATA.data_collections || []).map(r => ({
      ...r,
      record_type: 'data_collection',
      display_id: r.data_collection_id || r.object_id,
      display_title: r.short_title,
      display_subtitle: r.description,
      display_category: 'Datenerhebung',
      display_actor: `${r.data_sender || ''} -> ${r.data_receiver || ''}`.trim(),
      display_frequency: r.frequency || '',
      display_evidence: r.format || ''
    }));
    const records = [...requirementRecords, ...dataCollectionRecords];
    const state = { selected: null, filtered: [] };

    const fields = {
      q: document.querySelector('#q'),
      category: document.querySelector('#category'),
      source: document.querySelector('#source'),
      type: document.querySelector('#type'),
      results: document.querySelector('#results'),
      detail: document.querySelector('#detail'),
      stats: document.querySelector('#stats'),
      exportBtn: document.querySelector('#exportBtn')
    };

    function norm(value) {
      return String(value || '')
        .toLowerCase()
        .replaceAll('ä', 'ae')
        .replaceAll('ö', 'oe')
        .replaceAll('ü', 'ue')
        .replaceAll('ß', 'ss');
    }

    function textOf(record) {
      return norm([
        record.requirement_id,
        record.data_collection_id,
        record.short_title,
        record.description,
        record.data_sender,
        record.data_receiver,
        record.frequency,
        record.format,
        record.transmission_method,
        record.atomic_requirement,
        record.requirement_type,
        record.actor,
        record.action,
        record.object,
        record.condition,
        record.deadline_or_frequency,
        record.evidence_required,
        record.primary_category,
        (record.secondary_categories || []).join(' '),
        record.source_reference,
        record.source_title
      ].join(' '));
    }

    function unique(values) {
      return [...new Set(values.filter(Boolean).map(String))].sort((a, b) => a.localeCompare(b, 'de'));
    }

    function fillSelect(select, values, label) {
      select.innerHTML = `<option value="">${label}</option>` + values.map(v => `<option>${escapeHtml(v)}</option>`).join('');
    }

    function escapeHtml(value) {
      return String(value || '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
    }

    function initFilters() {
      fillSelect(fields.category, unique(records.map(r => r.record_type === 'data_collection' ? 'Datenerhebung' : r.primary_category)), 'Alle Kategorien');
      fillSelect(fields.source, unique(records.map(r => r.source_title || r.foundation_document_title || r.source_document_id)), 'Alle Quellen');
      fillSelect(fields.type, unique(records.map(r => r.requirement_type)), 'Alle Pflichttypen');
    }

    function score(record, terms) {
      if (!terms.length) return 1;
      const text = textOf(record);
      let score = 0;
      for (const term of terms) {
        if (text.includes(term)) score += 10;
        if (norm(record.display_category).includes(term)) score += 5;
        if (norm(record.source_reference).includes(term)) score += 4;
      }
      return score;
    }

    function applyFilters() {
      const terms = norm(fields.q.value).split(/[^a-z0-9.]+/).filter(Boolean);
      const cat = fields.category.value;
      const source = fields.source.value;
      const type = fields.type.value;

      state.filtered = records
        .map(record => ({ record, score: score(record, terms) }))
        .filter(item => item.score > 0)
        .filter(item => !cat || item.record.display_category === cat || item.record.primary_category === cat)
        .filter(item => !source || (item.record.source_title || item.record.foundation_document_title || item.record.source_document_id) === source)
        .filter(item => !type || item.record.requirement_type === type)
        .sort((a, b) => b.score - a.score || String(a.record.requirement_id).localeCompare(String(b.record.requirement_id)))
        .map(item => item.record);

      if (!state.selected || !state.filtered.some(r => r.requirement_id === state.selected.requirement_id)) {
        state.selected = state.filtered[0] || null;
      }
      render();
    }

    function renderStats() {
      fields.stats.innerHTML = [
        `<span class="stat"><strong>${state.filtered.length}</strong> Treffer</span>`,
        `<span class="stat"><strong>${requirementRecords.length}</strong> Anforderungen</span>`,
        `<span class="stat"><strong>${dataCollectionRecords.length}</strong> Datenerhebungen</span>`,
        `<span class="stat"><strong>${unique(records.map(r => r.source_document_id)).length}</strong> Quellen</span>`,
        `<span class="stat"><strong>${unique(records.map(r => r.display_category)).length}</strong> Kategorien</span>`
      ].join('');
    }

    function renderResults() {
      if (!state.filtered.length) {
        fields.results.innerHTML = '<div class="empty">Keine Treffer. Ändere Suche oder Filter.</div>';
        return;
      }
      const rows = state.filtered.map(record => {
        const active = state.selected && state.selected.display_id === record.display_id ? ' class="active"' : '';
        return `<tr${active} data-id="${escapeHtml(record.display_id)}">
          <td><strong>${escapeHtml(record.display_id)}</strong><br><span class="muted">${escapeHtml(record.record_type === 'data_collection' ? 'Datenerhebung' : record.source_reference)}</span></td>
          <td><span class="chip">${escapeHtml(record.display_category || 'ohne Kategorie')}</span></td>
          <td class="req">${escapeHtml(record.display_title)}</td>
          <td>${escapeHtml(record.display_actor)}</td>
          <td>${escapeHtml(record.display_frequency)}</td>
          <td>${escapeHtml(record.display_evidence)}</td>
        </tr>`;
      }).join('');
      fields.results.innerHTML = `<div class="tableWrap"><table>
        <thead><tr><th>ID / Quelle</th><th>Kategorie</th><th>Anforderung</th><th>Akteur</th><th>Frist</th><th>Nachweis</th></tr></thead>
        <tbody>${rows}</tbody>
      </table></div>`;
      fields.results.querySelectorAll('tr[data-id]').forEach(row => {
        row.addEventListener('click', () => {
          state.selected = records.find(r => r.display_id === row.dataset.id);
          render();
        });
      });
    }

    function renderDetail() {
      const r = state.selected;
      if (!r) {
        fields.detail.innerHTML = '<h2>Detail</h2><p class="muted">Wähle links eine Anforderung aus.</p>';
        return;
      }
      const secondary = (r.secondary_categories || []).join('; ');
      const relations = (r.relations || []).slice(0, 5).map(rel =>
        `<li>${escapeHtml(rel.other_requirement_id)}: ${escapeHtml(rel.relation_type)}</li>`
      ).join('');
      fields.detail.innerHTML = `
        <h2>${escapeHtml(r.display_id)}</h2>
        <span class="chip">${escapeHtml(r.display_category || 'ohne Kategorie')}</span>
        <div class="detailBlock"><h3>${r.record_type === 'data_collection' ? 'Datenerhebung' : 'Anforderung'}</h3><p>${escapeHtml(r.display_title)}</p></div>
        ${r.record_type === 'data_collection' ? `
        <div class="detailBlock"><h3>Beschreibung</h3><p>${escapeHtml(r.description || '-')}</p></div>
        <div class="detailBlock"><h3>Sender / Empfänger</h3><p>${escapeHtml(r.data_sender || '-')} -> ${escapeHtml(r.data_receiver || '-')}</p></div>
        <div class="detailBlock"><h3>Format / Frequenz</h3><p>${escapeHtml(r.format || '-')}<br>${escapeHtml(r.frequency || '-')}</p></div>
        <div class="detailBlock"><h3>Übermittlung</h3><p>${escapeHtml(r.transmission_method || '-')}<br>${escapeHtml((r.transmission_urls || []).join('; ') || '-')}</p></div>
        <div class="detailBlock"><h3>Grundlagendokument</h3><p>${escapeHtml(r.foundation_document_title || '-')}</p></div>
        ` : `
        <div class="detailBlock"><h3>Quelle</h3><p>${escapeHtml(r.source_title || r.source_document_id)}<br>${escapeHtml(r.source_reference)}${r.source_url ? `<br><a href="${escapeHtml(r.source_url)}" target="_blank" rel="noreferrer">Quelle öffnen</a>` : ''}</p></div>
        <div class="detailBlock"><h3>Bedingung</h3><p>${escapeHtml(r.condition || '-')}</p></div>
        <div class="detailBlock"><h3>Akteur / Aktion / Objekt</h3><p>${escapeHtml(r.actor || '-')} / ${escapeHtml(r.action || '-')} / ${escapeHtml(r.object || '-')}</p></div>
        <div class="detailBlock"><h3>Frist und Nachweis</h3><p>${escapeHtml(r.deadline_or_frequency || '-')}<br>${escapeHtml(r.evidence_required || '-')}</p></div>
        <div class="detailBlock"><h3>Nebenkategorien</h3><p>${escapeHtml(secondary || '-')}</p></div>
        <div class="detailBlock"><h3>Relationshinweise</h3>${relations ? `<ul>${relations}</ul>` : '<p>-</p>'}</div>
        `}
      `;
    }

    function render() {
      renderStats();
      renderResults();
      renderDetail();
    }

    function exportCsv() {
      const headers = ['record_type','display_id','display_category','display_title','display_actor','display_frequency','display_evidence'];
      const lines = [headers.join(';')];
      for (const record of state.filtered) {
        lines.push(headers.map(h => `"${String(record[h] || '').replaceAll('"', '""')}"`).join(';'));
      }
      const blob = new Blob(['\ufeff' + lines.join('\n')], { type: 'text/csv;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'anforderungssuche_export.csv';
      a.click();
      URL.revokeObjectURL(url);
    }

    initFilters();
    ['input', 'change'].forEach(evt => {
      fields.q.addEventListener(evt, applyFilters);
      fields.category.addEventListener(evt, applyFilters);
      fields.source.addEventListener(evt, applyFilters);
      fields.type.addEventListener(evt, applyFilters);
    });
    fields.exportBtn.addEventListener('click', exportCsv);
    fields.q.value = 'Stickstoff Hektar';
    applyFilters();
  </script>
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = json.loads(SEED_JSON.read_text(encoding="utf-8"))
    data_js = "window.REQUIREMENTS_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    OUT_DATA.write_text(data_js, encoding="utf-8")
    OUT_HTML.write_text(HTML, encoding="utf-8")
    standalone = HTML.replace('<script src="requirements_data.js"></script>', f"<script>\n{data_js}</script>")
    OUT_STANDALONE_HTML.write_text(standalone, encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# Static Search Demo Report",
                "",
                f"HTML: `{OUT_HTML}`",
                f"Standalone HTML: `{OUT_STANDALONE_HTML}`",
                f"Data: `{OUT_DATA}`",
                f"Atomic requirements: {len(payload.get('atomic_requirements', []))}",
                f"Data collections: {len(payload.get('data_collections', []))}",
                f"Total searchable records: {len(payload.get('atomic_requirements', [])) + len(payload.get('data_collections', []))}",
            ]
        ),
        encoding="utf-8",
    )
    print(OUT_HTML)


if __name__ == "__main__":
    main()
