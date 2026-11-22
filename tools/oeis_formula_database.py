"""OEIS/Komorebi formula catalogue. Python 3.10+, stdlib only.

The raw formula fields are *leads*, not certified or executable formulas.
Curated executable specifications are evaluated by a small, non-eval DSL.
A finite matching prefix never certifies a mathematical identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sqlite3
from pathlib import Path

ID = re.compile(r"^A\d{6}$")
FIELD = re.compile(r"^%([A-Za-z])\s+(A\d{6})\s*(.*)$")
INTEGER = re.compile(r"^[+-]?\d+$")
LICENSE = "CC-BY-SA-4.0"


def canonical(value):
    value = value.strip()
    if not INTEGER.fullmatch(value):
        raise ValueError(f"Non-integer sequence term: {value[:80]!r}")
    return str(int(value)) if len(value) < 4000 else (value.lstrip("+").lstrip("0") or "0")


def fingerprint(*parts):
    return hashlib.sha256(json.dumps(parts, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def connect(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA synchronous=NORMAL")
    db.executescript("""
    CREATE TABLE IF NOT EXISTS sequences (
      oeis_id TEXT PRIMARY KEY, name TEXT NOT NULL, offset INTEGER NOT NULL,
      offset_second INTEGER, terms_json TEXT NOT NULL, keywords TEXT NOT NULL,
      source_sha256 TEXT NOT NULL, source_url TEXT NOT NULL, license TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS formulas (
      formula_id TEXT PRIMARY KEY, oeis_id TEXT REFERENCES sequences(oeis_id),
      local_id TEXT, origin TEXT NOT NULL, field TEXT NOT NULL, ordinal INTEGER NOT NULL,
      kind TEXT NOT NULL, expression TEXT NOT NULL, evaluator_json TEXT,
      source_url TEXT NOT NULL, license TEXT NOT NULL, proof_status TEXT NOT NULL,
      verification TEXT NOT NULL, checked_terms INTEGER NOT NULL DEFAULT 0,
      first_failure TEXT, complexity TEXT,
      CHECK (oeis_id IS NOT NULL OR local_id IS NOT NULL)
    );
    CREATE INDEX IF NOT EXISTS formula_sequence_idx ON formulas(oeis_id, origin);
    CREATE INDEX IF NOT EXISTS formula_review_idx ON formulas(verification, kind);
    CREATE TABLE IF NOT EXISTS komorebi_records (
      local_id TEXT PRIMARY KEY, name TEXT NOT NULL, offset INTEGER NOT NULL,
      terms_json TEXT NOT NULL, source_url TEXT NOT NULL, record_sha256 TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS crosswalks (
      local_id TEXT NOT NULL REFERENCES komorebi_records(local_id),
      oeis_id TEXT NOT NULL, relation TEXT NOT NULL, evidence TEXT NOT NULL,
      PRIMARY KEY(local_id, oeis_id, relation)
    );
    """)
    return db


def parse_seq(raw):
    """Read the primary OEIS internal format, never infer mathematical offsets."""
    fields = {}
    seq_id = None
    for line in raw.splitlines():
        match = FIELD.match(line)
        if not match:
            continue
        field, found_id, data = match.groups()
        if seq_id is None:
            seq_id = found_id
        if found_id != seq_id:
            raise ValueError("Mixed OEIS IDs in one source file")
        fields.setdefault(field, []).append(data)
    if not seq_id:
        raise ValueError("No OEIS entry fields found")
    if "O" not in fields:
        raise ValueError(f"Missing mathematical offset for {seq_id}")
    offsets = fields["O"][0].split(",")
    first, second = int(offsets[0]), int(offsets[1]) if len(offsets) > 1 else None
    if first < 0:
        raise ValueError("Unsupported negative start index")
    raw_terms = "".join("".join(fields.get(x, ())) for x in "STU").strip(", ")
    terms = [canonical(t) for t in raw_terms.split(",") if t.strip()]
    return dict(oeis_id=seq_id, name=fields.get("N", [seq_id])[0], offset=first,
                offset_second=second, terms=terms, keywords=",".join(fields.get("K", [])),
                formulas=fields.get("F", []),
                programs={x: fields.get(x, []) for x in "pto"})


def classify_formula(s):
    x = s.lower()
    if "g.f." in x or "e.g.f." in x or "generating function" in x:
        return "generating_function"
    if re.search(r"\ba\s*\(\s*n\s*\)\s*=", x):
        return "recurrence" if re.search(r"a\s*\(\s*n\s*[-+]", x) else "term_candidate"
    if "sum_" in x or "sum(" in x or "sum_{" in x:
        return "finite_or_infinite_sum"
    if "product" in x or "prod_" in x:
        return "product_candidate"
    return "unclassified"


def store_seq(db, entry, raw, *, preserve_verified=True):
    sid = entry["oeis_id"]
    if not ID.fullmatch(sid):
        raise ValueError("Invalid OEIS ID")
    source_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    previous = db.execute("SELECT source_sha256 FROM sequences WHERE oeis_id=?", (sid,)).fetchone()
    if previous and previous[0] == source_sha:
        return "unchanged"
    url = f"https://oeis.org/{sid}"
    db.execute("""INSERT INTO sequences VALUES (?,?,?,?,?,?,?,?,?)
       ON CONFLICT(oeis_id) DO UPDATE SET name=excluded.name,offset=excluded.offset,
       offset_second=excluded.offset_second,terms_json=excluded.terms_json,
       keywords=excluded.keywords,source_sha256=excluded.source_sha256,
       source_url=excluded.source_url,license=excluded.license""",
       (sid, entry["name"], entry["offset"], entry["offset_second"],
        json.dumps(entry["terms"]), entry["keywords"], source_sha, url, LICENSE))
    db.execute("DELETE FROM formulas WHERE oeis_id=? AND origin IN ('oeis_formula', 'oeis_program')", (sid,))
    for i, expr in enumerate(entry["formulas"]):
        kind = classify_formula(expr)
        fid = fingerprint(sid, "OEIS", "F", i, expr)
        db.execute("""INSERT INTO formulas
             (formula_id,oeis_id,origin,field,ordinal,kind,expression,source_url,license,
              proof_status,verification) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (fid, sid, "oeis_formula", "F", i, kind, expr, url, LICENSE,
             "unassessed", "unreviewed"))
    for field, block in entry["programs"].items():
        if not block:
            continue
        expr = "\n".join(block)
        fid = fingerprint(sid, "OEIS", field, expr)
        db.execute("""INSERT INTO formulas
            (formula_id,oeis_id,origin,field,ordinal,kind,expression,source_url,license,
             proof_status,verification) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
             (fid, sid, "oeis_program", field, 0, "program_reference", expr, url,
              LICENSE, "unassessed", "not_executed"))
    return "updated" if previous else "inserted"


def ingest_oeis(db, root, limit=None, batch_size=1000):
    root = Path(root)
    if root.is_file():
        files = [root]
    else:
        files = root.rglob("*.seq")
    counters = {"seen": 0, "inserted": 0, "updated": 0, "unchanged": 0, "errors": 0}
    error_samples = []
    for file in files:
        if limit is not None and counters["seen"] >= limit:
            break
        counters["seen"] += 1
        try:
            raw = file.read_text(encoding="utf-8")
            entry = parse_seq(raw)
            if file.name != entry["oeis_id"] + ".seq":
                raise ValueError("File name does not match internal ID")
            result = store_seq(db, entry, raw)
            counters[result] += 1
        except (OSError, UnicodeError, ValueError, sqlite3.Error) as exc:
            counters["errors"] += 1
            if len(error_samples) < 12:
                error_samples.append(f"{file}: {exc}")
        if counters["seen"] % batch_size == 0:
            db.commit()
    db.commit()
    return dict(**counters, error_samples=error_samples)


def evaluate(spec, n, *, budget=100000):
    """Exact, bounded, declarative evaluator. No eval/exec of OEIS text."""
    if not isinstance(n, int) or n < 0 or n > budget:
        raise ValueError("index outside safe evaluation window")
    def ev(x, scope):
        if isinstance(x, int):
            return x
        if not isinstance(x, dict):
            raise ValueError("evaluator nodes must be integers or objects")
        op = x.get("op")
        if op == "n":
            return scope["n"]
        if op == "var":
            return scope[x["name"]]
        if op == "add":
            return sum(ev(y, scope) for y in x["args"])
        if op == "mul":
            return math.prod(ev(y, scope) for y in x["args"])
        if op == "sub":
            a, b = x["args"]
            return ev(a, scope) - ev(b, scope)
        if op == "pow":
            base, power = ev(x["base"], scope), ev(x["exp"], scope)
            if power < 0 or power > budget:
                raise ValueError("exponent outside safe window")
            return base ** power
        if op == "factorial":
            arg = ev(x["arg"], scope)
            if arg < 0 or arg > budget:
                raise ValueError("factorial argument outside safe window")
            return math.factorial(arg)
        if op == "binomial":
            a, b = ev(x["n"], scope), ev(x["k"], scope)
            if a < 0 or a > budget:
                raise ValueError("binomial top outside safe window")
            return math.comb(a, b) if 0 <= b <= a else 0
        if op == "exact_div":
            a, b = ev(x["num"], scope), ev(x["den"], scope)
            if not b or a % b:
                raise ValueError("division is not exact")
            return a // b
        if op == "sum":
            lo, hi = ev(x["from"], scope), ev(x["to"], scope)
            if hi - lo > budget:
                raise ValueError("sum range exceeds budget")
            var = x.get("var", "k")
            return sum(ev(x["body"], {**scope, var: k}) for k in range(lo, hi + 1))
        if op == "linear_recurrence":
            initial, coeff = x["initial"], x["coefficients"]
            order = len(initial)
            if not order or len(coeff) != order or any(not isinstance(c, int) for c in initial + coeff):
                raise ValueError("malformed recurrence")
            vals = list(initial)
            for j in range(order, n + 1):
                vals.append(sum(coeff[k] * vals[j-k-1] for k in range(order)))
            return vals[n]
        if op == "bell":
            vals = [1]
            for j in range(1, n + 1):
                vals.append(sum(math.comb(j-1,k) * vals[k] for k in range(j)))
            return vals[n]
        if op == "fubini":
            vals = [1]
            for j in range(1, n + 1):
                vals.append(sum(math.comb(j,k) * vals[j-k] for k in range(1,j+1)))
            return vals[n]
        if op == "involutions":
            vals = [1,1]
            for j in range(2,n+1):
                vals.append(vals[-1] + (j-1)*vals[-2])
            return vals[n]
        if op == "derangements":
            vals = [1,0]
            for j in range(2,n+1):
                vals.append((j-1) * (vals[-1] + vals[-2]))
            return vals[n]
        if op == "motzkin":
            vals = [1,1]
            for j in range(2,n+1):
                numerator = (2*j+1)*vals[-1]+3*(j-1)*vals[-2]
                if numerator%(j+2):
                    raise ValueError("Motzkin recurrence lost integrality")
                vals.append(numerator//(j+2))
            return vals[n]
        if op == "partitions":
            vals = [1]
            for j in range(1,n+1):
                total = 0
                for k in range(1,j+1):
                    sign = 1 if k%2 else -1
                    left = k*(3*k-1)//2
                    right = k*(3*k+1)//2
                    if left > j:
                        break
                    total += sign*vals[j-left]
                    if right <= j:
                        total += sign*vals[j-right]
                vals.append(total)
            return vals[n]
        if op == "divisor_sum":
            if n == 0:
                raise ValueError("divisor functions require positive indices")
            power = x["power"]
            if power not in (0,1):
                raise ValueError("unsupported divisor power")
            return sum((d ** power)*(1 if d*d == n else 0) if d*d==n else (d ** power + (n//d)**power) for d in range(1, math.isqrt(n)+1) if n%d==0)
        if op == "totient":
            if n == 0:
                raise ValueError("totient requires positive index")
            return sum(math.gcd(k,n)==1 for k in range(1,n+1))
        raise ValueError(f"unsupported evaluator operation: {op!r}")
    return ev(spec, {"n":n})


def verify_formula(db, formula_id, max_terms=24):
    row = db.execute("""SELECT f.oeis_id,f.evaluator_json,s.offset,s.terms_json
      FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
      WHERE f.formula_id=?""", (formula_id,)).fetchone()
    if not row or not row[1]:
        raise ValueError("formula has no evaluator or no OEIS sequence")
    sid, raw_spec, offset, raw_terms = row
    terms = json.loads(raw_terms)[:max_terms]
    checked, failure = 0, None
    for i, expected in enumerate(terms):
        try:
            observed = evaluate(json.loads(raw_spec), offset+i)
            if str(observed) != expected:
                failure = {"n":offset+i,"expected":expected,"observed":str(observed)}
                break
            checked += 1
        except (ValueError, KeyError, TypeError, OverflowError) as exc:
            failure = {"n":offset+i,"error":str(exc)}
            break
    state = "rejected" if failure else "finite_checked" if checked >= 8 else "insufficient_terms"
    db.execute("UPDATE formulas SET verification=?,checked_terms=?,first_failure=? WHERE formula_id=?",
               (state,checked,json.dumps(failure) if failure else None,formula_id))
    return dict(oeis_id=sid,formula_id=formula_id,verification=state,checked_terms=checked,failure=failure)


def ingest_curated(db, path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("license") != LICENSE:
        raise ValueError("Curated source must explicitly credit OEIS CC BY-SA 4.0")
    results = []
    for seq in payload["sequences"]:
        sid = seq["oeis_id"]
        row = db.execute("SELECT oeis_id FROM sequences WHERE oeis_id=?", (sid,)).fetchone()
        if not row:
            db.execute("INSERT INTO sequences VALUES (?,?,?,?,?,?,?,?,?)", (
                sid, seq["name"], seq["offset"], None, json.dumps(seq["terms"]),
                "seed", "seed:"+fingerprint(seq), f"https://oeis.org/{sid}", LICENSE))
        for j, formula in enumerate(seq["formulas"]):
            expr, spec = formula["expression"], formula["evaluator"]
            fid = fingerprint(sid, "Komorebi-curated", expr, spec)
            db.execute("""INSERT INTO formulas
              (formula_id,oeis_id,origin,field,ordinal,kind,expression,evaluator_json,
              source_url,license,proof_status,verification,complexity)
              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(formula_id) DO NOTHING""",
              (fid,sid,"komorebi_curated","curated",j,formula["kind"],expr,
               json.dumps(spec,sort_keys=True),formula.get("source_url", f"https://oeis.org/{sid}"),
               LICENSE,formula.get("proof_status","classical_reference"),"unreviewed",formula.get("complexity")))
            results.append(verify_formula(db, fid))
    db.commit()
    return results


def ingest_komorebi(db, file):
    """Import the site's exported library, retaining KSEQ/KFOR/KOM identities.

    OEIS finite matches are provenance-linked as candidates, NOT a claim that
    the two infinite sequences are mathematically equal.
    """
    data = json.loads(Path(file).read_text(encoding="utf-8"))
    records = data["entries"] if isinstance(data,dict) else data
    stats = {"records":0,"representations":0,"finite_crosswalks":0,"claimed_crosswalks":0}
    for entry in records:
        local_id = entry["id"]
        terms = [str(x) for x in entry["terms"]]
        digest = fingerprint(local_id,terms)
        source = entry.get("source", "")
        db.execute("""INSERT INTO komorebi_records VALUES (?,?,?,?,?,?)
         ON CONFLICT(local_id) DO UPDATE SET name=excluded.name,offset=excluded.offset,
         terms_json=excluded.terms_json,source_url=excluded.source_url,
         record_sha256=excluded.record_sha256""",
         (local_id,entry.get("title", local_id),entry["offset"],json.dumps(terms),source,digest))
        db.execute("DELETE FROM formulas WHERE local_id=? AND origin='komorebi_record'", (local_id,))
        db.execute("DELETE FROM crosswalks WHERE local_id=?", (local_id,))
        for j, formula in enumerate(entry.get("formulas", [])):
            expr = formula["expression"]
            db.execute("""INSERT INTO formulas
              (formula_id,local_id,origin,field,ordinal,kind,expression,source_url,license,
               proof_status,verification) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
              (fingerprint(local_id,j,expr), local_id,"komorebi_record","source",j,
               formula.get("kind","unclassified"),expr,formula.get("source",source),
               "source-dependent", "source_linked", "not_revalidated"))
            stats["representations"] += 1
        for match in entry.get("matches", []):
            sid = match["id"]
            if ID.fullmatch(sid):
                db.execute("INSERT OR REPLACE INTO crosswalks VALUES (?,?,?,?)",
                     (local_id,sid,"finite_match",json.dumps({"matched_terms":match.get("matched_terms"),
                                    "position":match.get("position")})))
                stats["finite_crosswalks"] += 1
        sid = entry.get("oeis")
        if sid and ID.fullmatch(sid):
            db.execute("INSERT OR REPLACE INTO crosswalks VALUES (?,?,?,?)",
                 (local_id,sid,"source_claim", "Existing source attribution; not independently proved here"))
            stats["claimed_crosswalks"] += 1
        stats["records"] += 1
        if stats["records"] % 1000 == 0:
            db.commit()
    db.commit()
    return stats


def statistics(db):
    sql = lambda q: db.execute(q).fetchone()[0]
    return {
      "oeis_sequences_stored":sql("SELECT COUNT(*) FROM sequences"),
      "local_records_stored":sql("SELECT COUNT(*) FROM komorebi_records"),
      "raw_oeis_formula_lines":sql("SELECT COUNT(*) FROM formulas WHERE origin='oeis_formula'"),
      "raw_oeis_program_blocks":sql("SELECT COUNT(*) FROM formulas WHERE origin='oeis_program'"),
      "curated_evaluator_formulas":sql("SELECT COUNT(*) FROM formulas WHERE evaluator_json IS NOT NULL"),
      "curated_finite_checked":sql("SELECT COUNT(*) FROM formulas WHERE evaluator_json IS NOT NULL AND verification='finite_checked'"),
      "curated_rejected":sql("SELECT COUNT(*) FROM formulas WHERE verification='rejected'"),
      "local_formula_representations":sql("SELECT COUNT(*) FROM formulas WHERE origin='komorebi_record'"),
      "finite_match_links_not_proofs":sql("SELECT COUNT(*) FROM crosswalks WHERE relation='finite_match'")
    }


def inspect(db, identifier):
    if ID.fullmatch(identifier):
        row = db.execute("SELECT * FROM sequences WHERE oeis_id=?", (identifier,)).fetchone()
        if not row: return None
        record = dict(zip([x[1] for x in db.execute("PRAGMA table_info(sequences)")],row))
        record["terms"] = json.loads(record.pop("terms_json"))
        rows = db.execute("""SELECT origin,field,kind,expression,verification,checked_terms,
             complexity,source_url FROM formulas WHERE oeis_id=? ORDER BY
             CASE WHEN verification='finite_checked' THEN 0 ELSE 1 END, origin,ordinal""",
             (identifier,)).fetchall()
        cols = [d[0] for d in db.execute("""SELECT origin,field,kind,expression,verification,
             checked_terms,complexity,source_url FROM formulas LIMIT 0""").description]
        record["formulas"] = [dict(zip(cols,r)) for r in rows]
        record["komorebi_candidates"] = [dict(local_id=r[0],relation=r[1],evidence=r[2]) for r in
            db.execute("SELECT local_id,relation,evidence FROM crosswalks WHERE oeis_id=?",(identifier,))]
        return record
    row = db.execute("SELECT name,offset,terms_json,source_url FROM komorebi_records WHERE local_id=?",(identifier,)).fetchone()
    return dict(id=identifier,name=row[0],offset=row[1],terms=json.loads(row[2]),source_url=row[3]) if row else None


def search(db, text, limit=30, verified_only=False):
    """Search names and formula text. All query values are SQL parameters."""
    if not text.strip():
        return []
    pattern = "%" + text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
    verified = "AND f.verification='finite_checked'" if verified_only else ""
    rows = db.execute(f"""SELECT s.oeis_id,s.name,f.kind,f.verification,
             substr(f.expression,1,500) AS expression
        FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
        WHERE (s.oeis_id=? OR s.name LIKE ? ESCAPE '\\'
             OR f.expression LIKE ? ESCAPE '\\') {verified}
        ORDER BY CASE WHEN f.verification='finite_checked' THEN 0 ELSE 1 END,
                 s.oeis_id, f.ordinal LIMIT ?""",
        (text.strip().upper(),pattern,pattern,limit)).fetchall()
    return [dict(zip(("oeis_id","name","kind","verification","expression"),r)) for r in rows]


def export_jsonl(db, path, verified_only=True):
    """Stream a machine-readable formula export with a license notice per record."""
    condition = "AND f.verification='finite_checked'" if verified_only else ""
    cursor = db.execute(f"""SELECT s.oeis_id,s.name,s.offset,f.expression,f.kind,
               f.origin,f.verification,f.checked_terms,f.source_url,f.license,
               f.evaluator_json,f.proof_status
          FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
          WHERE 1=1 {condition} ORDER BY s.oeis_id,f.ordinal""")
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    keys=("oeis_id","name","offset","expression","kind","origin",
          "verification","checked_terms","source_url","license","evaluator","proof_status")
    count=0
    with path.open("w",encoding="utf-8",newline="\n") as f:
        for record in cursor:
            line=dict(zip(keys,record))
            line["evaluator"]=json.loads(line["evaluator"]) if line["evaluator"] else None
            f.write(json.dumps(line,ensure_ascii=False)+"\n")
            count+=1
    return {"exported_formulas":count,"path":str(path),"verified_only":verified_only}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db",type=Path,default=Path("oeis-formulas.sqlite3"))
    subs=p.add_subparsers(dest="command",required=True)
    imp=subs.add_parser("ingest-oeis");imp.add_argument("--path",type=Path,required=True);imp.add_argument("--limit",type=int)
    seed=subs.add_parser("ingest-seeds");seed.add_argument("--path",type=Path,required=True)
    km=subs.add_parser("ingest-komorebi");km.add_argument("--path",type=Path,required=True)
    query=subs.add_parser("show");query.add_argument("id")
    lookup=subs.add_parser("search");lookup.add_argument("text");lookup.add_argument("--limit",type=int,default=30)
    lookup.add_argument("--verified-only",action="store_true")
    exp=subs.add_parser("export-jsonl");exp.add_argument("--path",type=Path,required=True)
    exp.add_argument("--include-unreviewed",action="store_true")
    subs.add_parser("stats")
    args=p.parse_args(argv)
    with connect(args.db) as db:
        if args.command=="ingest-oeis":
            output=ingest_oeis(db,args.path,args.limit)
        elif args.command=="ingest-seeds":
            results=ingest_curated(db,args.path)
            output={"formulas":len(results),"finite_checked":sum(r["verification"]=="finite_checked" for r in results),
                "rejected":[r for r in results if r["verification"]=="rejected"]}
        elif args.command=="ingest-komorebi":
            output=ingest_komorebi(db,args.path)
        elif args.command=="show":
            output=inspect(db,args.id)
        elif args.command=="search":
            output=search(db,args.text,args.limit,args.verified_only)
        elif args.command=="export-jsonl":
            output=export_jsonl(db,args.path,not args.include_unreviewed)
        else:
            output=statistics(db)
    print(json.dumps(output,ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
