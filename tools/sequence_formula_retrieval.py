"""Lossless, incremental, provenance-aware formula retrieval for OEIS/Komorebi.

Author: Komorebi P.

Every raw OEIS %F/%p/%t/%o formula is indexed as source text; NONE of it is
executed or promoted to a proof merely by appearing in a search result.
The index stores text, typed syntactic leads, verification state, and a receipt
bound to the exact formula content, independent of the transfer-proof system.

This is the retrieval layer to precede expensive symbolic normalization.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3

TAGS={
 'binomial':r'\b(?:binomial|binom|choose)\b|\\binom',
 'pochhammer':r'\b(?:pochhammer|rising.factorial|falling.factorial)\b|\(\s*[^()]{1,20}\s*\)\s*_\s*\{?\s*n\b',
 'hypergeometric':r'\bhypergeometric\b|\b[01234]\s*f\s*[01234]\b|\b_[01234]F_[01234]\b',
 'factorial':r'\b(?:factorial|gamma)\b|(?<![A-Za-z])n\s*!',
 'recurrence':r'\brecurrence\b|\ba\s*\(\s*n\s*[-+]\s*[1-9]',
 'generating_function':r'\b(?:generating.function|g\.f\.|e\.g\.f\.|ogf|egf)\b|\[\s*z\s*\^',
 'convolution':r'\b(?:convolution|cauchy.product|binomial.transform|dirichlet.convolution)\b',
 'multisection':r'\b(?:multisection|polyphase|root.of.unity.filter|residue.class)\b',
 'mobius':r'\b(?:m[oö]bius|m[oö]bius.inversion|dirichlet.inverse)\b',
 'matrix':r'\b(?:matrix|determinant|trace|eigenvalue)\b',
 'sum':r'\b(?:sum|summation)\b|\\sum|Σ',
 'product':r'\b(?:product)\b|\\prod|Π',
 'exact_arithmetic':r'\b(?:exact|integer|rational)\b',
}
COMPILED={name:re.compile(expr,re.IGNORECASE) for name,expr in TAGS.items()}
OEIS_REF=re.compile(r'(?<![A-Za-z0-9])A\d{6}(?!\d)')


def classify(expression):
    """Conservative lexical discovery aids, not proof of a formula's type."""
    return sorted(name for name,pattern in COMPILED.items() if pattern.search(expression))


def ensure_schema(db):
    try:
        db.executescript('''
        CREATE VIRTUAL TABLE IF NOT EXISTS formula_text_fts USING fts5(
          expression, tags, formula_id UNINDEXED, oeis_id UNINDEXED,
          tokenize='unicode61 remove_diacritics 2'
        );
        ''')
    except sqlite3.OperationalError as e:
        raise RuntimeError('SQLite FTS5 is required for scalable formula search') from e
    db.executescript('''
    CREATE TABLE IF NOT EXISTS formula_text_receipts(
        formula_id TEXT PRIMARY KEY, formula_rowid INTEGER NOT NULL UNIQUE,
        text_sha256 TEXT NOT NULL, tags_json TEXT NOT NULL,
        source_oeis_id TEXT, origin TEXT NOT NULL, field TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS formula_text_by_origin ON formula_text_receipts(origin,field);
    CREATE TABLE IF NOT EXISTS formula_text_leads(
        formula_id TEXT NOT NULL, referenced_oeis_id TEXT NOT NULL,
        relation TEXT NOT NULL CHECK(relation='mentioned_in_formula_text'),
        PRIMARY KEY(formula_id,referenced_oeis_id)
    );
    CREATE INDEX IF NOT EXISTS formula_lead_target ON formula_text_leads(referenced_oeis_id);
    ''')


