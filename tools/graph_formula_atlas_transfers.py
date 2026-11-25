"""Author: Komorebi P. Verified graph atlas transfers and complement presentation."""
import json
import subprocess
import tempfile
from pathlib import Path

TRANSFER_PAGE = 'graph-formulas/transfers.html'
TRANSFER_JSON = 'graph-formulas/sources/core-transfer-index.json'
ADDED_FAMILIES = [
    ('nonbipartite', 'Nonbipartite connected graphs', '', 13,
     'Connected graphs containing an odd cycle, by cycle rank and leaf count.'),
    ('nonbipartite-profiles', 'Nonbipartite degree profiles', '', 62,
     'Connected graphs containing an odd cycle, with prescribed core degrees.'),
]

def subtract_residues(a, b):
    """Exact signed residue sum, with no floating-point arithmetic."""
    s = [str((int(a['s'][i]) if i < len(a['s']) else 0) -
             (int(b['s'][i]) if i < len(b['s']) else 0))
         for i in range(max(len(a['s']), len(b['s'])))]
    lanes = a['lanes'] + [
        dict(lane, c=[str(-int(v)) for v in lane['c']]) for lane in b['lanes']]
    return {'s': s, 'lanes': lanes}

def compile_transfers(root, records, evaluate):
    """Run the independent BigInt all-index verifier and transfer compiler.

    Node.js is required for the expanded reader build. The immutable source
    hashes are checked by the parent atlas loader before calling this function.
    """
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'index.json'
        script = root.resolve() / 'tools' / 'compile_graph_atlas_transfers.js'
        subprocess.run(['node', str(script), str(path)], check=True,
                       cwd=root.resolve(), capture_output=True, text=True)
        bundle = json.loads(path.read_text(encoding='utf-8'))
    report = bundle['report']
    if (report['sourceRecords'], report['sourceDistinctRationalFunctions'],
        report['nonbipartiteNonzeroModels'], report['transferIdentities']) != (288, 262, 75, 60):
        raise ValueError('Unexpected transfer inventory')
    original = {r['id']: r for r in records if 'data' in r}
    core = {r['id']: r for r in bundle['coreModels']}
    if set(original) != set(core):
        raise ValueError('Transfer core identifiers do not match atlas')
    for rid, row in original.items():
        if row['data'] != core[rid]['residue']:
            raise ValueError('Python and JavaScript residue parsers disagree: '+rid)
    new = []
    for m in bundle['nonbipartiteModels']:
        rid = m['id']
        a, b = original[m['positive']], original[m['negative']]
        data = subtract_residues(a['data'], b['data'])
        for n in (0, 1, 4, 8, 16, 32, 79):
            if evaluate(data,n) != evaluate(a['data'],n)-evaluate(b['data'],n):
                raise ValueError('Signed residue mismatch: '+rid)
        factors = ''.join(r'\Phi_{'+str(d)+'}(x)'+
                          ('^{'+str(e)+'}' if e != 1 else '')
                          for d,e in m['cyclotomicFactors']) or '1'
        numerator = m['numerator']
        body = (
            'Exact difference of the connected and bipartite counts. '
            'The count is indexed by vertex number n, starting at zero. '
            'The source combinatorial identifications retain their archived evidence scope.\n\n'
            '$$F(x)=\\frac{x^{'+str(m['numeratorShift'])+'}R(x)}{Q(x)}$$\n\n'
            '$$Q(x)='+factors+'$$\n\n'
            'Numerator coefficients of R(x), in ascending order (including internal zeros):\n\n'
            +chr(96)+', '.join(numerator)+chr(96)+'\n\n'
            'Minimal eventual recurrence order: '+str(m['minimalEventualOrder'])+
            '. Least eventual quasipolynomial period: '+m['leastEventualPeriod']+'.\n\n'
            'Exact coefficient transfer: $a(n)=a_{\\rm all}(n)-a_{\\rm bip}(n)$.'
        )
        new.append(dict(id=rid,title=m['title'],
                        family='nonbipartite' if rid.startswith('NG') else 'nonbipartite-profiles',
                        body=body,oeis=[],meta='Derived exact rational complement; no new OEIS binding.',
                        data=data,
                        lanes='The exact residue formula is the positive source residue expansion minus the negative source expansion. Both source records are linked on the transfer page. The signed coefficients are available in machine-readable form by subtracting the two source models in the transfer index.',
                        parents=[m['positive'],m['negative']]))
    for slug,_,_,expected,_ in ADDED_FAMILIES:
        if sum(r['family']==slug for r in new)!=expected:
            raise ValueError('Unexpected complement family size: '+slug)
    return bundle, new
