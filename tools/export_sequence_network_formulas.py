#!/usr/bin/env python3
"""Export pinned, nonexecuting OEIS %%F text for connected Network records.

Author: Komorebi P.
Only official source text is retained. A source formula is not a proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3

OEIS_ID = re.compile(r"A\d{6}\Z")


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(4 * 1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def export(db_path: Path, index_path: Path, out_path: Path) -> dict:
    network = json.loads(index_path.read_text(encoding='utf-8'))
    source_sha256 = network['oeis']['snapshot_sha256']
    actual = digest(db_path)
    if actual != source_sha256:
        raise ValueError(f'OEIS SQLite source hash mismatch: {actual} != {source_sha256}')
    if network.get('schema') != 1 or network['oeis'].get('license') != 'CC-BY-SA-4.0':
        raise ValueError('Unsupported Network manifest or OEIS license')
    ids = sorted(row['id'] for row in network['records'])
    if len(set(ids)) != len(ids) or any(not OEIS_ID.fullmatch(identifier) for identifier in ids):
        raise ValueError('Network sequence identifiers must be unique OEIS IDs')
    grouped = {identifier: [] for identifier in ids}
    con = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    try:
        for start in range(0, len(ids), 400):
            batch = ids[start:start + 400]
            sql = ("SELECT oeis_id,kind,expression,source_url,verification "
                   "FROM formulas WHERE origin='oeis_formula' AND field='F' "
                   f"AND oeis_id IN ({','.join('?' for _ in batch)}) "
                   "ORDER BY oeis_id,ordinal,formula_id")
            for identifier, kind, formula, source_url, status in con.execute(sql, batch):
                if status != 'unreviewed':
                    raise ValueError(f'Unexpected OEIS raw formula evidence: {identifier}')
                if not isinstance(formula, str) or not isinstance(kind, str):
                    raise ValueError('Malformed OEIS raw formula')
                if source_url != f'https://oeis.org/{identifier}':
                    raise ValueError(f'Unexpected source URL for {identifier}')
                grouped[identifier].append({'kind': kind, 'text': formula})
    finally:
        con.close()
    entries = {identifier: {'source': f'https://oeis.org/{identifier}', 'formulas': rows}
               for identifier, rows in grouped.items() if rows}
    count = sum(len(row['formulas']) for row in entries.values())
    output = {'schema': 1, 'origin': 'Official OEIS %F fields (retained source text only)',
              'evidence': 'unreviewed_source_text',
              'license': 'CC-BY-SA-4.0',
              'attribution': 'The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc.',
              'snapshot_sha256': source_sha256,
              'scope': 'Only OEIS IDs in the curated Komorebi Network with %F records in the first 99,999-entry source snapshot. This does not prove the mathematical statements.',
              'counts': {'network_ids': len(ids), 'ids_with_formulas': len(entries), 'formula_lines': count},
              'entries': entries}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8', newline='\n')
    return output['counts']


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', required=True, type=Path)
    parser.add_argument('--network', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.db, args.network, args.output), indent=2))


if __name__ == '__main__':
    main()
