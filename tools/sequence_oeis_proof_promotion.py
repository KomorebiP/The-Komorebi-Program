"""All-index algebraic proof promotion for real OEIS finite-transfer leads.

Author: Komorebi P.

A proof here establishes an identity between TWO SUPPLIED, independently
extracted exact formula expressions on their common local index n>=0. OEIS
identification for all n is NOT established by its stored finite terms. A
candidate remains finite_candidate in its original table, and is promoted in
an independent, content-addressed table only when structural recurrences
and a sufficiently long exact initial-state witness prove the formula equality.

For recurrences P(S)b=0 and Q(S)c=0, P(S)Q(S)(b-c)=0 when both b and c obey
one of P and Q respectively: the product annihilates each, since shifts
commute. Vanishing of the first deg(P)+deg(Q) terms proves equality for all n.

No raw OEIS text or program listings are ever executed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
from math import comb
from pathlib import Path
import sqlite3

from oeis_formula_database import evaluate
from sequence_exponential_polynomial import infer
from sequence_recurrence_packets import (companion, characteristic, mat_pow)
from sequence_transfer_closure import shift_monic_polynomial

SCHEMA = '''
CREATE TABLE IF NOT EXISTS oeis_formula_transfer_proofs (
 candidate_id TEXT PRIMARY KEY,
 source_id TEXT NOT NULL,
 output_id TEXT NOT NULL,
 operator TEXT NOT NULL,
 source_formula_id TEXT NOT NULL,
 target_formula_id TEXT NOT NULL,
 source_record_sha256 TEXT NOT NULL,
 target_record_sha256 TEXT NOT NULL,
 source_formula_sha256 TEXT NOT NULL,
 target_formula_sha256 TEXT NOT NULL,
 certificate_json TEXT NOT NULL,
 proof_scope TEXT NOT NULL CHECK(proof_scope='normalized_formula_identity'),
 FOREIGN KEY(candidate_id) REFERENCES transfer_candidates(candidate_id)
);
CREATE INDEX IF NOT EXISTS idx_oeis_promotion_source ON oeis_formula_transfer_proofs(source_id);
CREATE INDEX IF NOT EXISTS idx_oeis_promotion_target ON oeis_formula_transfer_proofs(output_id);
'''

SUPPORTED = frozenset((
    'shift', 'polyphase', 'add_constant', 'multiply_constant',
    'adjacent_difference', 'prefix_sum', 'binomial_transform',
    'inverse_binomial_transform',
))


def sequence(initial, coeffs, count):
    """Exact recurrence stepping. Complexity O(count*order); index is local."""
    if type(count) is not int or count < 0:
        raise ValueError('nonnegative count required')
    if not coeffs or len(initial)!=len(coeffs) or any(type(x) is not int for x in initial+coeffs):
        raise ValueError('invalid integer recurrence')
    d=len(coeffs)
    out=list(initial)
    for n in range(d,count):
        out.append(sum(coeffs[j]*out[n-j-1] for j in range(d)))
    return out[:count]


def times_s_minus_one(coeffs):
    """(X-1) (X^d-c1X^(d-1)-...-cd), returned as recurrence."""
    p=[1]+[-x for x in coeffs]
    q=[0]*(len(p)+1)
    for i,x in enumerate(p):
        q[i]+=x
        q[i+1]-=x
    assert q[0]==1
    return [-x for x in q[1:]]


@lru_cache(maxsize=512)
def _phase_coefficients(coeff_tuple, modulus):
    a=mat_pow(companion(list(coeff_tuple)),modulus)
    p=characteristic(a)
    if p[0]!=1:raise ArithmeticError('phase polynomial is not monic')
    return tuple(-x for x in p[1:])


def apply_operator(coeffs, initial, operator, params):
    """Return exact C-finite recurrence and initial vector of a transfer.

    The operator is a *local-index* map, not a claim about source/target
    mathematical OEIS offset equivalence. That mapping is recorded separately.
    """
    if operator not in SUPPORTED:raise ValueError('unsupported operator')
    d=len(coeffs)
    if d<1 or d>18:raise ValueError('recurrence order outside audited bound')
    if len(initial)!=d:raise ValueError('initial length mismatch')
    if operator=='shift':
        s=params['shift']
        if type(s) is not int or s<0 or s>200:raise ValueError('invalid shift')
        initial2=sequence(initial,coeffs,d+s)[s:s+d]
        return list(coeffs),initial2,'The shift of a C-finite sequence has the same annihilating shift polynomial.'
    if operator=='polyphase':
        m,r=params['modulus'],params['residue']
        if type(m) is not int or type(r) is not int or not 2<=m<=12 or not 0<=r<m:
            raise ValueError('invalid phase')
        coefficients=list(_phase_coefficients(tuple(coeffs),m))
        source=sequence(initial,coeffs,m*(d-1)+r+1)
        initial2=[source[m*i+r] for i in range(d)]
        return coefficients,initial2,'Cayley-Hamilton applied to the exact shift operator S^m proves the phase recurrence.'
    if operator=='add_constant':
        k=params['constant']
        if type(k) is not int:raise ValueError('nonintegral constant')
        coefficients=times_s_minus_one(coeffs)
        initial2=[x+k for x in sequence(initial,coeffs,d+1)]
        return coefficients,initial2,'(S-1) annihilates the constant sequence; (S-1)P(S) annihilates the sum.'
    if operator=='multiply_constant':
        k=params['constant']
        if type(k) is not int:raise ValueError('nonintegral multiplier')
        return list(coeffs),[k*x for x in initial],'Scalar multiplication commutes with the recurrence shift operator.'
    if operator=='adjacent_difference':
        src=sequence(initial,coeffs,d+1)
        return list(coeffs),[src[i+1]-src[i] for i in range(d)],'P(S) commutes with S-1, so the adjacent difference satisfies P(S).'
    if operator=='prefix_sum':
        src=sequence(initial,coeffs,d+1)
        initial2=[]
        acc=0
        for x in src:
            acc+=x
            initial2.append(acc)
        return times_s_minus_one(coeffs),initial2,'(S-1)b(n)=a(n+1); hence P(S)(S-1)b(n)=0.'
    if operator in ('binomial_transform','inverse_binomial_transform'):
        inverse=operator=='inverse_binomial_transform'
        coefficients=shift_monic_polynomial(coeffs,1 if inverse else -1)
        src=sequence(initial,coeffs,d)
        iv=[sum(comb(n,k)*src[k]*((-1)**(n-k) if inverse else 1)
                for k in range(n+1)) for n in range(d)]
        return coefficients,iv,'EGF conjugation: exp(±x) P(D) exp(∓x)=P(D∓1), with exact binomial initial data.'
    raise AssertionError('unreachable')


def direct_operator(source, operator, params, n):
    if operator=='shift':return source[n+params['shift']]
    if operator=='polyphase':return source[params['modulus']*n+params['residue']]
    if operator=='add_constant':return source[n]+params['constant']
    if operator=='multiply_constant':return source[n]*params['constant']
    if operator=='adjacent_difference':return source[n+1]-source[n]
    if operator=='prefix_sum':return sum(source[:n+1])
    if operator=='binomial_transform':return sum(comb(n,k)*source[k] for k in range(n+1))
    if operator=='inverse_binomial_transform':return sum((-1)**(n-k)*comb(n,k)*source[k] for k in range(n+1))
    raise ValueError('unsupported operator')


def maximum_source_index(op,params,output_terms):
    if op=='shift':return output_terms+params['shift']
    if op=='polyphase':return (output_terms-1)*params['modulus']+params['residue']+1
    if op=='adjacent_difference':return output_terms+1
    return output_terms


def check_recurrence(spec, offset, coeffs, iv):
    """Independent DSL control, distinct from our recurrence generation."""
    count=min(max(2*len(coeffs)+4,12),42)
    vals=sequence(iv,coeffs,count)
    for n,x in enumerate(vals):
        if x!=evaluate(spec,offset+n):
            raise ValueError('inferred recurrence contradicts DSL evaluator')
    return count


def _source_signature(spec, fid, source_hash, offset, terms):
    recipe=infer(spec,offset)
    if recipe is None:return None
    coeffs=recipe['coefficients'];initial=recipe['initial']
    if len(coeffs)>18 or not coeffs:return None
    numchecks=check_recurrence(spec,offset,coeffs,initial)
    return {'formula_id':fid,'spec':spec,'offset':offset,'source_sha256':source_hash,
            'coefficients':coeffs,'initial':initial,'method':recipe['method'],
            'source_term_count':terms, 'dsl_check_terms':numchecks}


def _agree_across_formulas(definitions):
    """Certify all alternate supported formulae agree globally at n>=0.

    Disagreement yields a conflict instead of picking an arbitrary formula.
    """
    if len(definitions)<=1:return True
    base=definitions[0]
    for other in definitions[1:]:
        D=len(base['coefficients'])+len(other['coefficients'])
        if sequence(base['initial'],base['coefficients'],D)!=sequence(other['initial'],other['coefficients'],D):
            return False
    return True


def promote(db, *, max_edges=None, control_extra=5, batch_size=250, export=None):
    """Promote finite candidates only when the *formulae* are all-index equal.

    Candidate table stays untouched. A separate evidence ledger holds source
    hashes, formula IDs, recurrence polynomials, finite initial witness and
    the proof by the product annihilator. Rerun with fresh source receipts.
    """
    if type(control_extra) is not int or not 0<=control_extra<=30:raise ValueError('invalid controls')
    if type(batch_size) is not int or batch_size<1:raise ValueError('invalid batch_size')
    db.executescript(SCHEMA)
    defs={}; counts=Counter()
    q='''SELECT f.oeis_id,f.formula_id,f.evaluator_json,s.offset,s.source_sha256,
                 f.checked_terms
         FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
         WHERE f.origin='oeis_normalized' AND f.verification='finite_checked'
         ORDER BY f.oeis_id, f.formula_id'''
    for sid,fid,raw,offset,sha,terms in db.execute(q):
        try:
            item=_source_signature(json.loads(raw),fid,sha,offset,terms)
            if item is not None:
                defs.setdefault(sid,[]).append(item)
                counts['structurally_supported_formulas']+=1
        except (ValueError,TypeError,OverflowError,ZeroDivisionError,ArithmeticError):
            counts['source_formula_rejected']+=1
    selected={}
    for sid,items in defs.items():
        if not _agree_across_formulas(items):
            counts['conflicted_source_ids']+=1
            continue
        selected[sid]=min(items,key=lambda t:(len(t['coefficients']),t['formula_id']))
    counts['supported_source_ids']=len(selected)
    # Rebuild in one transaction: a failed promotion cannot leave partial evidence.
    db.execute('BEGIN')
    db.execute('DELETE FROM oeis_formula_transfer_proofs')
    proofs=[]
    for cid,out,raw_inputs,op,raw_params,checked in db.execute('''
       SELECT candidate_id,output_id,inputs_json,operator,parameters_json,checked_terms
       FROM transfer_candidates ORDER BY candidate_id'''):
        if max_edges is not None and counts['candidates_scanned']>=max_edges:break
        counts['candidates_scanned']+=1
        if op not in SUPPORTED:
            counts['operator_unsupported']+=1;continue
        input_ids=json.loads(raw_inputs)
        if len(input_ids)!=1 or out not in selected or input_ids[0] not in selected:
            counts['missing_formula']+=1;continue
        source_id=input_ids[0]
        a,b=selected[source_id],selected[out]
        params=json.loads(raw_params)
        try:
            c2,iv2,why=apply_operator(a['coefficients'],a['initial'],op,params)
            D=len(c2)+len(b['coefficients'])
            generated=sequence(iv2,c2,D+control_extra)
            target=sequence(b['initial'],b['coefficients'],D+control_extra)
            if generated[:D]!=target[:D]:
                counts['all_index_equality_rejected']+=1
                continue
            # Extra checks catch operator implementation mistakes; proof uses D alone.
            if generated[D:]!=target[D:]:
                raise ArithmeticError('control beyond the proof window failed')
            if checked and checked<10:
                raise ArithmeticError('candidate was not independently prefiltered')
            src_count=maximum_source_index(op,params,D+control_extra)
            original=sequence(a['initial'],a['coefficients'],src_count)
            for n in range(D+control_extra):
                if generated[n]!=direct_operator(original,op,params,n):
                    raise ArithmeticError('operator implementation contradicts direct exact transform')
            source_spec_sha=hashlib.sha256(json.dumps(a['spec'],sort_keys=True).encode()).hexdigest()
            target_spec_sha=hashlib.sha256(json.dumps(b['spec'],sort_keys=True).encode()).hexdigest()
            cert={'certificate_version':1,'candidate_id':cid,
                  'formula_source':a['formula_id'],'formula_target':b['formula_id'],
                  'index_variable':'local n>=0',
                  'source_oeis_offset':a['offset'],'target_oeis_offset':b['offset'],
                  'operator':op,'parameters':params,
                  'source_recurrence':a['coefficients'],
                  'transferred_recurrence':c2,'target_recurrence':b['coefficients'],
                  'annihilator_product_degree':D,'checked_initial_conditions':D,
                  'additional_controls':control_extra,
                  'first_initial_values':[str(x) for x in generated[:min(D,12)]],
                  'source_formula_method':a['method'],'target_formula_method':b['method'],
                  'proof':'P_source_transformed(S) and P_target(S) annihilate the two sequences. Their difference is annihilated by the product of these commuting monic shift polynomials. The first product-degree terms agree, so the difference vanishes for every local n>=0.',
                  'operator_proof':why,
                  'scope':'identity between normalized formula expressions for all local n>=0; OEIS sequence identification from finite terms is not proved'}
            db.execute('''INSERT INTO oeis_formula_transfer_proofs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',(
                cid,source_id,out,op,a['formula_id'],b['formula_id'],a['source_sha256'],b['source_sha256'],
                source_spec_sha,target_spec_sha,json.dumps(cert,separators=(',',':')),'normalized_formula_identity'))
            proofs.append({'candidate_id':cid,'source_id':source_id,'output_id':out,
                           'operator':op,'source_formula_id':a['formula_id'],
                           'target_formula_id':b['formula_id'],'certificate':cert})
            counts['formula_identities_certified']+=1
            counts['by_'+op]+=1
        except (ValueError,TypeError,OverflowError,ZeroDivisionError,ArithmeticError,KeyError,AssertionError) as exc:
            counts['operator_error']+=1
            if counts['operator_error']<=6:
                counts.setdefault('operator_error_samples',[]).append({'candidate_id':cid,'error':type(exc).__name__+': '+str(exc)[:150]})
    db.commit()
    if export:
        export=Path(export);export.parent.mkdir(parents=True,exist_ok=True)
        with export.open('w',encoding='utf-8') as fh:
            for item in proofs:fh.write(json.dumps(item,ensure_ascii=False,separators=(',',':'))+'\n')
    counts['by_operator']={k[3:]:v for k,v in sorted(counts.items()) if k.startswith('by_')}
    counts['status']='formula_identity_conditional_on_source_oeis_definitions'
    counts['original_candidate_rows_unchanged']=db.execute('SELECT count(*) FROM transfer_candidates').fetchone()[0]
    counts['proof_rows']=db.execute('SELECT count(*) FROM oeis_formula_transfer_proofs').fetchone()[0]
    return dict(counts)




def replay_certificate(db, candidate_id):
    """Reconstruct source receipts and validate a theorem by two paths.

    The second path calls the exact evaluator at the source and target indices
    instead of relying on cached recurrence terms. It checks data provenance
    and mathematical offsets before accepting a certificate.
    """
    row=db.execute('''SELECT source_id,output_id,operator,source_formula_id,target_formula_id,
       source_record_sha256,target_record_sha256,source_formula_sha256,
       target_formula_sha256,certificate_json FROM oeis_formula_transfer_proofs
       WHERE candidate_id=?''',(candidate_id,)).fetchone()
    if not row:raise ValueError('missing certificate: '+candidate_id)
    source_id,out,op,fida,fidb,sha_a,sha_b,spec_sha_a,spec_sha_b,rawcert=row
    cert=json.loads(rawcert)
    if cert['candidate_id']!=candidate_id or cert['formula_source']!=fida or cert['formula_target']!=fidb:
        raise ValueError('certificate identity mismatch')
    if cert['operator']!=op:raise ValueError('certificate operator mismatch')
    rec=db.execute('SELECT output_id,inputs_json,operator,parameters_json FROM transfer_candidates WHERE candidate_id=?',(candidate_id,)).fetchone()
    if rec is None or rec[0]!=out or json.loads(rec[1])!=[source_id] or rec[2]!=op or json.loads(rec[3])!=cert['parameters']:
        raise ValueError('candidate receipt mismatch')
    inputs=[]
    for sid,fid,expected_source_sha,expected_formula_sha in ((source_id,fida,sha_a,spec_sha_a),(out,fidb,sha_b,spec_sha_b)):
        entry=db.execute('''SELECT f.evaluator_json,f.verification,s.offset,s.source_sha256
               FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
               WHERE f.formula_id=? AND f.oeis_id=?''',(fid,sid)).fetchone()
        if entry is None or entry[1]!='finite_checked' or entry[3]!=expected_source_sha:
            raise ValueError('source changed or formula revoked: '+sid)
        spec=json.loads(entry[0])
        if hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()!=expected_formula_sha:
            raise ValueError('formula hash mismatch: '+sid)
        found=infer(spec,entry[2])
        if found is None or len(found['coefficients'])>18:
            raise ValueError('formula no longer structurally supported: '+sid)
        check_recurrence(spec,entry[2],found['coefficients'],found['initial'])
        inputs.append((entry[2],spec,found))
    (offa,speca,a),(offb,specb,b)=inputs
    transformed,initial,why=apply_operator(a['coefficients'],a['initial'],op,cert['parameters'])
    D=len(transformed)+len(b['coefficients'])
    if D!=cert['annihilator_product_degree'] or D!=cert['checked_initial_conditions'] or transformed!=cert['transferred_recurrence'] or initial!=sequence(initial,transformed,len(initial)):
        raise ValueError('annihilator witness mismatch')
    if a['coefficients']!=cert['source_recurrence'] or b['coefficients']!=cert['target_recurrence']:
        raise ValueError('formula recurrence witness mismatch')
    source_terms=sequence(a['initial'],a['coefficients'],maximum_source_index(op,cert['parameters'],D+5))
    generated=sequence(initial,transformed,D+5)
    target=sequence(b['initial'],b['coefficients'],D+5)
    if generated!=target:raise ValueError('recurrence identity does not hold')
    for j in range(D+5):
        direct=direct_operator(source_terms,op,cert['parameters'],j)
        if direct!=generated[j] or evaluate(specb,offb+j)!=target[j]:
            raise ValueError('independent exact target evaluator mismatch')
    # Independent evaluator check of source at nontrivial indices, not just the
    # first recurrence order used by infer().
    for j in range(len(source_terms)):
        if j<18 or j>=len(source_terms)-3:
            if evaluate(speca,offa+j)!=source_terms[j]:
                raise ValueError('independent exact source evaluator mismatch')
    return {'candidate_id':candidate_id,'replayed':True,'product_degree':D,
            'independent_controls':5,'formula_scope':'all local n>=0 conditional on formula definitions'}


def replay_all(db):
    counts=Counter();bad=[]
    for (cid,) in db.execute('SELECT candidate_id FROM oeis_formula_transfer_proofs ORDER BY candidate_id'):
        try:replay_certificate(db,cid);counts['passed']+=1
        except (ValueError,TypeError,OverflowError,ZeroDivisionError,ArithmeticError,AssertionError) as exc:
            counts['failed']+=1
            if len(bad)<10:bad.append({'candidate_id':cid,'error':type(exc).__name__+': '+str(exc)[:200]})
    return {'certificate_count':counts['passed']+counts['failed'],
            'replay_passed':counts['passed'],'replay_failed':counts['failed'],
            'errors':bad,'status':'verified' if not counts['failed'] else 'FAIL'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--export',type=Path,required=True)
    p.add_argument('--summary',type=Path)
    p.add_argument('--replay-only',action='store_true')
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        stats=replay_all(db) if args.replay_only else promote(db,export=args.export)
    if args.summary:
        args.summary.parent.mkdir(parents=True,exist_ok=True)
        args.summary.write_text(json.dumps(stats,indent=2,sort_keys=True)+'\n')
    print(json.dumps(stats,indent=2,sort_keys=True))


if __name__=='__main__':main()