def _fingerprint(kind,expression):
    return hashlib.sha256(json.dumps([kind,expression],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def _prune(db):
    old=db.execute('''SELECT r.formula_id,r.formula_rowid FROM formula_text_receipts r
      LEFT JOIN formulas f ON f.formula_id=r.formula_id
      WHERE f.formula_id IS NULL OR f.rowid!=r.formula_rowid''').fetchall()
    for fid,rowid in old:
        db.execute('DELETE FROM formula_text_fts WHERE rowid=?',(rowid,))
        db.execute('DELETE FROM formula_text_leads WHERE formula_id=?',(fid,))
        db.execute('DELETE FROM formula_text_receipts WHERE formula_id=?',(fid,))
    return len(old)


def index_formulas(db,batch_size=1000):
    """Incremental O(total formula bytes) source index, one row resident at a time."""
    if batch_size<1:raise ValueError('batch_size must be positive')
    ensure_schema(db)
    removed=_prune(db)
    updated=unchanged=inserted=0
    read=db.execute('''SELECT rowid,formula_id,oeis_id,origin,field,kind,expression
        FROM formulas ORDER BY rowid''')
    for rowid,fid,sid,origin,field,kind,expression in read:
        digest=_fingerprint(kind,expression)
        old=db.execute('SELECT formula_rowid,text_sha256 FROM formula_text_receipts WHERE formula_id=?',(fid,)).fetchone()
        if old==(rowid,digest):
            unchanged+=1
        else:
            tags=classify(expression)
            if old:
                db.execute('DELETE FROM formula_text_fts WHERE rowid=?',(old[0],))
                db.execute('DELETE FROM formula_text_leads WHERE formula_id=?',(fid,))
                db.execute('DELETE FROM formula_text_receipts WHERE formula_id=?',(fid,))
                updated+=1
            else:inserted+=1
            db.execute('INSERT INTO formula_text_fts (rowid,expression,tags,formula_id,oeis_id) VALUES (?,?,?,?,?)',
                       (rowid,expression,' '.join(tags),fid,sid))
            db.execute('INSERT INTO formula_text_receipts VALUES (?,?,?,?,?,?,?)',
                       (fid,rowid,digest,json.dumps(tags),sid,origin,field))
            # Lexical mentions are NOT claimed mathematical identities.
            for mentioned in sorted(set(OEIS_REF.findall(expression))-{sid}):
                db.execute('INSERT OR REPLACE INTO formula_text_leads VALUES (?,?,?)',
                           (fid,mentioned,'mentioned_in_formula_text'))
        if (inserted+updated+unchanged)%batch_size==0:db.commit()
    db.commit()
    return {'indexed':db.execute('SELECT count(*) FROM formula_text_receipts').fetchone()[0],
            'inserted':inserted,'updated':updated,'unchanged':unchanged,'removed':removed,
            'unproved_lexical_leads':db.execute('SELECT count(*) FROM formula_text_leads').fetchone()[0],
            'scope':'all raw formula text retained; lexical tags and references are not proofs'}


def search(db,query,limit=20,required_tag=None,verified_only=False):
    if limit<1 or limit>100:raise ValueError('limit out of range')
    if required_tag is not None and required_tag not in TAGS:raise ValueError('unknown tag')
    ensure_schema(db)
    sql='''SELECT f.formula_id,f.oeis_id,f.origin,f.field,f.kind,f.expression,
          f.proof_status,f.verification,f.source_url,r.tags_json,r.text_sha256
        FROM formula_text_fts x
        JOIN formula_text_receipts r ON formula_text_fts.formula_id=r.formula_id
        JOIN formulas f ON f.formula_id=formula_text_fts.formula_id
        WHERE formula_text_fts MATCH ?'''
    # SQLite FTS requires the virtual table's actual identifier, not alias.
    sql=sql.replace('FROM formula_text_fts x','FROM formula_text_fts')
    params=[query]
    if verified_only:
        sql+=" AND f.verification='finite_checked'"
    sql+=' ORDER BY bm25(formula_text_fts) LIMIT ?'
    params.append(max(1,limit*3))
    results=[]
    for fid,sid,origin,field,kind,expr,status,verified,url,tags_raw,digest in db.execute(sql,params):
        if _fingerprint(kind,expr)!=digest:continue
        tags=json.loads(tags_raw)
        if required_tag is not None and required_tag not in tags:continue
        results.append({'formula_id':fid,'oeis_id':sid,'origin':origin,'field':field,
             'kind':kind,'expression':expr[:1500],'tags':tags,'proof_status':status,
             'verification':verified,'source_url':url})
        if len(results)>=limit:break
    return results


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('index')
    q=sub.add_parser('query');q.add_argument('text');q.add_argument('--limit',type=int,default=20)
    q.add_argument('--tag');q.add_argument('--verified-only',action='store_true')
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        if args.command=='index':out=index_formulas(db)
        else:out=search(db,args.text,args.limit,args.tag,args.verified_only)
    print(json.dumps(out,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
