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


def build_site_assets(site, entries):
    """Copy checked release data; create only finite-label local->OEIS handoffs."""
    manifest=site.root/'manifests/sequence-transfer-network.json'
    data=read_index(manifest)
    raw=json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n'
    site.write('assets/sequence-network-data.json',raw)
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
    for name in ['sequence-network.css','sequence-network-ui.mjs']:
        source=site.root/'website/assets'/name
        site.write('assets/'+name,source.read_text(encoding='utf-8'))
    hashes={name:hashlib.sha256((site.output/'assets'/name).read_bytes()).hexdigest()[:12]
            for name in ['sequence-network.css','sequence-network-ui.mjs']}
    return {'edge_count':len(data['edges']), 'record_count':len(data['records']),
            'handoffs':len(handoffs), 'styles':'assets/sequence-network.css?v='+hashes['sequence-network.css'],
            'script':'assets/sequence-network-ui.mjs?v='+hashes['sequence-network-ui.mjs']}


def network_section(metadata):
    """Progressively enhanced network page with complete no-script explanation."""
    return ('''<section id="sequence-network" class="sn-network" data-sequence-network>
<h2>Formula connections and transfer operators</h2>
<p>Search OEIS IDs or names to inspect archived formula-level identities, index shifts,
Riordan maps and quadratic channels. The main Sequence Library search, exact calculators,
and OEIS term finder remain available.</p>
<form id="sn-form" role="search"><label for="sn-query">OEIS ID, local sequence ID, formula or name</label>
<div class="sn-fields"><input id="sn-query" type="search" maxlength="200" placeholder="A000108, Catalan, KFOR..." autocomplete="off">
<button type="submit">Find connections</button></div>
<label for="sn-filter">Relation class</label>
<select id="sn-filter"><option value="all">All formula transfers</option><option value="hyperedge">Multi-input and algebraic identities</option>
<option value="gauge">Hypergeometric gauges</option><option value="riordan">Riordan transforms</option>
<option value="quadratic">Quadratic channels</option></select></form>
<p id="sn-status" role="status" aria-live="polite">Loading the read-only transfer index...</p>
<div id="sn-handoffs" aria-live="polite"></div><ol id="sn-results" class="sn-results" aria-label="Transfer connections"></ol>
<details class="sn-boundary"><summary>Evidence classes, limitations, and attribution</summary>
<p><strong>Formula-level identity:</strong> an algebraic identity between extracted expressions under the recorded index domain.
<strong>Conditional OGF identity:</strong> exact formal generating-function transport assuming the source and target OGF premises.
Neither establishes an independent all-index identification of the named OEIS sequences. A local-to-OEIS comparison is a finite term match only.</p>
<p>This static interface displays source-bound transfer receipts and does not run the full Python optimizer or execute OEIS program listings.
Detailed exact computation remains in the existing <a href="sequence-library.html#library-search">Sequence Library</a> and
<a href="sequence-transfers.html#transfers">Transfer workbench</a>.</p>
<p>Reference data: <a href="https://oeis.org/">OEIS Foundation Inc.</a>,
<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.
<a href="https://github.com/KomorebiP/The-Komorebi-Program/tree/main/research/oeis-formulas">Komorebi derivations and reproduction instructions</a>.
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
