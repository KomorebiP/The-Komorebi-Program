"""Author: Komorebi P. Source-preserving graph and array formula atlas."""
import argparse
import hashlib
import html
import json
import math
import posixpath
import re
import shutil
from fractions import Fraction
from pathlib import Path

SOURCE = 'research/graph-formula-atlas'
HUB = 'graph-formulas.html'
FAMILIES = [
    ('connected', 'Connected graphs', 'Connected graphs', 17, 'Fixed cycle rank and leaf count.'),
    ('bipartite', 'Bipartite graphs', 'Bipartite connected graphs', 17, 'Connected bipartite graphs with fixed topology parameters.'),
    ('degree-profiles', 'Graph degree profiles', 'Connected graphs: degree profiles', 69, 'Fixed core degree distributions.'),
    ('bipartite-profiles', 'Bipartite degree profiles', 'Bipartite graphs: degree profiles', 69, 'Degree profiles with bipartite subdivision constraints.'),
    ('unicyclic', 'Unicyclic graphs', 'Unicyclic graphs: independent construction', 24, 'One cycle, fixed leaf count; independent dihedral construction.'),
    ('rooted', 'Rooted trees', 'Rooted trees: fixed leaf counts', 24, 'Unlabeled nonplane rooted trees with fixed leaf count.'),
    ('unrooted', 'Unrooted trees', 'Unrooted trees: fixed leaf counts', 23, 'Unlabeled trees with fixed leaf count.'),
    ('branching', 'Rooted branching profiles', 'Rooted trees: branching profiles', 45, 'Prescribed numbers of vertices of each branching degree.'),
    ('parity-arrays', 'Parity-decomposed arrays', 'Reduced parity formula', 27, 'Independent residue classes and reduced graph or binomial factors.'),
    ('boundary-arrays', 'Boundary-factorized arrays', 'Boundary factorization', 15, 'Boundary factors and independent-set interiors.'),
    ('binomial-arrays', 'Binomial array formulas', 'Elementary binomial formula', 9, 'Monotone configurations counted by binomial coefficients.'),
    ('finite-state-arrays', 'Finite-state arrays', 'Finite-state transfer', 99, 'Forbidden words and sliding-window constraints.'),
    ('block-arrays', 'Local block constraints', 'Block transfer', 18, 'Binary and nonbinary arrays constrained by 2×2 blocks.'),
    ('walks', 'Graph walks', '5. All four direct graph walks', 4, 'Path, cycle and complete-graph walk sequences.'),
    ('labeled', 'Connected labeled graphs', '6. Connected labeled graphs with edge parity', 2, 'Even and odd edge counts via formal exponential generating functions.'),
]
SOURCES = ('Graph_288_Formulas.md', 'Graph_288_Binomial_Lanes.md', 'OEIS_168_Array_Formulas.md', 'OEIS_64_Graph_Formulas.md', 'V30_THEOREMS.md', 'V31_THEOREMS.md', 'V32_THEOREMS.md')
SOURCE_SHA256 = (
    '493bd4289f29fe98195406669327bbfba3f9cbc1786f908cb31571edf40fa544',
    'dce80f74aded1285d8edbac4b7f22e64fe4d22ff4127e3353b360e22d7920435',
    '3663db595d4f90bedf409ab38f1c899d891ee48350e5a822f4a13ca2e14b1a2b',
    '480677a1ba19ca68d174d7c69e227bbbe59695da0b046ba82a959df9e0b2ca4c',
    'a98c3ba2ef596439e2322f492cf3cfc0b2a7457f9e904a7487db1fc45798a100',
    '555c0c4ffe671e05c20266b16203bfb1885236f08fafa4121d9b72037e210545',
    'a6b4de8fd4d801b7a72bbfdefd2b85d22107a4abcdabf1e5129dd2857f62c20d',
)
WALK_TITLES = {'A094233':'Nine-cycle closed walks','A005023':'Eight-vertex path walks','A095933':'Ten-cycle antipodal walk formula','A226493':'Complete graph K4, total closed walks','A054939':'Connected labeled graphs, even edge count','A054940':'Connected labeled graphs, odd edge count'}

def esc(s):
    return html.escape(str(s), quote=True)

def split_sections(text):
    h = list(re.finditer(r'^## (.+)$', text, re.M))
    return {m[1]: text[m.end():h[i+1].start() if i+1 < len(h) else len(text)].strip() for i,m in enumerate(h)}

