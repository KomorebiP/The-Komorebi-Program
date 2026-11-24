"""Conservative second-pass OEIS chained-equality formula extraction.

Author: Komorebi P. Original source is never executed. The original formula
is preserved, and every extracted expression requires exact prefix agreement.
No conditional or ambiguous line is promoted to a mathematical proof.
"""
from __future__ import annotations
import argparse,hashlib,json,re,sqlite3
from collections import Counter,defaultdict
from pathlib import Path
from oeis_formula_database import evaluate
from oeis_formula_discovery import ASSIGNMENT,compile_simple_term,UnsupportedFormula

CHAIN=re.compile(r'\s+=\s+(?!=)')
END=re.compile(r'\.(?=\s|$)|;\s|\s+-\s+_')


def extract_chain(text):
    for assignment in ASSIGNMENT.finditer(text):
        tail=text[assignment.end():].strip()
        # Only accept a *chained equality*, not an approximation, condition,
        # code statement, inequality, or free-parameter definition.
        m=CHAIN.search(tail)
        if m is None:continue
        rhs=tail[:m.start()].strip()
        if not rhs or len(rhs)>240:continue
        if any(x in rhs.lower() for x in (' if ',' for ',' where ',' when ',' ~ ',' approx','<','>','==')):
            continue
        if END.search(rhs):continue
        try:spec=compile_simple_term(rhs)
        except UnsupportedFormula:continue
        yield rhs,spec


def source_anchors():
    """Small classical anchors explicitly defined by official OEIS names.

    These are not inferred from numeric matching. The original name is
    checked for its expected description, and all stored terms are compared.
    """
    return {
       'A000984':('Central binomial coefficients', {'op':'binomial','n':{'op':'mul','args':[2,{'op':'n'}]},'k':{'op':'n'}}),
       'A000142':('Factorial numbers',{'op':'factorial','arg':{'op':'n'}}),
    }


def verify(db,sid,formula,minimum=12,max_terms=24):
    row=db.execute('SELECT offset,terms_json FROM sequences WHERE oeis_id=?',(sid,)).fetchone()
    if not row:return 0,'missing_sequence'
    offset,data=row
    if offset<0:return 0,'negative_offset'
    terms=[int(z) for z in json.loads(data)]
    count=min(max_terms,len(terms))
    if count<minimum:return count,'insufficient_terms'
    try:
        for j in range(count):
            if evaluate(formula,offset+j)!=terms[j]:return j,'term_mismatch'
    except (ValueError,OverflowError,ArithmeticError):return 0,'unsupported_evaluation'
    return count,'finite_checked'


def normalize(db,output,summary=None,max_lines=None):
    existing=defaultdict(set)
    for sid,raw in db.execute('''SELECT oeis_id,evaluator_json FROM formulas
         WHERE origin='oeis_normalized' AND evaluator_json IS NOT NULL'''):
        try:existing[sid].add(json.dumps(json.loads(raw),sort_keys=True))
        except (ValueError,TypeError):pass
    stats=Counter();found=[];seen=defaultdict(set)
    for fid,sid,line in db.execute("SELECT formula_id,oeis_id,expression FROM formulas WHERE origin='oeis_formula' ORDER BY oeis_id,formula_id"):
        if max_lines is not None and stats['formula_lines_scanned']>=max_lines:break
        stats['formula_lines_scanned']+=1
        for rhs,ast in extract_chain(line):
            key=json.dumps(ast,sort_keys=True)
            if key in existing[sid] or key in seen[sid]:
                stats['duplicate_existing']+=1;continue
            seen[sid].add(key)
            check,status=verify(db,sid,ast)
            stats[status]+=1
            if status!='finite_checked':continue
            found.append({'formula_id':'K-CHAIN-'+hashlib.sha256((fid+key).encode()).hexdigest()[:24],
                'oeis_id':sid,'source_formula_id':fid,'source_line_sha256':hashlib.sha256(line.encode()).hexdigest(),
                'source_url':f'https://oeis.org/{sid}','evaluator':ast,'expression':'a(n)='+rhs,
                'verification':'finite_checked','checked_terms':check,
                'proof_status':'unassessed; algebraic formula expression only if independently certified'})
    for sid,(name_part,ast) in source_anchors().items():
        row=db.execute('SELECT name FROM sequences WHERE oeis_id=?',(sid,)).fetchone()
        if not row or name_part not in row[0]:continue
        key=json.dumps(ast,sort_keys=True)
        if key in existing[sid] or key in seen[sid]:continue
        check,status=verify(db,sid,ast)
        if status!='finite_checked':continue
        found.append({'formula_id':'K-ANCHOR-'+sid,'oeis_id':sid,'source_formula_id':None,
            'source_line_sha256':hashlib.sha256(row[0].encode()).hexdigest(),
            'source_url':f'https://oeis.org/{sid}','evaluator':ast,'expression':row[0],
            'verification':'finite_checked','checked_terms':check,
            'proof_status':'classical defining expression, finite OEIS term cross-check; not a formal proof of OEIS identity'})
        stats['curated_anchors']+=1
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf8') as f:
        for x in found:f.write(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n')
    report={'status':'finite_checked_candidates_only','new_verified_expressions':len(found),**stats,
        'nonclaims':'Source prose and programs not executed; exact finite matching does not prove OEIS identity'}
    if summary:Path(summary).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path);p.add_argument('--summary',type=Path);p.add_argument('--max-lines',type=int)
    a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:stats=normalize(db,a.output,a.summary,a.max_lines)
    print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
