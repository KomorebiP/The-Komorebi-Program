"""Prove multi-input OEIS formula-expression hyperedges via exact normal forms.

Author: Komorebi P. OEIS identification remains finite checked. Source text is
never executed. Distinct from finite observations: these certificates compare
exact Q-coefficients of complete exponential-polynomial expressions for all n.
"""
from __future__ import annotations
import ast,argparse,hashlib,json,sqlite3
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from sequence_oeis_formula_dependencies import safe_parse,IDENTIFIER,UnsupportedFormula,OEIS_ID,eval_arithmetic
from sequence_oeis_symbolic_network import load_formulas,phase,formal_eval
from sequence_linear_identity_compiler import key,scaled
from sequence_exponential_polynomial import ep_add,ep_mul,ep_power


def scalar(expr):
    if not expr:return Q(0)
    if len(expr)==1 and 1 in expr and len(expr[1])==1:return Q(expr[1][0])
    raise UnsupportedFormula('requires non-constant symbolic quotient')


def affine(node,offset):
    """Index expression as m*t+r, t=n-target_offset, with integral m,r."""
    if isinstance(node,ast.Constant) and type(node.value) is int:return 0,int(node.value)
    if isinstance(node,ast.Name) and node.id=='n':return 1,offset
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
        m,r=affine(node.operand,offset);return (-m,-r) if isinstance(node.op,ast.USub) else (m,r)
    if isinstance(node,ast.BinOp):
        if isinstance(node.op,(ast.Add,ast.Sub)):
            m,r=affine(node.left,offset);p,q=affine(node.right,offset)
            return (m+p,r+q) if isinstance(node.op,ast.Add) else (m-p,r-q)
        if isinstance(node.op,ast.Mult):
            m,r=affine(node.left,offset);p,q=affine(node.right,offset)
            if m and p:raise UnsupportedFormula('non-affine index')
            return m*q+p*r,r*q
        if isinstance(node.op,(ast.Div,ast.FloorDiv)):
            m,r=affine(node.left,offset);p,q=affine(node.right,offset)
            if p or not q or m%q or r%q:raise UnsupportedFormula('fractional index')
            return m//q,r//q
    raise UnsupportedFormula('index is not an exact affine map')


def symbolic(node,offset,records):
    if isinstance(node,ast.Expression):return symbolic(node.body,offset,records)
    if isinstance(node,ast.Constant) and type(node.value) is int:return {} if node.value==0 else {1:[Q(node.value)]}
    if isinstance(node,ast.Name) and node.id=='n':return {1:[Q(offset),Q(1)]}
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and IDENTIFIER.fullmatch(node.func.id) and not node.keywords and len(node.args)==1:
        sid=node.func.id
        if sid not in records:raise UnsupportedFormula('source has no independently extracted exact formula')
        rec=records[sid];m,r=affine(node.args[0],offset)
        if m<0:raise UnsupportedFormula('negative slope eventually leaves source domain')
        k=r-rec['offset']
        if k<0:raise UnsupportedFormula('source mathematical index underflows')
        return ({1:[formal_eval(rec['expression'],k)]} if m==0 else phase(rec['expression'],m,k))
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
        exp=symbolic(node.operand,offset,records)
        return exp if isinstance(node.op,ast.UAdd) else scaled(exp,-1)
    if isinstance(node,ast.BinOp):
        if isinstance(node.op,ast.Pow):
            if isinstance(node.right,ast.Constant) and type(node.right.value) is int and 0<=node.right.value<=5:
                return ep_power(symbolic(node.left,offset,records),node.right.value)
            # Handle a nonzero constant base to an affine exponent, e.g. 2^n.
            if isinstance(node.left,ast.Constant) and type(node.left.value) is int and node.left.value!=0:
                m,r=affine(node.right,offset)
                if m<0 or abs(m)>16 or abs(r)>128:raise UnsupportedFormula('unsafe exponential rate')
                b=node.left.value
                return {b**m:[Q(b)**r]}
            raise UnsupportedFormula('unsupported symbolic power')
        a=symbolic(node.left,offset,records);b=symbolic(node.right,offset,records)
        if isinstance(node.op,ast.Add):return ep_add(a,b)
        if isinstance(node.op,ast.Sub):return ep_add(a,scaled(b,-1))
        if isinstance(node.op,ast.Mult):return ep_mul(a,b)
        if isinstance(node.op,ast.Div):
            denominator=scalar(b)
            if denominator==0:raise UnsupportedFormula('division by zero')
            return scaled(a,Q(1)/denominator)
        if isinstance(node.op,ast.FloorDiv):raise UnsupportedFormula('floor division requires independent integrality argument')
    raise UnsupportedFormula('syntax not in symbolic expression calculus')


