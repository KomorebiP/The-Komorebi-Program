"""Integrate a pinned, read-only OEIS transfer index into the Komorebi Sequence Library.

The indexed source is a compact *projection* of audited formula-level ledgers.
The static site never evaluates untrusted OEIS formula or program text, and
never silently promotes a finite OEIS match to an infinite sequence identity.
"""
from __future__ import annotations
from collections import Counter
import hashlib
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote

ID = re.compile(r'^A\d{6}$')
LOCAL = re.compile(r'^[A-Za-z][A-Za-z0-9_:-]{0,100}$')
KIND = {'hyperedge','gauge','riordan','quadratic'}
EVIDENCE = {
    'all_index_formula_identity',
    'all_index_formula_identity_on_tail',
    'conditional_exact_ogf_identity',
    'exact_quadratic_algebra',
}


def read_index(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if data.get('schema') != 1 or data.get('oeis',{}).get('license') != 'CC-BY-SA-4.0':
        raise ValueError('Unsupported transfer index or missing OEIS attribution')
    edges=data.get('edges')
    records=data.get('records')
    if not isinstance(edges,list) or not isinstance(records,list):
        raise ValueError('Invalid transfer index collections')
    counts=Counter()
    keys=set()
    ids=set()
    for row in records:
        identifier=row.get('id')
        if not isinstance(identifier,str) or not ID.fullmatch(identifier) or identifier in ids:
            raise ValueError('Duplicate or malformed OEIS record')
        if not isinstance(row.get('name'),str) or len(row['name'])>5000:
            raise ValueError('Malformed OEIS record name')
        ids.add(identifier)
    for edge in edges:
        key=edge.get('key')
        kind=edge.get('kind')
        targets=[edge.get('target'),*(edge.get('inputs') or [])]
        if not isinstance(key,str) or not (0<len(key)<160) or key in keys:
            raise ValueError('Duplicate/malformed transfer key')
        if kind not in KIND or edge.get('evidence') not in EVIDENCE:
            raise ValueError('Unsupported relation kind/evidence')
        if any(item not in ids for item in targets) or not edge.get('inputs'):
            raise ValueError('Transfer references missing from OEIS index')
        if not isinstance(edge.get('expression'),str) or len(edge['expression'])>16000:
            raise ValueError('Transfer expression too long')
        if not isinstance(edge.get('domain'),str):
            raise ValueError('Transfer domain missing')
        if kind=='gauge' and (not isinstance(edge.get('valid_from'),int) or edge['valid_from']<0):
            raise ValueError('Gauge domain invalid')
        counts[kind]+=1
        keys.add(key)
    if dict(counts)!=data.get('counts'):
        raise ValueError('Transfer count receipt differs from entries')
    return data


def read_formula_text(path, network):
    """Validate source-only OEIS text before publishing the lazy asset."""
    raw=Path(path).read_bytes()
    if len(raw)>4_000_000:
        raise ValueError('OEIS Network formula source exceeds reviewed limit')
    data=json.loads(raw)
    if (data.get('schema')!=1 or data.get('evidence')!='unreviewed_source_text'
            or data.get('license')!='CC-BY-SA-4.0'
            or data.get('snapshot_sha256')!=network['oeis']['snapshot_sha256']):
        raise ValueError('OEIS source text provenance or evidence mismatch')
    entries=data.get('entries')
    if not isinstance(entries,dict):
        raise ValueError('Invalid OEIS source-formula index')
    known={row['id'] for row in network['records']}
    if not set(entries)<=known:
        raise ValueError('OEIS source formula references outside the Network')
    lines=0
    for identifier,item in entries.items():
        if not ID.fullmatch(identifier) or item.get('source')!='https://oeis.org/'+identifier:
            raise ValueError('Invalid OEIS source formula address')
        formulas=item.get('formulas')
        if not isinstance(formulas,list) or not formulas:
            raise ValueError('Empty source formula list')
        for formula in formulas:
            if (not isinstance(formula,dict) or set(formula)!={'kind','text'}
                    or not isinstance(formula['kind'],str) or len(formula['kind'])>120
                    or not isinstance(formula['text'],str) or len(formula['text'])>5000):
                raise ValueError('Invalid OEIS source formula text')
        lines+=len(formulas)
    if data.get('counts')!={'network_ids':len(known),'ids_with_formulas':len(entries),
                            'formula_lines':lines}:
        raise ValueError('OEIS source formula count mismatch')
    return data


def build_site_assets(site, entries):
    """Copy checked release data; create only finite-label local->OEIS handoffs."""
    manifest=site.root/'manifests/sequence-transfer-network.json'
    data=read_index(manifest)
    raw=json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n'
    site.write('assets/sequence-network-data.json',raw)
    # Only the Network page requests this separate, pinned source-text asset.
    # Do not ship the 99,999-sequence SQLite database to a visitor.
    source_formulas=read_formula_text(site.root/'manifests/sequence-network-formula-text.json',data)
    site.write('assets/sequence-network-formulas.json',
               json.dumps(source_formulas,ensure_ascii=False,separators=(',',':'))+'\n')
    handoffs={}
    for entry in entries:
        identifier=entry.get('id')
        if not LOCAL.fullmatch(identifier or ''):
            raise ValueError('Malformed local entry ID in network handoff')
        if entry.get('oeis_checked'):
            hits=[dict(id=x['id'],terms=int(x['matched_terms'])) for x in entry.get('matches',[])[:8]
                  if ID.fullmatch(x.get('id','')) and int(x.get('matched_terms',0))>=8]
            if hits:handoffs[identifier]=hits
    site.write('assets/sequence-network-handoffs.json',json.dumps(dict(schema=1,
      scope='Local-to-OEIS finite-prefix candidates only, not certified infinite identities',
      matches=handoffs),ensure_ascii=False,separators=(',',':'))+'\n')
    for name in ['sequence-network.css','sequence-network-format.mjs','sequence-network-math.mjs']:
        source=site.root/'website/assets'/name
        site.write('assets/'+name,source.read_text(encoding='utf-8'))
    format_hash=hashlib.sha256((site.output/'assets/sequence-network-format.mjs').read_bytes()).hexdigest()[:12]
    script=(site.root/'website/assets/sequence-network-ui.mjs').read_text(encoding='utf-8')
    original="from './sequence-network-format.mjs'"
    if script.count(original)!=1:
        raise ValueError('Sequence Network math formatter import must appear exactly once')
    script=script.replace(original, "from './sequence-network-format.mjs?v="+format_hash+"'")
    source_hash=hashlib.sha256((site.output/'assets/sequence-network-math.mjs').read_bytes()).hexdigest()[:12]
    source_import="from './sequence-network-math.mjs'"
    if script.count(source_import)!=1:
        raise ValueError('Sequence Network source formatter import must appear exactly once')
    script=script.replace(source_import, "from './sequence-network-math.mjs?v="+source_hash+"'")
    site.write('assets/sequence-network-ui.mjs',script)
    hashes={name:hashlib.sha256((site.output/'assets'/name).read_bytes()).hexdigest()[:12]
            for name in ['sequence-network.css','sequence-network-ui.mjs']}
    return {'edge_count':len(data['edges']), 'record_count':len(data['records']),
            'handoffs':len(handoffs), 'styles':'assets/sequence-network.css?v='+hashes['sequence-network.css'],
            'script':'assets/sequence-network-ui.mjs?v='+hashes['sequence-network-ui.mjs']}


def network_section(metadata):
    """Progressively enhanced network page with complete no-script explanation."""
    return ('''<section id="sequence-network" class="sn-network" data-sequence-network>
<h2>Formula connections and transfer operators</h2>
<p>Find relationships between recorded sequences. Each card places the target to the left
of the arrow and the source sequences to the right. Mathematical notation is typeset when
available, with the exact archival expression preserved in a disclosure. Select a sequence
identifier in a result to explore its direct connections in this Network; official OEIS links
remain in the record and its provenance disclosure.</p>
<details class="sn-reader-guide"><summary>How to read these transfer records</summary>
<p>A gauge relates the ratio of two sequence formulas using a scale, an exponential factor,
and a defining function L. Supported gauges display the specialized ratio with named
sequence arguments and recorded offsets. Open Gauge parameters and normalization for the general equation and constants. Index offsets and the valid tail are essential. A Riordan record
lists transform parameters rather than a full equation. Formula equality in the archived
model does not independently establish equality of the named OEIS sequences.</p>
<p>The site-wide Math display setting lets readers switch between typeset and plain notation.
Long typeset equations can be scrolled horizontally without moving the whole page.</p>
</details>
<p><strong>New research: precision-aware transfers.</strong> Read the
<a href="collection/DIRECTIONAL_GHOSTS.html">directional ghost and Frobenius quotient generalizations</a>
for exact source-fiber counts, query-dependent reconstruction and proof boundaries.
These results describe mathematical transfer contracts; they do not add unverified
OEIS edges to the curated index.</p>
<form id="sn-form" role="search" aria-label="Search archived formula connections">
<label for="sn-query">OEIS ID, local sequence ID, formula or name</label>
<div class="sn-fields"><input id="sn-query" type="search" maxlength="200" placeholder="A000108, Catalan, KFOR..." autocomplete="off" aria-describedby="sn-search-help">
<button type="submit">Find connections</button></div>
<p id="sn-search-help" class="sn-help">An exact OEIS ID finds only direct connections as a
target or input. Use <code>text:A000108</code> to include references in sequence names and
formula text. Results are archived formula relations, not live OEIS verification.</p>
<label for="sn-filter">Relation class</label>
<select id="sn-filter"><option value="all">All formula transfers</option><option value="hyperedge">Multi-input and algebraic identities</option>
<option value="gauge">Hypergeometric gauges</option><option value="riordan">Riordan transforms</option>
<option value="quadratic">Quadratic channels</option></select></form>
<p id="sn-status" role="status" aria-live="polite">Loading the read-only transfer index...</p>
<div id="sn-handoffs" aria-live="polite"></div><ol id="sn-results" class="sn-results" aria-label="Transfer connections"></ol>
<div class="sn-more-wrap"><button type="button" id="sn-show-more" hidden>Show more connections</button></div>
<section id="sn-source-formulas" class="sn-source" hidden aria-label="OEIS source formulas">
<h3>OEIS source formulas</h3>
<p>These are archived OEIS formula fields, not independently verified sequence identities.
Recognized arithmetic may be typeset without execution. Exact original text remains available, and source programs are not loaded.</p>
<button type="button" id="sn-source-load">Load this sequence’s source formula text</button>
<div id="sn-source-options" hidden><label for="sn-source-type">Formula class</label> <select id="sn-source-type"><option value="all">All formula classes</option></select></div>
<p id="sn-source-status" role="status" aria-live="polite"></p>
<ol id="sn-source-results" class="sn-source-results"></ol>
<button type="button" id="sn-source-more" hidden>Show more formulas</button>
</section>
<details class="sn-boundary"><summary>Evidence classes, limitations, and attribution</summary>
<p><strong>Formula-level identity:</strong> an algebraic identity between extracted expressions under the recorded index domain.
<strong>Conditional OGF identity:</strong> exact formal generating-function transport assuming the source and target OGF premises.
Neither establishes an independent all-index identification of the named OEIS sequences. A local-to-OEIS comparison is a finite term match only.</p>
<p>This static interface displays source-bound transfer receipts and does not run the full Python optimizer or execute OEIS program listings.
Detailed exact computation remains in the existing <a href="sequence-library.html#library-search">Sequence Library</a> and
<a href="sequence-transfers.html#transfers">Transfer workbench</a>.</p>
<p>Reference data: <a href="https://oeis.org/">OEIS Foundation Inc.</a>,
<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.
<a href="https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/SEQUENCE_TRANSFER_NETWORK.md">Komorebi transfer index and proof boundaries</a>.
<a href="assets/sequence-network-data.json" download>Download this curated index (JSON)</a>.</p></details>
<noscript><p>Network search requires JavaScript. The curated JSON and the original
<a href="sequence-library.html">Sequence Library search</a> remain available directly.</p></noscript>
</section>''')


def local_network_link(entry, prefix=''):
    """Used by local record pages; no OEIS identity assertion is made."""
    identifier=entry.get('id','')
    if not LOCAL.fullmatch(identifier):raise ValueError('Invalid local ID')
    href=prefix+'sequence-network.html?q='+quote(identifier,safe='')+'#sequence-network'
    return '<p class="sn-entry-link"><a href="'+escape(href,quote=True)+'">Explore formula and transfer connections</a> <small>(OEIS matches are finite comparisons)</small></p>'
