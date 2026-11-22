"""Conservative exact-term-formula discovery for imported OEIS entries.

Author: Komorebi P.

Only a small whitelist of arithmetic expressions is translated into a
non-executable JSON expression tree. A prefix match is not a proof and an
unmatched OEIS formula remains available for manual interpretation.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

from oeis_formula_database import connect, fingerprint, verify_formula

# Reject text that looks like prose, definitions, compound formulae, or code.
ASSIGNMENT = re.compile(r'(?<![A-Za-z0-9_])a\s*\(\s*n\s*\)\s*=\s*', re.I)
ALLOWED = re.compile(r'^[\d\s,+\-*/^()_a-zA-Z]+$')
CALLS = {'binomial': 'binomial', 'binom': 'binomial', 'factorial': 'factorial'}
MAX_CHARS = 240
MAX_NODES = 45


class UnsupportedFormula(ValueError):
    pass


def _from_ast(expr):
    """Build a constrained declarative AST, not Python executable code."""
    if isinstance(expr, ast.Constant) and type(expr.value) is int:
        return expr.value
    if isinstance(expr, ast.Name) and expr.id == 'n':
        return {'op': 'n'}
    if isinstance(expr, ast.UnaryOp):
        operand = _from_ast(expr.operand)
        if isinstance(expr.op, ast.UAdd):
            return operand
        if isinstance(expr.op, ast.USub):
            return {'op': 'sub', 'args': [0, operand]}
    if isinstance(expr, ast.BinOp):
        a, b = _from_ast(expr.left), _from_ast(expr.right)
        if isinstance(expr.op, ast.Add):
            return {'op': 'add', 'args': [a, b]}
        if isinstance(expr.op, ast.Sub):
            return {'op': 'sub', 'args': [a, b]}
        if isinstance(expr.op, ast.Mult):
            return {'op': 'mul', 'args': [a, b]}
        if isinstance(expr.op, ast.Pow):
            return {'op': 'pow', 'base': a, 'exp': b}
        if isinstance(expr.op, ast.Div):
            return {'op': 'exact_div', 'num': a, 'den': b}
    if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name):
        if expr.keywords or expr.func.id not in CALLS:
            raise UnsupportedFormula('unknown or keyword function call')
        args = [_from_ast(a) for a in expr.args]
        if expr.func.id in ('binomial', 'binom') and len(args) == 2:
            return {'op': 'binomial', 'n': args[0], 'k': args[1]}
        if expr.func.id == 'factorial' and len(args) == 1:
            return {'op': 'factorial', 'arg': args[0]}
    raise UnsupportedFormula('not in the exact arithmetic whitelist')


def compile_simple_term(rhs):
    """Compile only fully parseable single-term elementary arithmetic.

    Excludes power-series, conditional definitions, approximations, recurrences,
    terms with free parameters, implicit products and any library calls other
    than binomial and factorial. Divisions must evaluate exactly at each term.
    """
    rhs = rhs.strip()
    if not rhs or len(rhs) > MAX_CHARS or not ALLOWED.fullmatch(rhs):
        raise UnsupportedFormula('unsupported characters or length')
    # OEIS mathematical syntax often uses ^ for exponentiation.
    rhs = rhs.replace('^', '**')
    # Restrict to an unambiguous n variable: "2n" is otherwise invalid.
    try:
        tree = ast.parse(rhs, mode='eval')
    except (SyntaxError, ValueError) as exc:
        raise UnsupportedFormula('cannot parse expression') from exc
    if sum(1 for _ in ast.walk(tree)) > MAX_NODES:
        raise UnsupportedFormula('expression is too large')
    return _from_ast(tree.body)


def extract_simple_terms(text):
    """Return tightly delimited candidate formulae from an OEIS name/%F line.

    This intentionally discards many usable human formulas rather than
    truncating a more complicated formula into a plausible false one.
    """
    found = []
    for assignment in ASSIGNMENT.finditer(text):
        tail = text[assignment.end():].strip()
        # Do not silently erase an explicitly conditional trailing clause.
        if re.search(r';\s*(?:for|if|when|where)\b', tail, flags=re.I):
            continue
        # A . is an OEIS sentence delimiter only if followed by whitespace/end.
        tail = re.split(r'\.(?=\s|$)|;\s|\s+-\s+_', tail, maxsplit=1)[0].strip()
        # Avoid accidentally accepting a prefix of a conditional formula or one
        # with a comma outside any supported function call.
        for trailer in (' for ', ' if ', ' where ', ' when ', ' with ', ' = ', ' ~ ', ' approximately '):
            if trailer in ' ' + tail.lower() + ' ':
                tail = ''
                break
        if not tail or len(tail) > MAX_CHARS:
            continue
        try:
            spec = compile_simple_term(tail)
        except UnsupportedFormula:
            continue
        found.append((tail, spec))
    return found


def normalize_oeis(db, limit=None, min_terms=12, max_terms=24, batch_size=500):
    """Extract and independently compare candidates with official term windows.

    Source/verification state is updated on every re-normalization. A finite
    match remains proof_status='unassessed' regardless of its length.
    """
    if not 1 <= min_terms <= max_terms <= 100:
        raise ValueError('require 1 <= min_terms <= max_terms <= 100')
    rows = db.execute('SELECT oeis_id,name,offset FROM sequences ORDER BY oeis_id').fetchall()
    counts = {'sequences_scanned': 0, 'formula_lines_scanned': 0,
              'parsed_candidates': 0, 'finite_checked': 0,
              'insufficient_terms': 0, 'rejected': 0, 'negative_offset_skipped': 0}
    for sid, name, offset in rows:
        if limit is not None and counts['sequences_scanned'] >= limit:
            break
        counts['sequences_scanned'] += 1
        if offset < 0:
            counts['negative_offset_skipped'] += 1
            continue
        # Changed formulas are regenerated with content-addressed IDs.
        db.execute("DELETE FROM formulas WHERE oeis_id=? AND origin='oeis_normalized'", (sid,))
        raws = [('N', -1, name)] + db.execute("""SELECT field,ordinal,expression
            FROM formulas WHERE oeis_id=? AND origin='oeis_formula'
            ORDER BY ordinal""", (sid,)).fetchall()
        seen = set()
        for field, ordinal, line in raws:
            counts['formula_lines_scanned'] += 1
            for expr, spec in extract_simple_terms(line):
                signature = json.dumps(spec, sort_keys=True, separators=(',', ':'))
                if signature in seen:
                    continue
                seen.add(signature)
                fid = fingerprint(sid, 'oeis_normalized', spec)
                db.execute("""INSERT INTO formulas
                  (formula_id,oeis_id,origin,field,ordinal,kind,expression,
                   evaluator_json,source_url,license,proof_status,verification)
                  VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (fid,sid,'oeis_normalized',field,ordinal,'term_candidate',
                   f'a(n)={expr}',json.dumps(spec,sort_keys=True),
                   f'https://oeis.org/{sid}', 'CC-BY-SA-4.0',
                   'unassessed', 'unreviewed'))
                result = verify_formula(db,fid,max_terms=max_terms)
                # Require a larger minimum than the core verifier's 8 terms.
                state = result['verification']
                if state == 'finite_checked' and result['checked_terms'] < min_terms:
                    state = 'insufficient_terms'
                    db.execute('UPDATE formulas SET verification=? WHERE formula_id=?',(state,fid))
                counts['parsed_candidates'] += 1
                counts[state] += 1
        if counts['sequences_scanned'] % batch_size == 0:
            db.commit()
    db.commit()
    return counts


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--limit',type=int)
    p.add_argument('--min-terms',type=int,default=12)
    p.add_argument('--max-terms',type=int,default=24)
    args = p.parse_args(argv)
    with connect(args.db) as db:
        report = normalize_oeis(db,limit=args.limit,min_terms=args.min_terms,max_terms=args.max_terms)
    print(json.dumps(report,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