def prove(db,source:Path,output:Path,summary:Path|None=None):
    records,conflicts=load_formulas(db)
    counts=Counter();certificates=[]
    with Path(source).open(encoding='utf-8') as stream:
        for raw in stream:
            x=json.loads(raw)
            if x['status']!='finite_checked_formula_hyperedge':continue
            counts['finitely_checked_candidates']+=1
            target=x['oeis_id']
            if target not in records:counts['missing_target_normal_form']+=1;continue
            if any(s not in records for s in x['references']):counts['missing_input_normal_form']+=1;continue
            expr=x['candidate_rhs']
            if not expr:continue
            tree=safe_parse(expr)
            if tree is None:continue
            try:
                result=symbolic(tree,records[target]['offset'],records)
                if key(result)!=records[target]['key']:
                    counts['symbolic_inequality']+=1;continue
                # Guard against mistakes in conversion through further exact rational evaluations.
                for n in [0,1,2,5,11,25]:
                    if formal_eval(result,n)!=formal_eval(records[target]['expression'],n):
                        raise AssertionError('computed symbolic forms disagree')
            except (UnsupportedFormula,ValueError,TypeError,OverflowError):
                counts['unsupported_exact_form']+=1;continue
            certificates.append({'formula_id':x['formula_id'],'oeis_id':target,'input_sequences':x['references'],
                'source_text_sha256':x['source_text_sha256'],
                'target_source_sha256':records[target]['record_sha256'],
                'input_source_sha256':{i:records[i]['record_sha256'] for i in x['references']},
                'rhs':expr,'proof_method':'Exact canonical exponential-polynomial coefficient equality in Q for all local n>=0',
                'oeis_identification':'Finite OEIS prefix agreement only; not independent all-index OEIS identification',
                'reference_terms_checked':x['checked_terms']})
            counts['proved_formula_hyperedges']+=1
            if len(x['references'])>1:counts['proved_multi_input_hyperedges']+=1
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',encoding='utf8') as f:
        for c in certificates:f.write(json.dumps(c,ensure_ascii=False,separators=(',',':'))+'\n')
    stats={'status':'conditional_on_exact_extracted_formula_definitions',**counts,
        'all_index_oeis_identification_proved':0,
        'input_formula_sequences_with_exact_models':len(records),
        'scope':'proof of formulas, not proof of OEIS sequence identity'}
    if summary:
        p=Path(summary);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(stats,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return stats


def replay(db,ledger:Path):
    """Independent source-receipt and symbolic replay of every retained hyperedge."""
    records,conflicts=load_formulas(db)
    counts=Counter();failures=[]
    for raw in Path(ledger).read_text(encoding='utf8').splitlines():
        if not raw.strip():continue
        c=json.loads(raw)
        counts['attempted']+=1
        try:
            target=c['oeis_id'];refs=c['input_sequences']
            if target not in records or any(r not in records for r in refs):raise ValueError('missing normalized formula')
            t=records[target]
            if t['record_sha256']!=c['target_source_sha256']:raise ValueError('stale target source record')
            if any(records[r]['record_sha256']!=c['input_source_sha256'][r] for r in refs):raise ValueError('stale input source record')
            row=db.execute("SELECT expression,oeis_id FROM formulas WHERE formula_id=? AND origin='oeis_formula'",(c['formula_id'],)).fetchone()
            if not row or row[1]!=target:raise ValueError('missing or changed source formula')
            if hashlib.sha256(row[0].encode()).hexdigest()!=c['source_text_sha256']:raise ValueError('stale raw formula receipt')
            if sorted(set(OEIS_ID.findall(row[0])))!=sorted(refs):raise ValueError('changed referenced IDs')
            tree=safe_parse(c['rhs'])
            if not tree:raise ValueError('unrecognized formula expression')
            lhs=symbolic(tree,t['offset'],records)
            if key(lhs)!=t['key']:raise ValueError('symbolic identity failed')
            for n in [0,1,2,3,7,13,29]:
                if formal_eval(lhs,n)!=formal_eval(t['expression'],n):raise ValueError('symbolic value witness mismatch')
            counts['passed']+=1
        except (ValueError,TypeError,KeyError,UnsupportedFormula,ArithmeticError) as exc:
            counts['failed']+=1
            if len(failures)<12:failures.append({'formula_id':c.get('formula_id'), 'error':str(exc)})
    return {'status':'passed' if counts['failed']==0 else 'failed',**counts,'failure_samples':failures,
            'scope':'Exact all-index identities between independently extracted formula expressions; not global OEIS identification'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True);p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=False)
    p.add_argument('--replay-only',action='store_true')
    a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:
        result=replay(db,a.output) if a.replay_only else prove(db,a.source,a.output,a.summary)
    print(json.dumps(result,indent=2))
    if a.replay_only and result['status']!='passed':raise SystemExit(1)
if __name__=='__main__':main()
