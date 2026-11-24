"""Exact-prefix transfer discovery and rational-ratio/Pochhammer candidates.

Author: Komorebi P.

All discoveries in this module are *finite candidates*, never global theorems.
Only existing, explicitly certified identities from sequence_transfer_graph may be
used as proof edges. Inputs use local positions starting at mathematical OEIS
offsets, which are included in every candidate's parameters and statement.

Uses integer and Fraction arithmetic only; does not execute OEIS formula text.
Python >=3.10, standard library.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
import sqlite3
from pathlib import Path


def identity(*parts):
    return hashlib.sha256(json.dumps(parts, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()[:24]


def load_sequences(db, *, include_local=False):
    """Use true offsets, and do not silently align distinct OEIS index ranges."""
    result={}
    for sid,offset,terms in db.execute('SELECT oeis_id,offset,terms_json FROM sequences ORDER BY oeis_id'):
        result[sid]=(int(offset), tuple(int(x) for x in json.loads(terms)))
    if include_local:
        for sid,offset,terms in db.execute('SELECT local_id,offset,terms_json FROM komorebi_records ORDER BY local_id'):
            if sid in result:raise ValueError('Komorebi ID collision: '+sid)
            result[sid]=(int(offset), tuple(int(x) for x in json.loads(terms)))
    return result


def ensure_miner_schema(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS transfer_candidates (
        candidate_id TEXT PRIMARY KEY,
        output_id TEXT NOT NULL,
        inputs_json TEXT NOT NULL,
        operator TEXT NOT NULL,
        parameters_json TEXT NOT NULL,
        checked_terms INTEGER NOT NULL,
        discovery_terms INTEGER NOT NULL,
        holdout_terms INTEGER NOT NULL,
        statement TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status='finite_candidate'),
        source TEXT NOT NULL,
        source_hashes_json TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_mined_output ON transfer_candidates(output_id);
    CREATE INDEX IF NOT EXISTS idx_mined_operator ON transfer_candidates(operator);
    CREATE TABLE IF NOT EXISTS rational_ratio_candidates (
        oeis_id TEXT PRIMARY KEY,
        local_start INTEGER NOT NULL,
        mathematical_start INTEGER NOT NULL,
        base_value TEXT NOT NULL,
        numerator_json TEXT NOT NULL,
        denominator_json TEXT NOT NULL,
        pochhammer_json TEXT,
        fitted_ratios INTEGER NOT NULL,
        holdout_ratios INTEGER NOT NULL,
        checked_ratios INTEGER NOT NULL,
        status TEXT NOT NULL CHECK(status='finite_candidate'),
        source_hash TEXT NOT NULL
    );
    ''')


def _hash_terms(offset,terms):
    return identity(offset,terms)


def _well_informed(values, *, minimum_distinct=5):
    """Prune constant and zero-heavy collisions, never use as proof strength."""
    return len(values)>=10 and len(set(values))>=minimum_distinct


def _match_target(target, generated, minimum):
    k=min(len(target),len(generated))
    if k<minimum or not _well_informed(target[:k]):return 0
    for i in range(k):
        if target[i]!=generated[i]:return 0
    return k


def _integer_candidates(data, min_terms, max_modulus, include_pairs):
    """Yield (output,inputs,operator,parameters,checked). Prefixes indexed first.

    Indexing first means complexity is chiefly O(S^2*L^2), not O(S^3*L^2).
    This is intended for coarse retrieval, not an exhaustive equality solver.
    """
    source_ids=sorted(data)
    # Only sufficiently varied output prefixes are indexed. The 10-term key
    # suppresses huge accidental classes of constant/zero-prefix sequences.
    index=defaultdict(list)
    for sid in source_ids:
        _,a=data[sid]
        if len(a)>=min_terms and _well_informed(a[:min_terms]):
            index[tuple(a[:min_terms])].append(sid)

    def hits(inputs,kind,parameters,generated):
        if len(generated)<min_terms:return
        for out in index.get(tuple(generated[:min_terms]),()):
            if len(inputs)==1 and inputs[0]==out:continue
            n=_match_target(data[out][1],generated,min_terms)
            if n:
                yield (out,inputs,kind,parameters,n)

    for sid in source_ids:
        off,a=data[sid]
        n=len(a)
        if n<min_terms:continue
        # Shift is a local offset shift: b(off_b+i)=a(off_a+i+shift).
        for shift in range(1,min(6,n-min_terms+1)):
            yield from hits([sid],'shift',{'shift':shift},a[shift:])
        # Polyphase subseries: b(off_b+i)=a(off_a + m*i+r).
        for m in range(2,max_modulus+1):
            for r in range(m):
                yield from hits([sid],'polyphase',{'modulus':m,'residue':r},a[r::m])
        for d in (-3,-2,-1,1,2,3):
            yield from hits([sid],'add_constant',{'constant':d},[x+d for x in a])
        for scale in (-4,-3,-2,2,3,4):
            yield from hits([sid],'multiply_constant',{'constant':scale},[x*scale for x in a])
        yield from hits([sid],'adjacent_difference',{},[a[j+1]-a[j] for j in range(n-1)])
        yield from hits([sid],'prefix_sum',{},list(itertools.accumulate(a)))
        # Both binomial transforms use local n rather than the native offset.
        for sign,operator in [(1,'binomial_transform'),(-1,'inverse_binomial_transform')]:
            b=[sum(((-1)**(j-k) if sign<0 else 1)*math.comb(j,k)*a[k]
                   for k in range(j+1)) for j in range(n)]
            yield from hits([sid],operator,{},b)

    if not include_pairs:return
    for i,sid in enumerate(source_ids):
        _,a=data[sid]
        if len(a)<min_terms:continue
        for tid in source_ids[i:]:
            _,b=data[tid]
            length=min(len(a),len(b))
            if length<min_terms:continue
            a2=a[:length];b2=b[:length]
            pair=[sid,tid]
            # Algebraic units are schemas, not useful pairwise discoveries:
            # a*1=a, a+0=a, a*delta=a for both OGF and EGF convolution.
            is_zero=lambda x:all(v==0 for v in x)
            is_one=lambda x:all(v==1 for v in x)
            is_delta=lambda x:x[0]==1 and all(v==0 for v in x[1:])
            if not (is_one(a2) or is_one(b2)):
                yield from hits(pair,'pointwise_product',{},[a2[j]*b2[j] for j in range(length)])
            # Binary convolution is *not* a single-input graph arrow.
            if not (is_delta(a2) or is_delta(b2)):
                ogf=[sum(a2[k]*b2[j-k] for k in range(j+1)) for j in range(length)]
                yield from hits(pair,'ogf_convolution',{},ogf)
                egf=[sum(math.comb(j,k)*a2[k]*b2[j-k] for k in range(j+1))
                     for j in range(length)]
                yield from hits(pair,'egf_convolution',{},egf)
            if not (is_zero(a2) or is_zero(b2)):
                yield from hits(pair,'pointwise_sum',{},[a2[j]+b2[j] for j in range(length)])


def _candidate_statement(out,inputs,kind,params,data):
    out_offset=data[out][0]
    symbols=[f'{key}[{data[key][0]}+j]' for key in inputs]
    prefix=f'{out}[{out_offset}+j] = '
    if kind=='shift':return prefix+f'{inputs[0]}[{data[inputs[0]][0]}+j+{params["shift"]}]'
    if kind=='polyphase':return prefix+f'{inputs[0]}[{data[inputs[0]][0]}+{params["modulus"]}j+{params["residue"]}]'
    if kind=='add_constant':return prefix+symbols[0]+f' + ({params["constant"]})'
    if kind=='multiply_constant':return prefix+f'{params["constant"]}*'+symbols[0]
    if kind=='adjacent_difference':return prefix+f'{inputs[0]}[{data[inputs[0]][0]}+j+1] - '+symbols[0]
    if kind=='prefix_sum':return prefix+f'sum_(k=0)^j {inputs[0]}[{data[inputs[0]][0]}+k]'
    if kind in ('binomial_transform','inverse_binomial_transform'):
        sign='' if kind=='binomial_transform' else '(-1)^(j-k)*'
        return prefix+f'sum_(k=0)^j {sign}binom(j,k)*{inputs[0]}[{data[inputs[0]][0]}+k]'
    if kind=='pointwise_product':return prefix+f'{symbols[0]} * {symbols[1]}'
    if kind=='pointwise_sum':return prefix+f'{symbols[0]} + {symbols[1]}'
    if kind in ('ogf_convolution','egf_convolution'):
        choose='binom(j,k)*' if kind=='egf_convolution' else ''
        return prefix+f'sum_(k=0)^j {choose}{inputs[0]}[{data[inputs[0]][0]}+k]*{inputs[1]}[{data[inputs[1]][0]}+j-k]'
    raise ValueError(kind)


def mine_transfers(db, *, min_terms=10, max_modulus=4, include_pairs=True,
                   include_local=False, max_sequences=10000,
                   limit=None, commit_every=1000):
    if min_terms<8:raise ValueError('at least 8 terms needed for initial screening')
    if max_modulus<2:raise ValueError('max_modulus must be >=2')
    ensure_miner_schema(db)
    data=load_sequences(db,include_local=include_local)
    if len(data)>max_sequences:
        raise ValueError('Sequence corpus exceeds configured miner limit; explicitly raise --max-sequences or run on shards')
    if include_pairs and len(data)>300:
        raise ValueError('Quadratic pair discovery disabled above 300 sequences; use --no-pairs for a large corpus')
    db.execute('DELETE FROM transfer_candidates')
    count=0
    by_kind=Counter()
    for out,inputs,kind,params,checked in _integer_candidates(
        data,min_terms,max_modulus,include_pairs):
        if checked<=min_terms:continue # require an independent check tail
        if checked>len(data[out][1]):checked=len(data[out][1])
        cid=identity(out,inputs,kind,params)
        hashes={sid:_hash_terms(*data[sid]) for sid in set(inputs+[out])}
        db.execute('''INSERT OR IGNORE INTO transfer_candidates VALUES
          (?,?,?,?,?,?,?,?,?,?,?,?)''',
          (cid,out,json.dumps(inputs),kind,json.dumps(params,sort_keys=True),
           checked,min_terms,checked-min_terms,
           _candidate_statement(out,inputs,kind,params,data),
           'finite_candidate', 'exact_integer_prefix_screen',
           json.dumps(hashes,sort_keys=True)))
        if db.execute('SELECT changes()').fetchone()[0]:
            count+=1;by_kind[kind]+=1
        if limit is not None and count>=limit:break
        if count%commit_every==0 and count:db.commit()
    db.commit()
    return {'sequences_indexed':len(data),'candidate_edges':count,
            'by_operator':dict(sorted(by_kind.items())),
            'inference':'finite candidate only; discovery-prefix+holdout exact comparisons; no universal identity claimed',
            'including_local_records':include_local,
            'neutral_laws_factored_out':['a+0=a','a*1=a','a(x)*1=a(x) under OGF/EGF convolution']}


def _solve_unique(matrix, rhs):
    """Unique rational solution using Gauss-Jordan; None for underdetermined/inconsistent."""
    if not matrix:return None
    w=len(matrix[0]);aug=[[Q(y) for y in row]+[Q(b)] for row,b in zip(matrix,rhs)]
    rank=0;pivots=[]
    for col in range(w):
        pivot=next((r for r in range(rank,len(aug)) if aug[r][col]),None)
        if pivot is None:continue
        aug[rank],aug[pivot]=aug[pivot],aug[rank]
        fac=aug[rank][col]
        aug[rank]=[x/fac for x in aug[rank]]
        for r in range(len(aug)):
            if r!=rank and aug[r][col]:
                fac=aug[r][col]
                aug[r]=[x-fac*y for x,y in zip(aug[r],aug[rank])]
        pivots.append(col);rank+=1
    if any(all(x==0 for x in row[:-1]) and row[-1]!=0 for row in aug):return None
    if rank<w:return None
    sol=[Q(0)]*w
    for r,c in enumerate(pivots):sol[c]=aug[r][-1]
    return sol


def _trim(a):
    while len(a)>1 and not a[-1]:a.pop()
    return a


def _poly(a,t):return sum(c*t**i for i,c in enumerate(a))


def _rational_square_root(x):
    if x<0:return None
    nn=math.isqrt(x.numerator);dd=math.isqrt(x.denominator)
    return Q(nn,dd) if nn*nn==x.numerator and dd*dd==x.denominator else None


def _roots(poly):
    p=_trim(list(poly))
    if len(p)==1:return []
    if len(p)==2:return [-p[0]/p[1]]
    if len(p)==3:
        c,b,a=p
        discriminant=b*b-4*a*c
        root=_rational_square_root(discriminant)
        if root is None:return None
        return [(-b+root)/(2*a),(-b-root)/(2*a)]
    return None


def _pochhammer_form(p,q):
    """Return c*(alpha)_t/(beta)_t factored over Q if possible."""
    pr,qr=_roots(p),_roots(q)
    if pr is None or qr is None:return None
    return {'multiplier':str(p[-1]/q[-1]),
            'upper':[str(-x) for x in sorted(pr)],
            'lower':[str(-x) for x in sorted(qr)],
            'form':'a(start+t)=base*c^t*prod((alpha)_t)/prod((beta)_t)',
            'definition':'(alpha)_t = prod_(k=0)^(t-1)(alpha+k)',
            'proof_status':'finite_candidate_not_globally_proved'}


def infer_ratio(terms, offset, *, max_degree=2, fitting_min=8,
                min_holdout=4, min_total_ratios=12):
    """Infer an *uncertified* rational consecutive-term ratio and Pochhammer form.

    Fit a few earliest nonzero ratios. Reserve trailing ratios as holdout.
    Recheck all observed ratios exactly. No extrapolation is certified.
    """
    start=next((i for i,x in enumerate(terms) if x!=0),None)
    if start is None or not _well_informed(terms[start:]):return None
    values=terms[start:]
    if any(v==0 for v in values):return None
    ratios=[Q(values[i+1],values[i]) for i in range(len(values)-1)]
    if len(ratios)<min_total_ratios:return None
    combos=sorted(itertools.product(range(max_degree+1), repeat=2),
                  key=lambda a:(sum(a),max(a),a[1]))
    for pdeg,qdeg in combos:
        unknown=pdeg+qdeg+1  # q(0)=1
        fitting=max(fitting_min,unknown+3)
        if len(ratios)<fitting+min_holdout:continue
        matrix=[];rhs=[]
        for k,r in enumerate(ratios[:fitting]):
            matrix.append([Q(k**j) for j in range(pdeg+1)]
                          +[-r*Q(k**j) for j in range(1,qdeg+1)])
            rhs.append(r)
        fit=_solve_unique(matrix,rhs)
        if fit is None:continue
        p=_trim(fit[:pdeg+1]);q=_trim([Q(1)]+fit[pdeg+1:])
        if all(_poly(q,k) and ratios[k]*_poly(q,k)==_poly(p,k)
               for k in range(len(ratios))):
            return {'start_local':start,'start_mathematical':offset+start,
                    'base':str(values[0]),
                    'numerator':[str(x) for x in p],
                    'denominator':[str(x) for x in q],
                    'fitted_ratios':fitting,'holdout_ratios':len(ratios)-fitting,
                    'checked_ratios':len(ratios),
                    'pochhammer':_pochhammer_form(p,q),
                    'status':'finite_candidate'}
    return None


def mine_rational_ratios(db, *, max_degree=2):
    ensure_miner_schema(db)
    data=load_sequences(db)
    db.execute('DELETE FROM rational_ratio_candidates')
    by_family=Counter();result=[]
    for sid,(offset,terms) in data.items():
        fit=infer_ratio(terms,offset,max_degree=max_degree)
        if fit is None:continue
        source_hash=_hash_terms(offset,terms)
        db.execute('''INSERT INTO rational_ratio_candidates VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?)''',(
            sid,fit['start_local'],fit['start_mathematical'],fit['base'],
            json.dumps(fit['numerator']),json.dumps(fit['denominator']),
            json.dumps(fit['pochhammer']) if fit['pochhammer'] else None,
            fit['fitted_ratios'],fit['holdout_ratios'],fit['checked_ratios'],
            'finite_candidate',source_hash))
        by_family['pochhammer' if fit['pochhammer'] else 'rational_ratio_only']+=1
        result.append({'oeis_id':sid,**fit})
    db.commit()
    return {'candidates':len(result),'categories':dict(by_family),'details':result,
            'warning':'A fit to finite OEIS coefficients is not an infinite identity proof'}


def candidates(db, *, oeis_id=None, operator=None, limit=50):
    ensure_miner_schema(db)
    query='SELECT output_id,inputs_json,operator,parameters_json,checked_terms,holdout_terms,statement FROM transfer_candidates WHERE 1=1'
    params=[]
    if oeis_id:
        query+=' AND (output_id=? OR inputs_json LIKE ?)'
        params.extend([oeis_id,'%"'+oeis_id+'"%'])
    if operator:
        query+=' AND operator=?';params.append(operator)
    query+=' ORDER BY holdout_terms DESC,checked_terms DESC,output_id LIMIT ?'
    params.append(limit)
    return [{'output':r[0],'inputs':json.loads(r[1]),'operator':r[2],
             'params':json.loads(r[3]),'checked_terms':r[4],
             'holdout_terms':r[5],'statement':r[6],
             'status':'finite_candidate'} for r in db.execute(query,params)]


def materialize_candidates(db):
    """Expose candidate hyperedges in graph, *without adding proof paths*."""
    ensure_miner_schema(db)
    from sequence_transfer_graph import _node,_edge
    # Refresh is idempotent and removes previous candidate projections,
    # including those invalidated by a subsequently changed source.
    db.execute("DELETE FROM transfer_edges WHERE status='finite_candidate'")
    db.execute("DELETE FROM transfer_nodes WHERE type IN ('candidate_hyperedge','candidate_recurrence')")
    current=load_sequences(db,include_local=True)
    digests={sid:_hash_terms(*value) for sid,value in current.items()}
    for (cid,out,inputs_raw,op,params_raw,checked,fit,holdout,statement,
         status,source,hashes) in db.execute('SELECT * FROM transfer_candidates'):
        inputs=json.loads(inputs_raw);param=json.loads(params_raw)
        if any(digests.get(sid)!=hashval for sid,hashval in json.loads(hashes).items()):
            continue  # Changed OEIS terms invalidate a finite-match certificate.
        if len(inputs)==1:
            _edge(db,inputs[0],out,'candidate_'+op,'finite_candidate',statement,
                  f'Exact integer prefix: {fit} discovery; {holdout} holdout; '
                  'no infinite identity proof',checked,
                  'not benchmarked',f'https://oeis.org/{out}',param)
        else:
            hyper='HYPER:'+cid
            _node(db,hyper,'candidate_hyperedge',op,
                  {'inputs':inputs,'output':out,'parameters':param,
                   'checked_terms':checked,'status':'finite_candidate'})
            for source_id in inputs:
                _edge(db,source_id,hyper,'hyperedge_input','finite_candidate',
                      statement,'Input required for unproved multi-sequence relation',
                      checked,'not benchmarked',f'https://oeis.org/{out}',{'candidate':cid,'source':source_id})
            _edge(db,hyper,out,'hyperedge_output','finite_candidate',statement,
                  f'Exact integer prefix: {fit} discovery; {holdout} holdout; no infinite identity proof',
                  checked,'not benchmarked',f'https://oeis.org/{out}',{'candidate':cid})
    for (sid,start,start_math,base,p,q,poch,fit,holdout,checked,status,hash) in db.execute(
        'SELECT * FROM rational_ratio_candidates'):
        if digests.get(sid) != hash:
            continue  # Stored terms changed after finite-ratio discovery.
        _node(db,'RATIO:'+sid,'candidate_recurrence','rational ratio '+sid,
              {'start':start_math,'local_start':start,'base':base,'P':json.loads(p),
               'Q':json.loads(q),'pochhammer':json.loads(poch) if poch else None,
               'fitted_ratios':fit,'holdout_ratios':holdout,
               'status':'finite_candidate'})
        _edge(db,'RATIO:'+sid,sid,'rational_ratio','finite_candidate',
              f'Q(t)*a(start+t+1)=P(t)*a(start+t), t>=0 (candidate); start={start_math}',
              f'{fit} fitted ratios, {holdout} exact holdout ratios; no global proof',
              checked,'not benchmarked',f'https://oeis.org/{sid}',{'local_start':start})


def export_candidates(db,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    counts=Counter()
    with path.open('w',encoding='utf-8',newline='\n') as f:
        for r in db.execute('SELECT * FROM transfer_candidates ORDER BY candidate_id'):
            cid,out,inputs,op,params,checked,fit,holdout,statement,status,source,hashes=r
            row={'kind':'transfer','id':cid,'output':out,'inputs':json.loads(inputs),
                 'operator':op,'parameters':json.loads(params),
                 'checked_terms':checked,'discovery_terms':fit,
                 'holdout_terms':holdout,'statement':statement,
                 'status':status,'source':source,'source_hashes':json.loads(hashes)}
            f.write(json.dumps(row,ensure_ascii=False)+'\n');counts['transfer']+=1
        for r in db.execute('SELECT * FROM rational_ratio_candidates ORDER BY oeis_id'):
            sid,start,start_math,base,p,q,poch,fit,holdout,checked,status,hash=r
            row={'kind':'ratio','oeis_id':sid,'local_start':start,'mathematical_start':start_math,
                 'base':base,'numerator':json.loads(p),'denominator':json.loads(q),
                 'pochhammer':json.loads(poch) if poch else None,
                 'fitted_ratios':fit,'holdout_ratios':holdout,
                 'checked_ratios':checked,'status':status,'source_hash':hash}
            f.write(json.dumps(row,ensure_ascii=False)+'\n');counts['ratio']+=1
    return {'path':str(path),'records':dict(counts)}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    subs=p.add_subparsers(dest='command',required=True)
    m=subs.add_parser('mine');m.add_argument('--min-terms',type=int,default=10)
    m.add_argument('--max-modulus',type=int,default=4)
    m.add_argument('--no-pairs',action='store_true')
    m.add_argument('--include-komorebi',action='store_true')
    m.add_argument('--max-sequences',type=int,default=10000)
    m.add_argument('--export',type=Path)
    l=subs.add_parser('list');l.add_argument('--id');l.add_argument('--operator');l.add_argument('--limit',type=int,default=30)
    s=subs.add_parser('stats')
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        if args.command=='mine':
            transfer=mine_transfers(db,min_terms=args.min_terms,max_modulus=args.max_modulus,include_pairs=not args.no_pairs,
                                    include_local=args.include_komorebi,max_sequences=args.max_sequences)
            ratios=mine_rational_ratios(db)
            output={'transfer':transfer,'ratios':{k:v for k,v in ratios.items() if k!='details'}}
            if args.export:output['export']=export_candidates(db,args.export)
        elif args.command=='list':output=candidates(db,oeis_id=args.id,operator=args.operator,limit=args.limit)
        else:
            ensure_miner_schema(db)
            output={'transfers':db.execute('SELECT COUNT(*) FROM transfer_candidates').fetchone()[0],
                    'ratios':db.execute('SELECT COUNT(*) FROM rational_ratio_candidates').fetchone()[0]}
    print(json.dumps(output,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
