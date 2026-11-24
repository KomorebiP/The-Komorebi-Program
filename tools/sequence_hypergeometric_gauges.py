"""Exact hypergeometric transfer gauges between formula-defined sequences.

Author: Komorebi P.

If two formula expressions have rational successive-term ratios r_A(t),
r_B(t), solve r_B/r_A=c*L(t+1)/L(t) with a rational product L of
linear factors. A single base evaluation certifies the transfer on a
non-singular tail. OEIS identification still requires separate proof.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, sqlite3
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
from sequence_ratio_certificates import Ratio,derive_ratio,ratio_polynomials
from sequence_holonomic_compiler import Rat, fraction_eval, pzero, trim, start_and_components, peval


def local_ratio(r,offset):
    s=Ratio();s.scalar=r.scalar
    for (a,b),e in r.factors.items():
        if e:s.factor(a,b+a*offset,e)
    return s


def source_model(fid,sid,ast,off,raw,source_sha):
    vals=[int(x) for x in json.loads(raw)]
    data=start_and_components(ast,off,vals,max_components=1)
    if data is None:return None
    tail,parts,_=data
    if len(parts)!=1:return None
    r=derive_ratio(parts[0],off+tail)
    if r is None:return None
    r=local_ratio(r,off)
    return {'oeis_id':sid,'formula_id':fid,'source_sha256':source_sha,
        'evaluator_sha256':hashlib.sha256(json.dumps(ast,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'ast':ast,'offset':off,'tail':tail,'ratio':r}


def difference_ratio(source,target):
    d=Ratio();d.mul(target['ratio']);d.mul(source['ratio'],-1)
    # Strip recorded zero-exponent factors.
    for z in list(d.factors):
        if not d.factors[z]:del d.factors[z]
    return d


def solve_gauge(d,max_support=4,max_span=12,max_degree=7):
    """Solve shift-coboundary for linear factors using residue orbits.

    Let e_(a,b) be exponent of (at+b) in d/c. We require
      e_(a,b) = x_(a,b-a)-x_(a,b),
    with finite support x. Each progression b modulo a must sum to zero.
    """
    groups=defaultdict(dict)
    for (a,b),power in d.factors.items():
        if power:
            if a<=0:return None
            groups[(a,b%a)][b]=power
    out={}
    for (a,residue),terms in groups.items():
        indices=sorted(terms)
        if (indices[-1]-indices[0])//a>max_span:return None
        current=0
        for b in range(indices[0],indices[-1]+a,a):
            current-=terms.get(b,0)
            if current:out[(a,b)]=current
        if current:return None
    out={key:v for key,v in out.items() if v}
    if sum(abs(v) for v in out.values())>max_support:return None
    if sum(max(0,v) for v in out.values())>max_degree or sum(max(0,-v) for v in out.values())>max_degree:
        return None
    L=Rat()
    for (a,b),power in sorted(out.items()):
        term=Rat((b,a))
        for _ in range(abs(power)):
            L=L*term if power>0 else L/term
    D=Rat(*ratio_polynomials(d))
    if L.shift(1)/L*Rat((d.scalar,))!=D:
        raise AssertionError('factor-orbit gauge fails symbolic rational identity')
    return out,L


def gauge_value(ledger,t):
    v=F(1)
    for m in ledger:
        z=F(m['a']*t+m['b'])
        v*=z**m['power']
    return v


def certify_pair(source,target,max_support=4):
    if source['oeis_id']==target['oeis_id']:return None
    diff=difference_ratio(source,target)
    gauge=solve_gauge(diff,max_support=max_support)
    if gauge is None:return None
    factors,L=gauge
    start=max(source['tail'],target['tail'])
    # Source/target ratios and gauge factors must be nonzero at all later t.
    if any(a*start+b<=0 for a,b in factors):return None
    try:
        a0=fraction_eval(source['ast'],source['offset']+start)
        b0=fraction_eval(target['ast'],target['offset']+start)
        if a0==0 or b0==0 or not L.at(start):return None
        K=b0/a0
        if not K:return None
        # Secondary checks evaluate formulas, not the stored OEIS prefixes.
        for t in (start,start+1,start+3,start+7):
            sa=fraction_eval(source['ast'],source['offset']+t)
            tb=fraction_eval(target['ast'],target['offset']+t)
            predicted=K*diff.scalar**(t-start)*L.at(t)/L.at(start)*sa
            if predicted!=tb:raise AssertionError('exact gauge fails independent value checks')
    except (ValueError,ZeroDivisionError,OverflowError):return None
    entries=[{'a':a,'b':b,'power':v} for (a,b),v in sorted(factors.items())]
    return {'source':source['oeis_id'],'target':target['oeis_id'],'source_formula':source['formula_id'],
        'target_formula':target['formula_id'],'source_sha256':source['source_sha256'],
        'target_sha256':target['source_sha256'],
        'source_evaluator_sha256':source['evaluator_sha256'],
        'target_evaluator_sha256':target['evaluator_sha256'],
        'source_offset':source['offset'],'target_offset':target['offset'],
        'tail_start_local':start,'base_ratio':str(K),'exponential_factor':str(diff.scalar),
        'gauge_linear_factors':entries,'support':sum(abs(v) for v in factors.values()),
        'proof_method':'Exact shift-orbit factor equations in Q(t), plus one nonzero initial ratio; valid on the nonsingular tail',
        'scope':'All-index equality of the supplied formula expressions for local t>=tail_start_local; source OEIS identification finite-checked only'}


def load_models(db,extra=None):
    models={};counts=Counter()
    query='''SELECT f.formula_id,f.oeis_id,f.evaluator_json,s.offset,s.terms_json,s.source_sha256
       FROM formulas f JOIN sequences s ON f.oeis_id=s.oeis_id
       WHERE f.origin='oeis_normalized' AND f.verification='finite_checked'
       ORDER BY f.oeis_id,f.formula_id'''
    for fid,sid,ast,off,terms,sha in db.execute(query):
        if sid in models:continue
        counts['attempted']+=1
        try:
            m=source_model(fid,sid,json.loads(ast),off,terms,sha)
            if m is not None:models[sid]=m;counts['models']+=1
        except (ValueError,ArithmeticError,OverflowError,AssertionError):counts['unsupported']+=1
    if extra:
        for line in Path(extra).open(encoding='utf8'):
            if not line.strip():continue
            x=json.loads(line)
            sid=x['oeis_id']
            if x.get('verification')!='finite_checked':continue
            row=db.execute('SELECT offset,terms_json,source_sha256,name FROM sequences WHERE oeis_id=?',(sid,)).fetchone()
            if not row:continue
            off,terms,sha,name=row
            # Re-verify supplemental source receipts, rather than trusting
            # a JSONL record that could have been edited after extraction.
            if x.get('source_formula_id'):
                raw=db.execute("SELECT expression FROM formulas WHERE formula_id=? AND oeis_id=? AND origin='oeis_formula'",
                               (x['source_formula_id'],sid)).fetchone()
                if not raw or hashlib.sha256(raw[0].encode()).hexdigest()!=x['source_line_sha256']:
                    raise ValueError('supplemental raw OEIS formula has changed: '+sid)
            elif hashlib.sha256(name.encode()).hexdigest()!=x['source_line_sha256']:
                raise ValueError('supplemental OEIS description has changed: '+sid)
            from sequence_oeis_chain_normalizer import verify
            count,status=verify(db,sid,x['evaluator'])
            if status!='finite_checked' or count!=x['checked_terms']:
                raise ValueError('supplemental formula no longer finite-checks: '+sid)
            m=source_model(x['formula_id'],sid,x['evaluator'],off,terms,sha)
            if m is not None:models[sid]=m;counts['extra_models']+=1
    return models,counts


def discover(db,output,summary=None,extra=None,max_support=3,max_pairs=None):
    models,counts=load_models(db,extra)
    records=list(models.values());edges=[];attempted=0
    for s,t in itertools.combinations(records,2):
        if max_pairs is not None and attempted>=max_pairs:break
        attempted+=1
        # Try both directions, but algebraic path is invertible when all factors
        # remain nonsingular. Keep one oriented certificate to prevent doubling.
        try:c=certify_pair(s,t,max_support)
        except (AssertionError,ArithmeticError,OverflowError):
            counts['algebra_error']+=1;continue
        if c:
            edges.append(c);counts['gauges']+=1
            typ=('rational' if c['support'] else 'none', c['exponential_factor']!='1')
            counts['kind_'+str(typ)]+=1
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf8') as stream:
        for e in edges:stream.write(json.dumps(e,separators=(',',':'))+'\n')
    stats={'status':'all_index_formula_gauges','single_term_models':len(models),'pairwise_checked':attempted,
         'gauges':len(edges),'source_records_attempted':counts['attempted'],
         'extra_models':counts['extra_models'],'nonclaims':'No global OEIS identification, speedup, or novelty claim'}
    if summary:Path(summary).write_text(json.dumps(stats,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return stats



def structured_discover(db,output,summary=None,extra=None,max_support=2,max_neighbors=140):
    """Inverted-index candidate search prioritizing non-C-finite targets.

    A full pairwise O(N^2) gauge search creates many mathematically vacuous
    links. Use common (or adjacent shifted) affine factors to propose nearby
    formula families, then prove a small gauge exactly.
    """
    from sequence_linear_identity_compiler import normalized
    models,counts=load_models(db,extra)
    inverted=defaultdict(set)
    for sid,m in models.items():
        for factor,power in m['ratio'].factors.items():
            if power:inverted[factor].add(sid)
    noncfinite=[sid for sid,m in models.items() if normalized(m['ast'],m['offset']) is None]
    seen=set();edges=[];examined=0;proposed=0
    for target in sorted(noncfinite):
        m=models[target];weights=Counter()
        for (a,b),power in m['ratio'].factors.items():
            if not power:continue
            for shift in (-a,0,a):
                for sid in inverted.get((a,b+shift),()):
                    if sid!=target:weights[sid]+=2 if shift==0 else 1
        nearby=sorted(weights,key=lambda sid:(-weights[sid],sid))[:max_neighbors]
        proposed+=len(nearby)
        for sid in nearby:
            pair=tuple(sorted((sid,target)))
            if pair in seen:continue
            seen.add(pair);examined+=1
            x,y=(models[id] for id in pair)
            try:c=certify_pair(x,y,max_support=max_support)
            except (AssertionError,ArithmeticError,OverflowError):
                counts['symbolic_rejections']+=1;continue
            if c:edges.append(c)
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf8') as stream:
        for e in edges:stream.write(json.dumps(e,separators=(',',':'))+'\n')
    stats={'status':'all_index_formula_gauges','single_term_models':len(models),
       'non_constant_recurrence_models':len(noncfinite),
       'candidate_neighbors':proposed,'distinct_pairs_examined':examined,
       'certified_gauges':len(edges),'maximum_affine_factor_support':max_support,
       'scope':'Exact identities of admitted source formula expressions on explicit tails; not OEIS global identification'}
    if summary:Path(summary).write_text(json.dumps(stats,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return stats


def replay_gauges(db,ledger,extra=None):
    """Rebuild each exact rational-function gauge from current source bytes."""
    models,_=load_models(db,extra)
    counts=Counter();fails=[]
    for line in Path(ledger).open(encoding='utf8'):
        if not line.strip():continue
        old=json.loads(line);counts['attempted']+=1
        try:
            x=models.get(old['source']);y=models.get(old['target'])
            if x is None or y is None:raise ValueError('missing source formula')
            if x['source_sha256']!=old['source_sha256'] or y['source_sha256']!=old['target_sha256']:
                raise ValueError('source content fingerprint mismatch')
            new=certify_pair(x,y,max_support=max(4,old['support']))
            if new is None:raise ValueError('exact gauge not reproducible')
            for key in ('source_formula','target_formula','source_evaluator_sha256',
                        'target_evaluator_sha256','tail_start_local','base_ratio',
                        'exponential_factor','gauge_linear_factors'):
                if old[key]!=new[key]:raise ValueError('formula gauge metadata mismatch: '+key)
            counts['passed']+=1
        except (ValueError,ArithmeticError,AssertionError,TypeError,KeyError) as exc:
            counts['failed']+=1
            if len(fails)<12:fails.append({'source':old.get('source'),'target':old.get('target'),'error':str(exc)})
    return {'status':'passed' if counts['failed']==0 else 'failed',**counts,'samples':fails,
        'scope':'Exact extracted-formula identities, not a global OEIS sequence identity'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    p.add_argument('--summary',type=Path);p.add_argument('--extra',type=Path);p.add_argument('--max-pairs',type=int)
    p.add_argument('--structured',action='store_true');p.add_argument('--max-support',type=int,default=2)
    p.add_argument('--replay',action='store_true')
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        stats=(replay_gauges(db,args.output,args.extra) if args.replay else structured_discover(db,args.output,args.summary,args.extra,max_support=args.max_support) if args.structured else discover(db,args.output,args.summary,args.extra,max_pairs=args.max_pairs))
    print(json.dumps(stats,indent=2))
    if stats['status']=='failed':raise SystemExit(1)
if __name__=='__main__':main()