def split_records(text):
    h = list(re.finditer(r'^### ([A-Z]+\d+)(?:[ \t]+(?:—[ \t]+(.*)|\*))?[ \t]*$',text,re.M))
    return [(m[1],m[2] or '',text[m.end():h[i+1].start() if i+1<len(h) else len(text)].strip()) for i,m in enumerate(h)]

def lane_data(text):
    finite = re.search(r'Finite polynomial part S \(ascending\): `([^`]+)`',text)
    if not finite:
        raise ValueError('Missing finite polynomial part')
    data = {'s':[str(int(c)) for c in finite[1].split(',')], 'lanes':[]}
    for m in re.finditer(r'\*\*d=(\d+), e=(\d+), h=(\d+)\*\*\s*```text\n(.*?)\n```',text,re.S):
        d,e,h = map(int,m.groups()[:3]); c=[]
        for line in m[4].splitlines():
            block = re.fullmatch(r'\s*(\d+)-(\d+)\s+(.+)',line)
            if not block or int(block[1]) != len(c):
                raise ValueError('Invalid coefficient block')
            vals = [str(int(x)) for x in block[3].split(',')]
            if int(block[2]) != len(c)+len(vals)-1:
                raise ValueError('Coefficient block length')
            c.extend(vals)
        if not d or not e or not h or len(c)>d*e:
            raise ValueError('Invalid residue lane')
        data['lanes'].append({'d':d,'e':e,'h':str(h),'c':c})
    if len(data['lanes']) != len(re.findall(r'\*\*d=\d+, e=\d+, h=\d+\*\*',text)) or not data['lanes']:
        raise ValueError('Missing lanes')
    return data

def evaluate(data,n):
    val = Fraction(int(data['s'][n]) if n < len(data['s']) else 0)
    for lane in data['lanes']:
        d,e,h,c = lane['d'],lane['e'],int(lane['h']),lane['c']
        q,r = divmod(n,d)
        val += Fraction(sum(int(c[r+d*j])*math.comb(q-j+e-1,e-1) for j in range(min(q,e-1)+1) if r+d*j<len(c)),h)
    if val.denominator != 1 or val < 0:
        raise ValueError('Nonintegral or negative count')
    return val.numerator

def array_title(rid,meta,body):
    n=int(rid[1:]); shape=meta.split(';')[0]
    known=[(202092,202100,'001 / 011, rows and columns'),(202194,202202,'001 / 101, rows and columns'),(202398,202406,'000 / 010, rows and columns'),(202427,202435,'000 / 001, rows, columns and NW–SE diagonals'),(202484,202492,'000 / 010, rows, columns and NW–SE diagonals'),(202594,202601,'000 / 001, rows and columns'),(184200,184207,'Binary 2×2 sums at least 2'),(184208,184217,'Quaternary 2×2 sums at least 7')]
    for lo,hi,label in known:
        if lo<=n<=hi:return label+' · '+shape
    p=re.search(r'\^\{\(([01]);([01,]+)\)\}',body)
    if p:return 'Forbid '+p[2].replace(',',' / ')+(', rows, columns and NW–SE diagonals' if p[1]=='1' else ', rows and columns')+' · '+shape
    p=re.search(r'\\mathcal C_\{[^,]+,(\d+),(\d+)\}',body)
    if p:return 'At most '+p[2]+' ones per '+p[1]+' cells · '+shape
    return meta

