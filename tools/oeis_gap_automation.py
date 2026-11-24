#!/usr/bin/env python3
"""Offline, source-bound OEIS formula acquisition and transfer gap discovery.

Author: Komorebi P.

This tool NEVER executes OEIS-supplied formula text. A rational-function proof
concerns parsed expressions over Q(n), not the identity of a named OEIS entry.
The input network's existing proofs are reused with their original scope.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
from math import factorial
from pathlib import Path
import re
import sqlite3
import sys
from typing import Iterable
import csv

ID = re.compile(r"A\d{6}\Z")
REF = re.compile(r"(?<![A-Za-z0-9])A\d{6}(?![A-Za-z0-9])")
SEQ_LINE = re.compile(r"^%([A-Z])\s+(A\d{6})\s*(.*)$")
TERM = re.compile(r"^\s*a\s*\(\s*n\s*\)\s*=\s*(.+)$", re.I)
VALID_EVIDENCE = {
    "all_index_formula_identity", "all_index_formula_identity_on_tail",
    "conditional_exact_ogf_identity", "exact_quadratic_algebra",
}
KINDS = ("hyperedge", "gauge", "riordan", "quadratic")
KIND_SCORE = {
    "term_candidate": 5, "generating_function": 5,
    "recurrence": 4, "finite_or_infinite_sum": 3,
    "product_candidate": 2, "unclassified": 1,
}
SCHEMA_VERSION = 1
MAX_FORMULA = 20000


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_csv_cell(value: object) -> object:
    """Neutralize spreadsheet formula interpretation in untrusted source text."""
    if isinstance(value, str) and value.lstrip(' \t\r\n').startswith(('=', '+', '-', '@')):
        return '\'' + value
    return value


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def classify(s: str) -> str:
    t = s.lower()
    if "g.f." in t or "generating function" in t or "generating series" in t:
        return "generating_function"
    if any(x in t for x in ("recurrence", "a(n-1)", "a(n-2)")):
        return "recurrence"
    if t.lstrip().startswith("a(n)") or t.lstrip().startswith("a(n "):
        return "term_candidate"
    if any(x in t for x in ("sum_{", "sum(", "sum ")):
        return "finite_or_infinite_sum"
    if any(x in t for x in ("prod_", "product_", "product ")):
        return "product_candidate"
    return "unclassified"


def load_network(path: Path) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    if d.get("schema") != 1 or d.get("oeis", {}).get("license") != "CC-BY-SA-4.0":
        raise ValueError("Unrecognized network schema or missing OEIS license")
    ids = [r["id"] for r in d["records"]]
    if len(set(ids)) != len(ids) or any(not ID.fullmatch(i) for i in ids):
        raise ValueError("Duplicate or malformed network sequence IDs")
    counts, keys = Counter(), set()
    for row in d["edges"]:
        if row.get("evidence") not in VALID_EVIDENCE or row.get("kind") not in KINDS:
            raise ValueError("Unexpected network evidence or transfer kind")
        if row["key"] in keys:
            raise ValueError("Duplicate transfer edge key")
        keys.add(row["key"])
        if row["target"] not in ids or not row.get("inputs") or any(i not in ids for i in row["inputs"]):
            raise ValueError("Network edge has missing endpoint")
        counts[row["kind"]] += 1
    if dict(counts) != d.get("counts"):
        raise ValueError("Network declared counts do not match content")
    return d


def components(network: dict) -> tuple[dict[str, int], list[list[str]]]:
    parent = {r["id"]: r["id"] for r in network["records"]}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        a, b = find(x), find(y)
        if a != b:
            parent[max(a, b)] = min(a, b)

    for e in network["edges"]:
        for i in e["inputs"]:
            union(e["target"], i)
    buckets: dict[str, list[str]] = defaultdict(list)
    for k in parent:
        buckets[find(k)].append(k)
    groups = sorted((sorted(v) for v in buckets.values()), key=lambda v: (-len(v), v[0]))
    cid = {id_: i for i, g in enumerate(groups) for id_ in g}
    return cid, groups


def parse_seq_file(path: Path) -> dict:
    """Parse OEIS internal % fields, retaining source lines and offset verbatim."""
    found: dict[str, object] = {"formulas": [], "crossrefs": []}
    ident = None
    for lineno, text in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        m = SEQ_LINE.match(text)
        if not m:
            continue
        field, sid, val = m.groups()
        if ident is None:
            ident = sid
        if ident != sid:
            raise ValueError(f"Mixed sequence IDs in {path}:{lineno}")
        if field == "F":
            found["formulas"].append({"kind": classify(val), "text": val, "line": lineno, "field": "F"})
        elif field == "Y":
            found["crossrefs"].append({"text": val, "line": lineno, "field": "Y"})
        elif field in ("N", "O"):
            if field == "N" and "name" not in found:
                found["name"] = val
            if field == "O" and "offset_raw" not in found:
                found["offset_raw"] = val
    if ident is None:
        raise ValueError(f"No OEIS sequence ID in {path}")
    if not ID.fullmatch(ident) or path.name != f"{ident}.seq":
        raise ValueError(f"Unexpected source filename/sequence: {path}, {ident}")
    found["id"] = ident
    return found


def ingest(oeis_dir: Path, db_path: Path, revision: str, limit: int | None = None) -> dict:
    """Idempotent incremental ingestion from a local oeis/oeisdata clone.

    No automatic network calls, no Git LFS checkout, no interpretation of formula code.
    Entries missing from a partial input are never deleted.
    """
    files = sorted(oeis_dir.glob("seq/A[0-9][0-9][0-9]/A[0-9][0-9][0-9][0-9][0-9][0-9].seq"))
    if limit is not None:
        files = files[:limit]
    if not files:
        raise ValueError("No .seq files found under <oeis_dir>/seq/Axxx/Axxxxxx.seq")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db_path))
    try:
        con.executescript("""
          CREATE TABLE IF NOT EXISTS source_entries (
            oeis_id TEXT PRIMARY KEY, source_sha256 TEXT NOT NULL, revision TEXT NOT NULL,
            relative_path TEXT NOT NULL, name TEXT, offset_raw TEXT
          );
          CREATE TABLE IF NOT EXISTS source_fields (
            oeis_id TEXT NOT NULL, line INTEGER NOT NULL, field TEXT NOT NULL,
            kind TEXT NOT NULL, text TEXT NOT NULL,
            PRIMARY KEY (oeis_id, line)
          );
          CREATE INDEX IF NOT EXISTS source_fields_id ON source_fields(oeis_id);
        """)
        changed = 0
        formula_lines = 0
        for f in files:
            raw = f.read_bytes()
            sha = digest_bytes(raw)
            id_ = f.stem
            stored = con.execute("SELECT source_sha256 FROM source_entries WHERE oeis_id=?", (id_,)).fetchone()
            if stored and stored[0] == sha:
                continue
            obj = parse_seq_file(f)
            relative = f.relative_to(oeis_dir).as_posix()
            with con:
                con.execute("DELETE FROM source_fields WHERE oeis_id=?", (id_,))
                con.executemany("INSERT INTO source_fields VALUES(?,?,?,?,?)", [
                    (id_, row["line"], row["field"], row.get("kind", "cross_reference"), row["text"])
                    for row in (obj["formulas"] + obj["crossrefs"])
                ])
                con.execute("REPLACE INTO source_entries VALUES (?,?,?,?,?,?)", (
                    id_, sha, revision, relative, obj.get("name"), obj.get("offset_raw")))
            changed += 1
            formula_lines += len(obj["formulas"])
    finally:
        con.close()
    return {"files_seen": len(files), "entries_changed": changed,
            "formula_lines_changed": formula_lines, "db": str(db_path),
            "source_revision": revision, "status": "source_text_only"}


def formula_rows(source_manifest: Path | None, source_db: Path | None) -> Iterable[dict]:
    if source_db:
        con = sqlite3.connect(f"file:{source_db}?mode=ro", uri=True)
        try:
            for row in con.execute("SELECT oeis_id,field,kind,text,line FROM source_fields ORDER BY oeis_id,line"):
                id_, field, kind, expression, line = row
                yield dict(source=id_, field=field, kind=kind, text=expression, source_line=line)
        finally:
            con.close()
    elif source_manifest:
        data = json.loads(source_manifest.read_text(encoding="utf-8"))
        if data.get("schema") != 1 or data.get("evidence") != "unreviewed_source_text" or data.get("license") != "CC-BY-SA-4.0":
            raise ValueError("Formula manifest has unexpected source evidence or license")
        for ident, obj in sorted(data["entries"].items()):
            if not ID.fullmatch(ident) or obj.get("source") != f"https://oeis.org/{ident}":
                raise ValueError(f"Invalid OEIS attribution for {ident}")
            for i, row in enumerate(obj["formulas"]):
                yield dict(source=ident, field="F", kind=row["kind"], text=row["text"], source_line=i+1)
    else:
        raise ValueError("Provide --formulas or --source-db")


# Exact rational-function algebra over Q(n), implemented without eval/sympy.
# A polynomial is a tuple of rational coefficients in ascending degree order.
def trim(p: Iterable[Q]) -> tuple[Q, ...]:
    result = list(p)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result) or (Q(0),)


def add(a: tuple[Q, ...], b: tuple[Q, ...]) -> tuple[Q, ...]:
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])


def mul(a: tuple[Q, ...], b: tuple[Q, ...]) -> tuple[Q, ...]:
    r = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i+j] += x*y
    return trim(r)


def neg(a: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(-x for x in a)


def divmod_poly(a: tuple[Q, ...], b: tuple[Q, ...]) -> tuple[tuple[Q, ...], tuple[Q, ...]]:
    if b == (0,):
        raise ZeroDivisionError("Polynomial division by zero")
    r = list(trim(a)); q = [Q(0)] * max(1, len(a)-len(b)+1)
    while len(r) >= len(b) and any(r):
        shift = len(r)-len(b); scale = r[-1]/b[-1]; q[shift] += scale
        for i, bi in enumerate(b):
            r[shift+i] -= scale*bi
        r = list(trim(r))
    return trim(q), trim(r)


def pgcd(a: tuple[Q, ...], b: tuple[Q, ...]) -> tuple[Q, ...]:
    while b != (0,):
        _, r = divmod_poly(a,b); a,b=b,r
    if a == (0,):
        return (Q(1),)
    return tuple(x/a[-1] for x in a)


@dataclass(frozen=True)
class Rational:
    num: tuple[Q, ...]
    den: tuple[Q, ...]

    def __post_init__(self) -> None:
        if self.den == (0,):
            raise ZeroDivisionError("Zero rational denominator")
        if max(len(self.num),len(self.den)) > 35:
            raise ValueError("Degree cap exceeded")

    @staticmethod
    def constant(x: Q) -> 'Rational':
        return Rational((Q(x),), (Q(1),))

    def plus(self, other: 'Rational') -> 'Rational':
        return Rational(add(mul(self.num,other.den),mul(other.num,self.den)),mul(self.den,other.den)).reduce()

    def minus(self, other: 'Rational') -> 'Rational':
        return self.plus(Rational(neg(other.num),other.den))

    def times(self, other: 'Rational') -> 'Rational':
        return Rational(mul(self.num,other.num),mul(self.den,other.den)).reduce()

    def over(self, other: 'Rational') -> 'Rational':
        if other.num == (0,):
            raise ZeroDivisionError("Division by formal zero")
        return Rational(mul(self.num,other.den),mul(self.den,other.num)).reduce()

    def power(self, n: int) -> 'Rational':
        if not isinstance(n,int) or abs(n)>16:
            raise ValueError("Unsupported exponent")
        if n<0:
            return Rational.constant(Q(1)).over(self.power(-n))
        out = Rational.constant(Q(1))
        for _ in range(n):
            out=out.times(self)
        return out

    def reduce(self) -> 'Rational':
        if self.num == (0,):
            return Rational((Q(0),),(Q(1),))
        g=pgcd(trim(self.num),trim(self.den))
        n,r=divmod_poly(self.num,g)
        d,s=divmod_poly(self.den,g)
        assert r == (0,) and s == (0,)
        scale=d[-1]
        return Rational(trim(x/scale for x in n),trim(x/scale for x in d))

    def is_zero(self) -> bool:
        return self.num == (0,)

    def expr_data(self) -> dict:
        return {"num": [[x.numerator,x.denominator] for x in self.num],
                "den": [[x.numerator,x.denominator] for x in self.den]}


def parse_safe_rhs(source: str) -> Rational:
    if len(source)>400:
        raise ValueError("Formula exceeds small exact parser budget")
    source=source.replace("^", "**")
    tree=ast.parse(source,mode="eval")
    budget=[0]

    def rec(node: ast.AST, depth: int = 0) -> Rational:
        budget[0] += 1
        if depth>35 or budget[0]>100:
            raise ValueError("Formula exceeds AST limits")
        if isinstance(node, ast.Constant) and type(node.value) is int and len(str(node.value))<=40:
            return Rational.constant(Q(node.value))
        if isinstance(node, ast.Name) and node.id=="n":
            return Rational((Q(0),Q(1)),(Q(1),))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            return rec(node.operand,depth+1)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return Rational.constant(Q(-1)).times(rec(node.operand,depth+1))
        if isinstance(node, ast.BinOp):
            if isinstance(node.op,ast.Pow):
                if not isinstance(node.right,ast.Constant) or type(node.right.value) is not int:
                    raise ValueError("Non-literal exponent")
                return rec(node.left,depth+1).power(node.right.value)
            x=rec(node.left,depth+1); y=rec(node.right,depth+1)
            if isinstance(node.op,ast.Add):return x.plus(y)
            if isinstance(node.op,ast.Sub):return x.minus(y)
            if isinstance(node.op,ast.Mult):return x.times(y)
            if isinstance(node.op,ast.Div):return x.over(y)
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in ("binomial","binom") and len(node.args)==2 and not node.keywords:
            top=rec(node.args[0],depth+1)
            k=node.args[1]
            if not isinstance(k,ast.Constant) or type(k.value) is not int or not 0<=k.value<=12:
                raise ValueError("Only binomial(polynomial, fixed nonnegative integer) supported")
            out=Rational.constant(Q(1))
            for i in range(k.value):out=out.times(top.minus(Rational.constant(Q(i))))
            return out.over(Rational.constant(Q(factorial(k.value))))
        raise ValueError("Unsupported or unsafe OEIS formula syntax")

    return rec(tree.body).reduce()


def parse_term_formula(text: str) -> tuple[Rational,str]:
    m=TERM.match(text)
    if not m:
        raise ValueError("Not a stand-alone a(n) expression")
    rhs=m.group(1).strip()
    rhs=rhs.split(" - _",1)[0].split(";",1)[0].strip().rstrip(".").strip()
    # An annotation like 'n>=1' is not an algebraic operation. Reject, do not discard.
    return parse_safe_rhs(rhs), rhs


def affine_certificate(target: Rational, source: Rational) -> dict | None:
    """Prove T(n) = c*S(n) + b*n + a over Q(n), if nontrivial and small."""
    if target.den != (1,) or source.den != (1,):
        return None
    dt, ds = len(target.num)-1, len(source.num)-1
    if dt < 2 or ds != dt:
        return None
    c=target.num[-1]/source.num[-1]
    if c == 0 or abs(c.numerator)>12 or c.denominator>12:
        return None
    residual=target.minus(source.times(Rational.constant(c))).reduce()
    if residual.den != (1,) or len(residual.num)>2:
        return None
    a=residual.num[0]; b=residual.num[1] if len(residual.num)>1 else Q(0)
    if max(abs(a.numerator),abs(b.numerator),a.denominator,b.denominator)>24:
        return None
    if c==1 and a==0 and b==0:
        return None
    assert target.minus(source.times(Rational.constant(c))).minus(Rational((a,b),(Q(1),))).is_zero()
    return {"c":str(c),"b":str(b),"a":str(a),"identity":"target(n) = c*source(n) + b*n + a",
            "proof":"exact polynomial rational arithmetic over Q[n]",
            "oeis_identification":"unverified premise"}


def scanner(network: dict, rows: Iterable[dict], *, limit: int | None = None) -> dict:
    cid, groups = components(network)
    all_ids = set(cid)
    store: dict[tuple[str,str],dict] = {}
    rational_forms: dict[str, list[tuple[Rational,str,int]]] = defaultdict(list)
    obs_count=0; formula_count=0; parse_attempts=0; parse_success=0
    kind_counts=Counter()
    for row in rows:
        if limit is not None and formula_count>=limit:
            break
        src, field, text = row['source'], row['field'], row['text']
        if not ID.fullmatch(src) or not isinstance(text,str) or len(text)>MAX_FORMULA:
            continue
        formula_count += 1
        kind=row.get('kind') or classify(text)
        kind_counts[kind]+=1
        refs=set(REF.findall(text))-{src}
        if src not in all_ids and not any(t in all_ids for t in refs):
            continue  # Keep full-corpus memory tied to the curated network frontier.
        for target in sorted(refs):
            key=(src,target)
            entry=store.setdefault(key,{"from":src,"to":target,"source_fields":set(),
                                        "formula_kinds":set(),"sample":"","line":row.get('source_line'),
                                        "mentions":0,"field_types":set()})
            entry["mentions"]+=1
            entry['formula_kinds'].add(kind)
            entry['field_types'].add(field)
            if not entry['sample'] or (field=='F' and 'F' not in entry['source_fields']):
                entry['sample']=text[:360];entry['line']=row.get('source_line')
            entry['source_fields'].add(field)
            obs_count+=1
        if field=='F' and src in all_ids and kind=='term_candidate':
            parse_attempts+=1
            try:
                rational, rhs=parse_term_formula(text)
            except (ValueError, SyntaxError, TypeError, RecursionError, ZeroDivisionError, OverflowError):
                continue
            parse_success+=1
            if len(rational_forms[src])<4:
                rational_forms[src].append((rational,rhs,row.get('source_line',0)))

    # Lexical cross-references never acquire stronger mathematical status.
    queues={'cross_component':[],'new_id_frontier':[],'in_component':[],'outside_to_network':[]}
    rational_candidates=[]
    for ent in store.values():
        s,t=ent['from'],ent['to']
        if s in cid and t in cid:
            bucket='cross_component' if cid[s]!=cid[t] else 'in_component'
        elif s in cid and t not in cid:
            bucket='new_id_frontier'
        elif s not in cid and t in cid:
            bucket='outside_to_network'
        else:
            continue
        kind_strength=max((KIND_SCORE.get(k,1) for k in ent['formula_kinds']),default=1)
        expression_bonus=2 if 'F' in ent['field_types'] else 0
        source_size=len(groups[cid[s]]) if s in cid else 0
        target_size=len(groups[cid[t]]) if t in cid else 0
        # Heuristic only. Does not imply a bridge mathematically exists.
        score=2*kind_strength+expression_bonus+min(ent['mentions'],5)
        if bucket=='cross_component':
            score+=6+min(source_size,target_size,20)//5
        if bucket=='new_id_frontier':
            score+=4
        output={"from":s,"to":t,"priority_score":score,"mentions":ent['mentions'],
                "formula_kinds":sorted(ent['formula_kinds']),"fields":sorted(ent['field_types']),
                "source_line":ent['line'],"source_excerpt":ent['sample'],
                "source_component":cid.get(s),"target_component":cid.get(t),
                "triage_status":"lexical_lead_not_a_transfer",
                "next_action":"parse and independently prove underlying all-index formula, then verify OEIS premise"}
        if s in rational_forms and t in rational_forms and bucket in ('cross_component','in_component'):
            hits=[]
            for p,ps,pl in rational_forms[s]:
                for q,qt,ql in rational_forms[t]:
                    if p.minus(q).is_zero():
                        hits.append({"identity":"source(n) == target(n)","proof":"exact equality in Q(n)",
                                     "source_expression":ps,"target_expression":qt,"domain":"where all original expressions defined"})
                    elif (a:=affine_certificate(p,q)) is not None:
                        hits.append({**a,"target_expression":ps,"source_expression":qt,
                                     "domain":"all n where the original OEIS expressions are defined"})
            if hits:
                output['formal_expression_certificates']=hits[:5]
                output['next_action']='Review OEIS identification and index offsets; formal algebra is certified only for supplied expressions'
                rational_candidates.append({"pair":[s,t],"count":len(hits)})
        queues[bucket].append(output)
    for q in queues.values():
        q.sort(key=lambda item:(-item['priority_score'],-item['mentions'],item['from'],item['to']))
    return {"schema":SCHEMA_VERSION,"author":"Komorebi P.","scope":"transfer discovery leads; existing formula-level proofs retain their original scope",
            "safety":"OEIS source text never executed; cross-references are lexical leads only",
            "network":{"records":len(network['records']),"edges":len(network['edges']),
                       "types":network['counts'],"components":len(groups),
                       "largest_component_sizes":[len(g) for g in groups[:20]],
                       "largest_component_members":groups[0][:30],
                       "source_oeis_snapshot_sha256":network['oeis']['snapshot_sha256']},
            "scan":{"source_lines_scanned":formula_count,"reference_occurrences":obs_count,
                    "kinds":dict(kind_counts),"rational_parse_attempts":parse_attempts,
                    "rational_formulas_parsed":parse_success,"rational_formula_sequence_ids":len(rational_forms),
                    "pairs_with_exact_expression_certificates":len(rational_candidates)},
            "queue_counts":{k:len(v) for k,v in queues.items()},"queues":queues,
            "claim_boundary":"Expression identities in Q(n) are not automatically OEIS sequence identities; index offsets and domains must be independently verified."}


def audit(network_file: Path, source_manifest: Path | None, source_db: Path | None,
          output: Path, limit: int | None = None, recurrence_seeds: Path | None = None) -> dict:
    network=load_network(network_file)
    if source_manifest:
        d=json.loads(source_manifest.read_text(encoding="utf-8"))
        if d.get('snapshot_sha256')!=network['oeis']['snapshot_sha256']:
            raise ValueError('Source formula manifest snapshot does not match network snapshot')
    report=scanner(network,formula_rows(source_manifest,source_db),limit=limit)
    if recurrence_seeds:
        from oeis_cfinite_bridge import write_certificates
        comp,_=components(network)
        report['cfinite_recurrence_certificates']=write_certificates(
            recurrence_seeds,set(comp),comp,output/'cfinite_recurrence_certificates.json')
    report['inputs']={"network_sha256":file_sha256(network_file),
                      "formula_source_sha256":file_sha256(source_manifest) if source_manifest else None,
                      "source_db_file_sha256":file_sha256(source_db) if source_db else None,
                      "formula_source":"sqlite" if source_db else "curated-manifest",
                      "formula_snapshot_matches_network":bool(source_manifest),
                      "scan_limit":limit}
    output.mkdir(parents=True,exist_ok=True)
    write_json(output/'audit.json',{k:v for k,v in report.items() if k!='queues'})
    write_json(output/'review_queues.json',report)
    for name, data in report['queues'].items():
        with (output/(name+'.csv')).open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['from','to','priority_score','mentions','source_component','target_component','formula_kinds','fields','source_line','triage_status','source_excerpt','next_action'])
            w.writeheader()
            for row in data:
                clean={**row,'formula_kinds':';'.join(row['formula_kinds']), 'fields':';'.join(row['fields'])}
                w.writerow({k:safe_csv_cell(clean.get(k)) for k in w.fieldnames})
    return {**report['network'], **report['scan'], 'queue_counts':report['queue_counts'],
            'output':str(output)}


def main(argv: list[str] | None = None) -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    ing=sub.add_parser('ingest',help='Import full or partial pinned oeis/oeisdata sequence files into SQLite')
    ing.add_argument('--oeis-dir',type=Path,required=True)
    ing.add_argument('--db',type=Path,required=True)
    ing.add_argument('--revision',required=True,help='OEIS git revision or explicit unversioned label')
    ing.add_argument('--limit',type=int)
    aud=sub.add_parser('audit',help='Compute network components and source-bound bridge review queues')
    aud.add_argument('--network',type=Path,required=True)
    src=aud.add_mutually_exclusive_group(required=True)
    src.add_argument('--formulas',type=Path)
    src.add_argument('--source-db',type=Path)
    aud.add_argument('--out',type=Path,required=True)
    aud.add_argument('--limit',type=int)
    aud.add_argument('--recurrence-seeds',type=Path,help='Optional reviewed order-2 recurrence premises')
    args=parser.parse_args(argv)
    result=(ingest(args.oeis_dir,args.db,args.revision,args.limit) if args.command=='ingest' else
            audit(args.network,args.formulas,args.source_db,args.out,args.limit,args.recurrence_seeds))
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
