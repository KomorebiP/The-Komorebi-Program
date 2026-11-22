"""Sequence transfer graph and exact Fibonacci-resolvent construction.

Author: Komorebi P.

Goals: maximize captured representations and candidate relationships first,
retain mathematical offsets, and never equate a finite agreement with a proof.
The verified algebraic operator schemas are separate from user-supplied OEIS
formula text and from unclassified OEIS cross-reference mentions.

Python 3.10+, standard library only. No arbitrary formula evaluation.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import chain
import json
import math
from pathlib import Path
import re
import sqlite3

OEIS_ID = re.compile(r"\bA\d{6}\b")
FORMULA = re.compile(r"^%([A-Za-z])\s+(A\d{6})\s*(.*)$")


def exact_series_mul(a, b, length):
    """Truncated multiplication in Q[[x]]."""
    out = [Q(0)] * length
    for i, ai in enumerate(a[:length]):
        if ai:
            for j, bj in enumerate(b[: length-i]):
                out[i+j] += ai * bj
    return out


def exact_series_quotient(numerator, denominator, length):
    """Independent coefficient-recurrence reference for N/D."""
    if length < 0 or not denominator or not denominator[0]:
        raise ValueError("denominator must have nonzero constant term")
    answer = [Q(0)] * length
    d0 = Q(denominator[0])
    for n in range(length):
        answer[n] = (Q(numerator[n]) if n < len(numerator) else Q(0))
        answer[n] -= sum(Q(denominator[k]) * answer[n-k]
                         for k in range(1, min(n+1, len(denominator))))
        answer[n] /= d0
    return answer


def sqrt_one(series, length):
    """Unique formal square root with constant term +1 (char != 2)."""
    if length < 0 or not series or series[0] != 1:
        raise ValueError("formal sqrt requires constant term 1")
    root = [Q(1)] + [Q(0)] * (length-1)
    for n in range(1, length):
        coefficient = Q(series[n]) if n < len(series) else Q(0)
        coefficient -= sum(root[k] * root[n-k] for k in range(1,n))
        root[n] = coefficient / 2
    return root


def fib_resolvent(numerator, denominator, length):
    """N/D = N sum_{k>=0} F_{k+1} phi^k, phi=(sqrt(5-4D)-1)/2.

    Requires D(0)=1 and Q-valued formal power series. Because phi(0)=0,
    truncating to k<length is exact modulo x**length.
    Returns the coefficients together with the compositional substitution.
    """
    if length < 1 or not denominator or Q(denominator[0]) != 1:
        raise ValueError("require positive length and D(0)=1")
    ds = [Q(denominator[i]) if i < len(denominator) else Q(0)
          for i in range(length)]
    root_argument = [Q(5 if i == 0 else 0) - 4 * ds[i]
                     for i in range(length)]
    root = sqrt_one(root_argument,length)
    phi = [(root[i] - (1 if i == 0 else 0))/2 for i in range(length)]
    gf = [Q(0)] * length
    power = [Q(1)] + [Q(0)] * (length-1)
    f0, f1 = 0,1
    for _ in range(length):
        # F_{k+1} for k = 0,1,...
        f0,f1 = f1, f0+f1
        for j in range(length):
            gf[j] += f0 * power[j]
        power = exact_series_mul(power,phi,length)
    n = [Q(numerator[i]) if i < len(numerator) else Q(0)
         for i in range(length)]
    return exact_series_mul(n,gf,length), phi


def euler_via_fibonacci(length):
    """Exact Euler zigzag E_n using only Fibonacci numbers and sin/cos."""
    numerator = [Q(0)]*length
    denominator = [Q(0)]*length
    numerator[0] = denominator[0] = Q(1)
    for n in range(1,length):
        if n%2:
            numerator[n] = Q((-1)**((n-1)//2),math.factorial(n))
        else:
            denominator[n] = Q((-1)**(n//2),math.factorial(n))
    terms,phi = fib_resolvent(numerator,denominator,length)
    return [t*math.factorial(n) for n,t in enumerate(terms)], phi


def _terms(db, key):
    row=db.execute('SELECT offset,terms_json FROM sequences WHERE oeis_id=?',(key,)).fetchone()
    return (row[0],list(map(int,json.loads(row[1])))) if row else None


def _edge_id(src,dst,operator,parameters):
    obj=json.dumps([src,dst,operator,parameters],sort_keys=True,separators=(',',':'))
    return sha256(obj.encode()).hexdigest()[:20]


# Symbolic transfer families are stored once rather than materializing
# millions of dyadic/odd-adic or polyphase parameter instances.
OPERATOR_SCHEMAS = [
    ('multi_section','P_{m,r}[a](n)=a(o+m*n+r), m>=1, 0<=r<m',
     'Exact reindexing; local n and OEIS offset o must not be conflated'),
    ('fibonacci_resolvent',
     'N(x)/D(x)=N(x)*sum_{k>=0} F_{k+1}*((sqrt(5-4*D(x))-1)/2)^k, D(0)=1',
     'Formal Q[[x]] identity; mathematically exact but not automatically faster'),
    ('ordinary_quotient','A(x)=N(x)/D(x), D(0)!=0',
     'Formal power series division; admit a cost only after benchmarking'),
    ('egf_product','a_n=sum_{k=0}^n binom(n,k)*b_k*c_{n-k}',
     'Binomial convolution induced by EGF multiplication'),
    ('ogf_product','a_n=sum_{k=0}^n b_k*c_{n-k}',
     'Ordinary convolution induced by OGF multiplication'),
    ('egf_composition','A(x)=B(C(x)), C(0)=0',
     'Formal EGF composition with normalization preserved'),
    ('binomial_transform','b_n=sum_{k=0}^n binom(n,k)*a_k',
     'Invertible with signs (-1)^(n-k)'),
    ('finite_difference','b_n=a_{n+1}-a_n',
     'May lose an additive constant'),
    ('parity_split','a_even(n)=a_{2n}; a_odd(n)=a_{2n+1}',
     'Dyadic decomposition, valid with index-offset mapping'),
    ('roots_of_unity','[n=j(mod m)]a_n via 1/m*sum_{h=0}^{m-1}omega^(-jh)A(omega^h*x)',
     'Field must support an m-th root of unity, or work in a suitable extension'),
]


def ensure_schema(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS oeis_xrefs(
        source_id TEXT NOT NULL,target_id TEXT NOT NULL,
        line TEXT NOT NULL,source_file TEXT NOT NULL,
        PRIMARY KEY (source_id,target_id,line));
    CREATE TABLE IF NOT EXISTS transfer_nodes(
        node_id TEXT PRIMARY KEY, type TEXT NOT NULL, label TEXT NOT NULL,
        data_json TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS transfer_edges(
        edge_id TEXT PRIMARY KEY, source_node TEXT NOT NULL,
        target_node TEXT NOT NULL, operator TEXT NOT NULL,
        status TEXT NOT NULL, statement TEXT NOT NULL,
        evidence TEXT NOT NULL, checked_terms INTEGER NOT NULL DEFAULT 0,
        complexity TEXT NOT NULL, source_url TEXT NOT NULL,
        params_json TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_transfer_source ON transfer_edges(source_node);
    CREATE INDEX IF NOT EXISTS idx_transfer_target ON transfer_edges(target_node);
    CREATE INDEX IF NOT EXISTS idx_transfer_status ON transfer_edges(status);
    ''')


def create_graph(db):
    ensure_schema(db)
    db.execute('DELETE FROM transfer_edges')
    db.execute('DELETE FROM transfer_nodes')
    for sid,name,offset in db.execute('SELECT oeis_id,name,offset FROM sequences'):
        _node(db,sid,'oeis_sequence',name,{'offset':offset})
    for identifier,expr,origin,oeis_id,verification,proof_status,kind in db.execute('''
        SELECT formula_id,expression,origin,oeis_id,verification,proof_status,kind
        FROM formulas'''):
        formula_node='FORMULA:'+identifier
        _node(db,formula_node,'formula',expr[:110],{
            'origin':origin,'kind':kind,'proof_status':proof_status,
            'verification':verification})
        if oeis_id:
            _edge(db,formula_node,oeis_id,'formula_representation',
                  'recorded_representation',expr[:150],
                  verification+': '+proof_status,0,
                  'unknown','https://oeis.org/'+oeis_id,{})
        # References inside OEIS formula text are candidate relations only.
        if origin.startswith('oeis_') and oeis_id:
            for ref in set(OEIS_ID.findall(expr)) - {oeis_id}:
                if _terms(db,ref) is not None:
                    _edge(db,oeis_id,ref,'referenced_in_formula',
                          'reference_only','Source formula mentions '+ref,
                          'Lexical mention, no relationship proven',0,'unknown',
                          'https://oeis.org/'+oeis_id,{})
    for key,statement,note in OPERATOR_SCHEMAS:
        _node(db,'OP:'+key,'operator_schema',key,
              {'statement':statement,'notes':note})
    _known_examples(db)
    _materialize_staged_xrefs(db)
    db.commit()
    return graph_stats(db)


def _node(db,key,kind,label,extra):
    db.execute('INSERT OR REPLACE INTO transfer_nodes VALUES (?,?,?,?)',
               (key,kind,label,json.dumps(extra,ensure_ascii=False,sort_keys=True)))


def _edge(db,src,dst,operator,status,statement,evidence,checked,cost,url,parameters):
    db.execute('''INSERT OR REPLACE INTO transfer_edges
      VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
      (_edge_id(src,dst,operator,parameters),src,dst,operator,status,statement,
       evidence,checked,cost,url,json.dumps(parameters,sort_keys=True)))


def _known_examples(db):
    """A few independently derived graph edges; no claim of discovery priority."""
    cases = [
      ('A000045','A000032','linear_shift',
       'Lucas(n) = 2*Fibonacci(n+1)-Fibonacci(n)',
       lambda a,n: 2*a[n+1]-a[n], 'O(1) arithmetic given F_n and F_(n+1)'),
      ('A000984','A000108','exact_term_division',
       'Catalan(n) = central_binomial(n)/(n+1)',
       lambda a,n: a[n]//(n+1), 'O(1) arithmetic given binomial(2n,n)'),
      ('A000079','A000302','polyphase',
       '4^n = (2^k)|_(k=2*n)',
       lambda a,n:a[2*n], 'O(1) reindexing given source'),
      ('A000079','A000225','subtract_one',
       'Mersenne(n) = 2^n - 1',
       lambda a,n:a[n]-1, 'O(1) arithmetic'),
      ('A000217','A000124','add_one',
       'central_polygonal(n) = triangular(n) + 1',
       lambda a,n:a[n]+1, 'O(1) arithmetic'),
      ('A000290','A000330','prefix_sum',
       'square_pyramidal(n) = sum_(j=0)^n j^2',
       lambda a,n:sum(a[:n+1]), 'O(n) naive; O(1) via known polynomial'),
      ('A000111','A000364','even_subsequence',
       'secant(n) = alternating_permutations(2*n)',
       lambda a,n:a[2*n], 'O(1) reindexing given source'),
      ('A000040','A001223','adjacent_difference',
       'prime_gap(n) = prime(n+1)-prime(n), with OEIS indexing starting at 1',
       lambda a,n:a[n+1]-a[n], 'O(1) arithmetic given consecutive primes'),
      ('A000110','A000262','egf_composition',
       'EGF_sets_of_lists(x)=EGF_Bell(-log(1-x))=exp(x/(1-x))',
       None, 'unknown; composition cost depends on truncation'),
      ('A000045','A000111','fibonacci_resolvent',
       'EGF_Euler(x)=(1+sin(x))*sum_(k>=0) F_(k+1)*((sqrt(5-4*cos(x))-1)/2)^k',
       None, 'unknown; exact but may be slower than direct inversion'),
    ]
    for sid,did,kind,formula,evaluator,cost in cases:
        s=_terms(db,sid);d=_terms(db,did)
        if s is None or d is None:
            continue
        _,a=s;_,b=d
        if kind=='fibonacci_resolvent':
            values,_=euler_via_fibonacci(min(len(b),18))
            checked=min(len(values),len(b))
            assert [int(x) for x in values[:checked]]==b[:checked],kind
        elif kind=='egf_composition':
            # Bell exponential generating function A(z)=exp(exp(z)-1).
            # Compose z=-log(1-x); equivalently exp(x/(1-x)).
            # Its coefficients satisfy c_n=(sum_(j=1)^n j*c_(n-j))/n
            # when c_n=a_n/n!, n>=1. Derive from C'/C=1/(1-x)^2.
            order=min(len(b),18)
            coefficients=[Q(1)]
            for n in range(1,order):
                coefficients.append(sum(Q(j)*coefficients[n-j] for j in range(1,n+1))/n)
            values=[coefficients[n]*math.factorial(n) for n in range(order)]
            checked=min(len(values),len(b))
            assert [int(x) for x in values[:checked]]==b[:checked],kind
        else:
            checked=0
            if evaluator:
                for n in range(len(b)):
                    try:
                        result=evaluator(a,n)
                    except IndexError:
                        break
                    if result!=b[n]:
                        raise AssertionError(f'{kind}: {sid}->{did}: n={n}')
                    checked+=1
        _edge(db,sid,did,kind,'algebraic_identity',formula,
              'Elementary generating-function/recurrence identity; independently '
              'checked over stored term window, not a novelty claim',checked,
              cost, 'https://oeis.org/'+did,{})


def _materialize_staged_xrefs(db):
    for from_id,to_id,line,source_file in db.execute(
        'SELECT source_id,target_id,line,source_file FROM oeis_xrefs'):
        if _terms(db,from_id) is None or _terms(db,to_id) is None:
            continue
        _edge(db,from_id,to_id,'oeis_cross_reference','reference_only',
              line[:500], 'Unclassified OEIS %Y cross reference, not a theorem',0,
              'unknown','https://oeis.org/'+from_id,{})


def import_xrefs(db,src_root,limit=None):
    """Stage and materialize candidate-only %Y links from official .seq files.

    Cross references are durable across graph rebuilds. A reimport replaces
    only the same source's entries and no %Y link is a mathematical assertion.
    """
    ensure_schema(db)
    root=Path(src_root)
    paths=[root] if root.is_file() else root.rglob('*.seq')
    scanned=0;mentions=0;known=0
    for path in paths:
        if limit is not None and scanned>=limit:break
        raw=path.read_text('utf-8').splitlines()
        scanned+=1
        source_ids={m[2] for line in raw if (m:=FORMULA.match(line))}
        if len(source_ids)!=1:
            continue
        from_id=next(iter(source_ids))
        db.execute('DELETE FROM oeis_xrefs WHERE source_id=?',(from_id,))
        for line in raw:
            m=FORMULA.match(line)
            if not m or m[1]!='Y':continue
            for other_id in sorted(set(OEIS_ID.findall(m[3]))-{from_id}):
                mentions+=1
                db.execute('INSERT OR REPLACE INTO oeis_xrefs VALUES (?,?,?,?)',
                           (from_id,other_id,m[3][:1000],path.name))
                if _terms(db,from_id) and _terms(db,other_id):
                    known+=1
        if scanned%1000==0:db.commit()
    db.commit()
    _materialize_staged_xrefs(db)
    db.commit()
    return {'files_scanned':scanned,'mentions':mentions,
            'links_to_imported_nodes':known,
            'staged':db.execute('SELECT count(*) FROM oeis_xrefs').fetchone()[0]}


def graph_stats(db):
    count=lambda table:db.execute('SELECT count(*) FROM '+table).fetchone()[0]
    statuses=dict(db.execute('SELECT status,count(*) FROM transfer_edges GROUP BY status'))
    return {'nodes':count('transfer_nodes'),'edges':count('transfer_edges'),
            'statuses':statuses,'schemata':len(OPERATOR_SCHEMAS)}


def path_query(db,src,dst,allow_references=False):
    """Shortest *structural* route; it is not a computational cost optimum."""
    from collections import deque
    if not src or not dst or src==dst:return []
    edges=defaultdict(list)
    for origin,target,op,status,statement in db.execute('''
       SELECT source_node,target_node,operator,status,statement FROM transfer_edges
       WHERE status='algebraic_identity' OR
             (? AND status='reference_only')''',(int(allow_references),)):
        edges[origin].append((target,op,status,statement))
    queue=deque([(src,[])])
    seen={src}
    while queue:
        node,path=queue.popleft()
        for target,operator,status,statement in edges[node]:
            if target in seen:continue
            nxt=path+[{'source':node,'target':target,'operator':operator,
                       'status':status,'statement':statement}]
            if target==dst:return nxt
            seen.add(target);queue.append((target,nxt))
    return None


def export(db,path):
    output=Path(path);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',encoding='utf-8',newline='\n') as fh:
        for key,typ,label,info in db.execute('SELECT * FROM transfer_nodes ORDER BY node_id'):
            fh.write(json.dumps({'type':'node','id':key,'node_type':typ,
                     'label':label,'data':json.loads(info)},ensure_ascii=False)+'\n')
        for eid,src,dst,op,status,statement,evidence,checked,complexity,url,params in db.execute(
                'SELECT * FROM transfer_edges ORDER BY source_node,target_node'):
            fh.write(json.dumps({'type':'edge','id':eid,'source':src,'target':dst,
                'operator':op,'status':status,'statement':statement,
                'evidence':evidence,'checked_terms':checked,'complexity':complexity,
                'source_url':url,'parameters':json.loads(params)},ensure_ascii=False)+'\n')
    return {'path':str(output),**graph_stats(db)}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',required=True,type=Path)
    subs=parser.add_subparsers(dest='cmd',required=True)
    b=subs.add_parser('build');b.add_argument('--export',type=Path)
    x=subs.add_parser('xrefs');x.add_argument('--seq-root',type=Path,required=True);x.add_argument('--limit',type=int)
    q=subs.add_parser('path');q.add_argument('--from-id',required=True);q.add_argument('--to-id',required=True)
    q.add_argument('--include-unverified-references',action='store_true')
    subs.add_parser('stats')
    args=parser.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        if args.cmd=='build':
            output=create_graph(db)
            if args.export:output=export(db,args.export)
        elif args.cmd=='xrefs':output=import_xrefs(db,args.seq_root,args.limit)
        elif args.cmd=='path':
            output=path_query(db,args.from_id,args.to_id,args.include_unverified_references)
        else:output=graph_stats(db)
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