def load(root):
    raw={}
    for name,digest in zip(SOURCES,SOURCE_SHA256):
        payload=(root/SOURCE/name).read_bytes()
        if hashlib.sha256(payload).hexdigest()!=digest:raise ValueError('Source checksum mismatch: '+name)
        raw[name]=payload.decode('utf-8')
    graph=split_sections(raw[SOURCES[0]])
    lanes=split_sections(raw[SOURCES[1]])
    arr=split_sections(raw[SOURCES[2]])
    supplement=split_sections(raw[SOURCES[3]])
    arrays=split_records(raw[SOURCES[2]].split('## Appendix:',1)[0])
    records=[]; counts={}
    for i,(slug,title,source,count,description) in enumerate(FAMILIES):
        if i<8:
            lmap={r[0]:r[2] for r in split_records(lanes[source])}
            items=split_records(graph[source])
            if set(lmap)!={r[0] for r in items}:
                raise ValueError('Lane identifiers do not match rational models')
        elif i<13:
            items=[r for r in arrays if r[2].splitlines()[0].split(';')[-1].strip().rstrip('.')==source]
        else:
            items=split_records(supplement[source])
        if len(items)!=count:
            raise ValueError(f'{slug}: expected {count} entries, got {len(items)}')
        counts[slug]=len(items)
        for rid,label,body in items:
            ids=sorted(set(re.findall(r'\bA\d{6}\b',rid+' '+label)))
            meta=body.splitlines()[0] if i<13 else 'Inherited OEIS model; finite source checks.'
            title=label if i<8 else (array_title(rid,meta,body) if i<13 else WALK_TITLES[rid])
            row=dict(id=rid,title=title,family=slug,body=body,oeis=ids,meta=meta)
            if i<8:
                row['lanes']=lmap[rid]; row['data']=lane_data(lmap[rid])
                for n in (0,1,4,8,16):evaluate(row['data'],n)
            records.append(row)
    if len(records)!=462 or len({r['id'] for r in records})!=462 or len({a for r in records for a in r['oeis']})!=184:
        raise ValueError('Unexpected inventory size or duplicate identifier')
    return raw,graph,arr,supplement,records,counts

# Restrained renderer for the archived catalog dialect. Escapes all source text;
# math uses the reader's MathJax delimiters and code remains selectable text.
INLINE=re.compile(r'(`[^`\n]+`|\$[^$\n]+\$|\*\*[^*\n]+\*\*)')
BLOCK=re.compile(r'(^```[^\n]*\n.*?^```[ \t]*$|\$\$.*?\$\$|\\\[.*?\\\])',re.M|re.S)

def inline(text):
    out=[]
    for i,s in enumerate(INLINE.split(text)):
        if i%2==0:out.append(esc(s))
        elif s.startswith('`'):out.append('<code>'+esc(s[1:-1])+'</code>')
        elif s.startswith('$'):out.append('<span class="arithmatex">\\('+esc(s[1:-1])+'\\)</span>')
        else:out.append('<strong>'+esc(s[2:-2])+'</strong>')
    return ''.join(out)

def render(text):
    out=[]
    for i,s in enumerate(BLOCK.split(text)):
        if i%2:
            if s.startswith('```'):
                out.append('<pre class="gfa-coeff">'+esc(s.split('\n',1)[1].rsplit('\n',1)[0])+'</pre>')
            else:
                out.append('<div class="gfa-equation arithmatex">\\['+esc(s[2:-2])+'\\]</div>')
            continue
        for p in re.split(r'\n\s*\n',s.strip()):
            if not p:continue
            lines=p.splitlines()
            if all(line.startswith('- ') or line.startswith('* ') for line in lines):
                out.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in lines)+'</ul>')
            elif lines[0].startswith('### '):
                out.append('<h3>'+inline(lines[0][4:])+'</h3>')
                if len(lines)>1:out.append('<p>'+inline(' '.join(lines[1:]))+'</p>')
            else:out.append('<p>'+inline(' '.join(lines))+'</p>')
    return ''.join(out)

def family_url(slug):return 'graph-formulas/'+slug+'.html'

