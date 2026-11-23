"""Extract attributed OEIS formula references as candidate hyperedges, not proofs.

Author: Komorebi P. Stored OEIS formula text is never executed. A restricted,
explicitly whitelisted Python AST accepts arithmetic of n and Axxxxxx(n+shift).
All numerical observations are finite checks and are reported as such.
"""
from __future__ import annotations
import argparse,ast,hashlib,json,re,sqlite3
from collections import Counter
from fractions import Fraction
from pathlib import Path

OEIS_ID = re.compile(r'\bA\d{6}\b')
ASSIGNMENT = re.compile(r'^\s*a\s*\(\s*n\s*\)\s*=\s*(.+)$',re.IGNORECASE)
IDENTIFIER = re.compile(r'^A\d{6}$')

class UnsupportedFormula(Exception):pass
class MissingTerm(Exception):pass


def rhs(text):
    m=ASSIGNMENT.match(text)
    if not m:return None
    s=m.group(1).strip()
    for marker in [' - _',' [From ', ' [Proof ', '  [', ' (see ', ' (for ', ' ; ']:
        if marker in s:s=s.split(marker,1)[0].strip()
    s=s.rstrip(' .;')
    if '=' in s or '\n' in s or len(s)>300:return None
    # OEIS uses '^' exponentiation, not Python's bitwise XOR; parse but do not eval.
    return s.replace('^','**')


def _check_value(x):
    if x.denominator.bit_length()>100000 or x.numerator.bit_length()>100000:raise UnsupportedFormula('excessive integer size')
    return x


def eval_arithmetic(node,n,lookup):
    if isinstance(node,ast.Expression):return eval_arithmetic(node.body,n,lookup)
    if isinstance(node,ast.Constant) and isinstance(node.value,int) and not isinstance(node.value,bool):
        return Fraction(node.value)
    if isinstance(node,ast.Name) and node.id=='n':return Fraction(n)
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
        a=eval_arithmetic(node.operand,n,lookup)
        return -a if isinstance(node.op,ast.USub) else a
    if isinstance(node,ast.BinOp):
        if not isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Div,ast.FloorDiv,ast.Pow)):
            raise UnsupportedFormula('unsupported binary operator')
        a=eval_arithmetic(node.left,n,lookup)
        b=eval_arithmetic(node.right,n,lookup)
        if isinstance(node.op,ast.Add):return _check_value(a+b)
        if isinstance(node.op,ast.Sub):return _check_value(a-b)
        if isinstance(node.op,ast.Mult):return _check_value(a*b)
        if isinstance(node.op,ast.Div):
            if not b:raise UnsupportedFormula('zero divisor')
            return _check_value(a/b)
        if isinstance(node.op,ast.FloorDiv):
            if not b:raise UnsupportedFormula('zero divisor')
            return Fraction(a//b)
        if b.denominator!=1 or abs(b.numerator)>16:raise UnsupportedFormula('unsafe exponent')
        if a==0 and b.numerator<0:raise UnsupportedFormula('zero negative power')
        return _check_value(a**int(b))
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and IDENTIFIER.fullmatch(node.func.id) and not node.keywords and len(node.args)==1:
        k=eval_arithmetic(node.args[0],n,lookup)
        if k.denominator!=1 or abs(k.numerator)>1000000:raise UnsupportedFormula('non-integral or unbounded index')
        return Fraction(lookup(node.func.id,int(k)))
    raise UnsupportedFormula('unsupported operation or potential code')


def safe_parse(source):
    try:
        tree=ast.parse(source,mode='eval')
        # Reject unsupported operations BEFORE accepting a parsed formula.
        # Operator nodes themselves are traversed as children of their parent.
        def shape(node):
            if isinstance(node,ast.Expression):return shape(node.body)
            if isinstance(node,ast.Constant) and isinstance(node.value,int) and not isinstance(node.value,bool):return
            if isinstance(node,ast.Name) and node.id=='n':return
            if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
                return shape(node.operand)
            if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Div,ast.FloorDiv,ast.Pow)):
                shape(node.left);shape(node.right);return
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and IDENTIFIER.fullmatch(node.func.id) and not node.keywords and len(node.args)==1:
                return shape(node.args[0])
            raise UnsupportedFormula('AST syntax not in allowlist')
        if sum(1 for _ in ast.walk(tree))>90:raise UnsupportedFormula('AST too complex')
        shape(tree)
        return tree
    except (SyntaxError,RecursionError,UnsupportedFormula):return None


def extract(db,output:Path|None=None,summary:Path|None=None,minimum=12,holdout=8):
    if minimum<1 or holdout<1:raise ValueError('positive verification windows required')
    library={a:(off,[int(x) for x in json.loads(terms)]) for a,off,terms in db.execute('SELECT oeis_id,offset,terms_json FROM sequences')}
    found=Counter();out=[]
    for formula_id,source,text in db.execute("SELECT formula_id,oeis_id,expression FROM formulas WHERE origin='oeis_formula' ORDER BY formula_id"):
        matches=sorted(set(OEIS_ID.findall(text or '')))
        if not matches:continue
        found['source_formula_lines']+=1
        found['reference_occurrences']+=len(OEIS_ID.findall(text))
        resolved=[x for x in matches if x in library]
        found['references_in_import']+=len(resolved)
        expression=rhs(text or '')
        tree=safe_parse(expression) if expression else None
        status='textual_dependency_unverified';checked=0;failure=None;has_all=bool(len(matches)==len(resolved))
        if tree:
            # Keep references inside RHS, not just in arbitrary appended prose.
            rhs_refs=set(OEIS_ID.findall(expression))
            calls={x.func.id for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and IDENTIFIER.fullmatch(x.func.id)}
            if rhs_refs==calls and calls:
                found['strict_ast_parsed']+=1
                if has_all and source in library:
                    off,values=library[source]
                    try:
                        def lookup(sid,k):
                            s_off,terms=library[sid]
                            if k<s_off or k>=s_off+len(terms):raise MissingTerm(sid)
                            return terms[k-s_off]
                        for ix,expected in enumerate(values):
                            n=ix+off
                            v=eval_arithmetic(tree,n,lookup)
                            if v!=expected:
                                failure={'index':n,'expected':str(expected),'actual':str(v)};break
                            checked+=1
                    except MissingTerm:pass
                    except (UnsupportedFormula,ZeroDivisionError,OverflowError):
                        failure={'error':'operator evaluation unsupported'}
                    if not failure and checked>=minimum+holdout:
                        status='finite_checked_formula_hyperedge';found['finite_checked_lines']+=1
                        found['finite_checked_terms']+=checked
                    else:
                        status='parsed_but_unverified';found['parsed_but_unverified']+=1
                        if failure:found['rejected_examples']+=1
                else:status='parsed_but_out_of_corpus';found['parsed_out_of_corpus']+=1
        if len(matches)>1:found['multi_input_lines']+=1
        if status=='textual_dependency_unverified':found['textual_only_lines']+=1
        out.append({'formula_id':formula_id,'oeis_id':source,'references':matches,
                    'references_in_corpus':resolved,'source_field':'%F','source_text_sha256':hashlib.sha256((text or '').encode()).hexdigest(),
                    'candidate_rhs':expression if tree else None,'status':status,'checked_terms':checked,'first_failure':failure,
                    'scope':'textual or finite source evidence only; not an all-index OEIS identity'})
    if output:
        output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('w',encoding='utf8') as f:
            for row in out:f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
    stats=dict(found,oeis_source_records=len(library),lines=len(out),unique_sources=len({x['oeis_id'] for x in out}),
               unique_references=len({ref for x in out for ref in x['references']}),
               high_value_status='strict finite checks never establish global OEIS formula equality')
    if summary:
        p=Path(summary);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(stats,sort_keys=True,indent=2)+'\n',encoding='utf8')
    return stats


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--summary',required=True,type=Path)
    p.add_argument('--min-terms',type=int,default=12)
    p.add_argument('--holdout',type=int,default=8)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        print(json.dumps(extract(db,args.output,args.summary,args.min_terms,args.holdout),sort_keys=True,indent=2))

if __name__=='__main__':main()