def build(site):
    raw,graph,arr,supplement,records,counts=load(site.root)
    for name,source in raw.items():site.write('graph-formulas/sources/'+name,source)
    manifest={name:hashlib.sha256(source.encode()).hexdigest() for name,source in raw.items()}
    site.write('graph-formulas/sources/manifest.json',json.dumps(manifest,indent=2)+'\n')
    version=hashlib.sha256((site.root/'website/assets/graph-formula-atlas.js').read_bytes()).hexdigest()[:12]
    cssver=hashlib.sha256((site.root/'website/assets/graph-formula-atlas.css').read_bytes()).hexdigest()[:12]
    def shell(page,title,content):
        asset=lambda name:site.rel('assets/'+name,page)
        site.page(page,title,'<link rel="stylesheet" href="'+asset('graph-formula-atlas.css')+'?v='+cssver+'"><div class="gfa">'+content+'</div><script defer src="'+asset('graph-formula-atlas.js')+'?v='+version+'"></script>')
    def nav(page):
        return '<nav class="gfa-nav" aria-label="Formula atlas navigation"><a href="'+site.rel(HUB,page)+'">Formula atlas</a><a href="'+site.rel('graph-formulas/definitions.html',page)+'">Definitions and sources</a><a href="'+site.rel('sequence-library.html',page)+'">Sequence Library</a></nav>'
    cards=''.join('<a class="gfa-family" href="'+family_url(slug)+'"><span class="gfa-count">'+str(count)+' records</span><h3>'+esc(title)+'</h3><p>'+esc(desc)+'</p></a>' for slug,title,source,count,desc in FAMILIES)
    opts=''.join('<option value="'+slug+'">'+esc(title)+' ('+str(count)+')</option>' for slug,title,_,count,_ in FAMILIES)
    names={f[0]:f[1] for f in FAMILIES}
    index=[]
    for row in records:
        rid=row['id']; slug=row['family']; title=row['title']; oeis=' '.join(row['oeis'])
        search=' '.join((rid,title,oeis,names[slug],row['meta'],row['body'][:500] if 'data' not in row else ''))
        index.append('<li data-gfa-record data-family="'+slug+'" data-oeis="'+('yes' if oeis else 'no')+'" data-search="'+esc(search.lower())+'"><a href="'+family_url(slug)+'#'+rid+'"><strong>'+esc(rid)+'</strong> '+esc(title)+'</a><small>'+esc(names[slug]+(' · '+oeis if oeis and rid not in row['oeis'] else ''))+'</small></li>')
    hero='<header class="gfa-hero"><p class="gfa-kicker">Komorebi / Realization Calculus</p><h1>Graph &amp; array formula atlas</h1><p>Browse exact graph, tree and constrained-array formulas by mathematical family. Read the underlying constructions, inspect every coefficient, and evaluate the structural-core models with exact integer arithmetic.</p><div class="gfa-stats"><div><strong>462</strong><span>formula records</span></div><div><strong>15</strong><span>family groups</span></div><div><strong>184</strong><span>distinct OEIS IDs</span></div><div><strong>262</strong><span>distinct core rational functions</span></div></div></header>'
    search='<section id="formula-index"><h2>Find an individual formula</h2><form class="gfa-controls" id="gfa-search" hidden><label>Search identifier, pattern or description<input type="search" id="gfa-query" placeholder="A202485, g=2, 000, leaves"></label><label>Family<select id="gfa-family"><option value="">All families</option>'+opts+'</select></label><label>OEIS binding<select id="gfa-bound"><option value="">All records</option><option value="yes">OEIS-linked</option><option value="no">Unbound research models</option></select></label><button type="reset">Clear</button></form><p id="gfa-status" role="status" aria-live="polite">462 records. Enable JavaScript to search and paginate.</p><ul class="gfa-index" id="gfa-results">'+''.join(index)+'</ul><div class="gfa-pagination" id="gfa-pagination" hidden><button type="button" id="gfa-prev">Previous</button><span id="gfa-page"></span><button type="button" id="gfa-next">Next</button></div></section>'
    shell(HUB,'Graph and array formula atlas',hero+nav(HUB)+'<p class="gfa-note">Scope: 288 v31–v32 structural-core records (262 distinct rational functions), 168 constrained-array entries, and six other OEIS graph formulas. The 64-entry graph supplement overlaps these collections; ten tree bindings appear under Rooted trees. These are retained models and finite OEIS identifications, not 462 new OEIS admissions.</p><p><a href="#formula-index">Find a formula</a> · <a href="graph-formulas/definitions.html#sources">Proofs and source downloads</a></p><section><h2>Browse by mathematical family</h2><div class="gfa-families">'+cards+'</div></section>'+search)
    for slug,title,source,count,desc in FAMILIES:
        page=family_url(slug); body=[]
        for row in [r for r in records if r['family']==slug]:
            rid=row['id']; links=' '.join('<a href="https://oeis.org/'+a+'">'+a+'</a>' for a in row['oeis'])
            heading='<strong>'+rid+'</strong> <span>'+esc(row['title'])+'</span>'
            extra=''
            if 'data' in row:
                model=json.dumps(row['data'],separators=(',',':'))
                extra='<form class="gfa-eval" data-model="'+esc(model)+'" hidden><label>Vertex count n<input type="number" min="0" max="10000" step="1" value="8" required></label><button type="submit">Evaluate exactly</button><output aria-live="polite"></output></form><details class="gfa-lanes"><summary>Complete binomial-residue expansion</summary>'+render(row['lanes'])+'</details>'
            body.append('<details class="gfa-record" id="'+rid+'"><summary>'+heading+'</summary><div class="gfa-record-body">'+('<p class="gfa-oeis">OEIS reference: '+links+'. Identification retains finite-check evidence.</p>' if links else '<p class="gfa-note">Research model; no OEIS identifier assigned in the retained source.</p>')+render(row['body'])+extra+'<p><a href="'+site.rel('graph-formulas/definitions.html',page)+'">Notation, evaluation formulas and proof sources</a></p></div></details>')
        prefix=''
        if slug in ('walks','labeled'):
            prefix=render(supplement[source].split('### ',1)[0])
        if slug in ('parity-arrays','boundary-arrays','binomial-arrays','finite-state-arrays','block-arrays'):
            prefix='<p>Index n starts at 1. Square and flattened-table models have variable width. See the <a href="definitions.html#array-definitions">array matrix definitions</a> before evaluating a formula.</p>'
        shell(page,title,'<header class="gfa-hero"><p class="gfa-kicker">Formula atlas / '+esc(str(count))+' records</p><h1>'+esc(title)+'</h1><p>'+esc(desc)+'</p></header>'+nav(page)+prefix+'<section aria-label="Individual formulas">'+''.join(body)+'</section>')
        site.search.append(dict(title=title+' — formula atlas',group='Collection',kind='Examples',url=page,text=desc+' '+' '.join(r['id']+' '+r['title'] for r in records if r['family']==slug),work_ids=[]))
    page='graph-formulas/definitions.html'
    downloads=''.join('<li><a download href="sources/'+name+'">'+esc(name)+'</a></li>' for name in SOURCES)
    shell(page,'Formula definitions and source collection','<header class="gfa-hero"><h1>Definitions, proofs and exact source data</h1><p>Author: Komorebi P. Written proofs and exact computational checks retain their original evidence scope.</p></header>'+nav(page)+'<section><h2>Structural-core formula conventions</h2>'+render(graph['Common explicit a(n) formula'])+'<h3>Explicit cyclotomic factors</h3>'+render(graph['Explicit cyclotomic factors'])+'<h3>Binomial-residue evaluation</h3>'+render(raw[SOURCES[1]].split('## Connected graphs',1)[0].split('\n\n',1)[1])+'</section><section id="array-definitions"><h2>Array definitions and matrices</h2>'+render(arr['Definitions'].split('### A184200',1)[0])+'<h3>Explicit strip polynomials</h3>'+render(arr['Appendix: explicit strip polynomials'])+'</section><section id="sources"><h2>Sources and evidence</h2><p>Original definitions and reference terms are credited to the OEIS Foundation Inc., <a href="https://oeis.org/">OEIS</a>, CC BY-SA 4.0. Written arguments are not Lean verification or a literature-priority claim. No full-corpus scan is implied.</p><ul>'+downloads+'</ul><p><a href="sources/manifest.json">SHA-256 source manifest</a></p><p><a href="../collection/PARITY_ARRAY_TRANSFER.html">Parity array proof</a> · <a href="../collection/LATTICE_POLYPHASE_GRAPH.html">Lattice and spectral generalization</a></p></section>')
    site.search.append(dict(title='Graph and array formula atlas',group='Collection',kind='Examples',url=HUB,text='462 graph tree array formulas, cycle rank, leaves, forbidden patterns, OEIS, structural cores and exact recurrence data',work_ids=[]))
    return {'formula_records':len(records),'families':len(FAMILIES),'oeis_ids':184,'core_models':288,'source_hashes':manifest}

class PreviewSite:
    """Local static preview without the full reader shell or MathJax runtime."""
    def __init__(self,root,output):self.root=root;self.output=output;self.search=[]
    def rel(self,target,page):return posixpath.relpath(target,posixpath.dirname(page) or '.')
    def write(self,path,text):
        f=self.output/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text,encoding='utf-8')
    def page(self,path,title,body):
        self.write(path,'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+esc(title)+'</title></head><body style="margin:0;background:#faf9f6;color:#242c2a;font:16px/1.6 system-ui,sans-serif"><main style="max-width:1100px;margin:auto;padding:16px">'+body+'</main></body></html>')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--preview',type=Path,required=True);args=p.parse_args();args.preview.mkdir(parents=True,exist_ok=True)
    assets=args.preview/'assets';assets.mkdir(exist_ok=True)
    for n in ('graph-formula-atlas.css','graph-formula-atlas.js'):shutil.copyfile(args.root/'website/assets'/n,assets/n)
    print(json.dumps(build(PreviewSite(args.root,args.preview)),indent=2))
