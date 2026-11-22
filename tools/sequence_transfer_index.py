"""Disk-backed OEIS single-source transfer search with bounded memory.

Author: Komorebi P.

This module mines exact *finite-prefix candidates*. A candidate is NEVER a
proof of an identity of infinite sequences. It preserves both OEIS offsets,
uses a 10-term SHA-256 index to find plausible output sequences, and checks
all available overlapping terms after the discovery signature. Neither
formula text nor OEIS program listings are executed.

The persistent index is designed to support large corpora one source row at a
time. Pairwise AND-hyperedge mining stays in the small-corpus miner.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import sqlite3

from sequence_transfer_miner import (
    _candidate_statement, _hash_terms, _well_informed, identity,
    ensure_miner_schema,
)

SINGLE_OPERATORS = (
    'shift', 'polyphase', 'add_constant', 'multiply_constant',
    'adjacent_difference', 'prefix_sum',
    'binomial_transform', 'inverse_binomial_transform',
)


def _terms(raw):
    return tuple(int(x) for x in json.loads(raw))


def _digest(terms):
    # Canonical source witness covers ALL stored terms, not just the index key.
    return hashlib.sha256(json.dumps(terms, separators=(',', ':')).encode()).hexdigest()


def _key(terms, width):
    return hashlib.sha256(json.dumps(terms[:width],separators=(',', ':')).encode()).hexdigest()


def ensure_index(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS transfer_prefix_index(
        oeis_id TEXT PRIMARY KEY,
        width INTEGER NOT NULL,
        prefix_hash TEXT,
        offset INTEGER NOT NULL,
        term_count INTEGER NOT NULL,
        terms_digest TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS transfer_prefix_lookup
    ON transfer_prefix_index(width,prefix_hash);
    ''')
    ensure_miner_schema(db)


def build_prefix_index(db, *, width=10, commit_every=1000):
    """O(number of stored terms); one sequence term list resident at a time.

    Rebuild mode is idempotent and removes disappeared sequences. The miner
    validates row digests again before admitting prefix-index hits.
    """
    if width < 8: raise ValueError('index width must be at least eight')
    if commit_every < 1: raise ValueError('commit_every must be positive')
    ensure_index(db)
    counts=Counter()
    read=db.execute('SELECT oeis_id,offset,terms_json FROM sequences ORDER BY oeis_id')
    for sid, offset, raw in read:
        terms=_terms(raw)
        enabled=len(terms)>=width and _well_informed(terms[:width])
        key=_key(terms,width) if enabled else None
        old=db.execute('SELECT width,prefix_hash,offset,term_count,terms_digest FROM transfer_prefix_index WHERE oeis_id=?',(sid,)).fetchone()
        item=(width,key,offset,len(terms),_digest(terms))
        if old==item:
            counts['unchanged']+=1
        else:
            db.execute('''INSERT INTO transfer_prefix_index VALUES (?,?,?,?,?,?)
                ON CONFLICT(oeis_id) DO UPDATE SET width=excluded.width,
                prefix_hash=excluded.prefix_hash,offset=excluded.offset,
                term_count=excluded.term_count,terms_digest=excluded.terms_digest''',
                (sid,)+item)
            counts['updated' if old else 'inserted']+=1
        if sum(counts.values())%commit_every==0:db.commit()
    prior=db.execute('SELECT count(*) FROM transfer_prefix_index').fetchone()[0]
    db.execute('DELETE FROM transfer_prefix_index WHERE oeis_id NOT IN (SELECT oeis_id FROM sequences)')
    counts['removed']=prior-db.execute('SELECT count(*) FROM transfer_prefix_index').fetchone()[0]
    db.commit()
    return dict(counts, indexed=db.execute('SELECT count(*) FROM transfer_prefix_index WHERE prefix_hash IS NOT NULL').fetchone()[0],
                stored=db.execute('SELECT count(*) FROM transfer_prefix_index').fetchone()[0], width=width)


def _generators(source, *, width, max_modulus):
    """Yield non-pairwise transformations; local OEIS coefficients start at 0."""
    length=len(source)
    for shift in range(1,min(6,length-width+1)):
        yield 'shift',{'shift':shift},source[shift:]
    for modulus in range(2,max_modulus+1):
        for residue in range(modulus):
            yield 'polyphase',{'modulus':modulus,'residue':residue},source[residue::modulus]
    for d in (-3,-2,-1,1,2,3):
        yield 'add_constant',{'constant':d},[v+d for v in source]
    for scale in (-4,-3,-2,2,3,4):
        yield 'multiply_constant',{'constant':scale},[v*scale for v in source]
    yield 'adjacent_difference',{},[source[i+1]-source[i] for i in range(length-1)]
    yield 'prefix_sum',{},list(itertools.accumulate(source))
    for sign,kind in ((1,'binomial_transform'),(-1,'inverse_binomial_transform')):
        yield kind,{},[sum(math.comb(n,k)*source[k]*(1 if sign==1 else (-1)**(n-k))
                           for k in range(n+1)) for n in range(length)]


def mine_indexed(db, *, width=10, max_modulus=4, from_id=None, through_id=None,
                 reset_unary=False, commit_every=500, auto_index=True):
    """Search indexed outputs with O(1) sequence memory, not an S x S scan.

    Repeated/sharded calls are idempotent. For fresh whole-corpus reruns set
    reset_unary=True; pairwise candidates from v0.4 are never deleted here.
    """
    if width<10 or max_modulus<2 or max_modulus>12 or commit_every<1:
        raise ValueError('width>=10, 2<=max_modulus<=12, commit_every>=1 required')
    ensure_index(db)
    if auto_index:
        build_prefix_index(db,width=width,commit_every=commit_every)
    elif db.execute('SELECT count(*) FROM transfer_prefix_index WHERE width=?',(width,)).fetchone()[0] == 0:
        raise ValueError('index missing: build it first')
    if reset_unary:
        placeholders=','.join('?' for _ in SINGLE_OPERATORS)
        db.execute(f'DELETE FROM transfer_candidates WHERE operator IN ({placeholders})',SINGLE_OPERATORS)
    counts=Counter()
    select='SELECT oeis_id,offset,terms_json FROM sequences WHERE 1=1'
    params=[]
    if from_id:
        select+=' AND oeis_id>=?';params.append(from_id)
    if through_id:
        select+=' AND oeis_id<=?';params.append(through_id)
    select+=' ORDER BY oeis_id'
    incoming=db.execute(select,params)
    for sid, source_offset, raw in incoming:
        source=_terms(raw)
        counts['sources']+=1
        if len(source)<width:
            continue
        source_digest=_hash_terms(source_offset,source)
        for op, parms, generated in _generators(source,width=width,max_modulus=max_modulus):
            if len(generated)<=width or not _well_informed(generated[:width]):
                continue
            prefix=_key(generated,width)
            target_cursor=db.execute('''SELECT ix.oeis_id,ix.offset,ix.terms_digest,s.terms_json
                FROM transfer_prefix_index AS ix
                JOIN sequences AS s ON s.oeis_id=ix.oeis_id
                WHERE ix.width=? AND ix.prefix_hash=?''',(width,prefix))
            for target_id, target_offset, digest, target_raw in target_cursor:
                if target_id==sid:
                    continue
                target=_terms(target_raw)
                if _digest(target)!=digest:
                    # A source edit invalidates the cache until rebuilt.
                    counts['stale_index_hits']+=1
                    continue
                checked=min(len(generated),len(target))
                if checked<=width or any(generated[i]!=target[i] for i in range(checked)):
                    continue
                candidate_id=identity(target_id,[sid],op,parms)
                data={sid:(source_offset,source), target_id:(target_offset,target)}
                sources={sid:source_digest,target_id:_hash_terms(target_offset,target)}
                db.execute('''INSERT INTO transfer_candidates VALUES
                    (?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(candidate_id) DO UPDATE SET
                        checked_terms=excluded.checked_terms,
                        discovery_terms=excluded.discovery_terms,
                        holdout_terms=excluded.holdout_terms,
                        source_hashes_json=excluded.source_hashes_json,
                        statement=excluded.statement''',(
                    candidate_id,target_id,json.dumps([sid]),op,json.dumps(parms,sort_keys=True),
                    checked,width,checked-width,
                    _candidate_statement(target_id,[sid],op,parms,data),
                    'finite_candidate','sql_prefix_index',json.dumps(sources,sort_keys=True)))
                counts['exact_prefix_hits']+=1
                counts['by_'+op]+=1
        if counts['sources']%commit_every==0:db.commit()
    db.commit()
    return {
        'sources_scanned':counts['sources'],
        'exact_prefix_hits':counts['exact_prefix_hits'],
        'by_operator':{k[3:]:v for k,v in sorted(counts.items()) if k.startswith('by_')},
        'stale_index_hits':counts['stale_index_hits'],
        'proof_status':'finite_candidate_only',
        'memory':'one source and one retrieved target record at a time (plus SQLite cursors)',
        'range':{'from_id':from_id,'through_id':through_id}
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    sub=p.add_subparsers(dest='command',required=True)
    b=sub.add_parser('index');b.add_argument('--width',type=int,default=10)
    m=sub.add_parser('mine');m.add_argument('--width',type=int,default=10)
    m.add_argument('--max-modulus',type=int,default=4)
    m.add_argument('--from-id');m.add_argument('--through-id')
    m.add_argument('--reset-unary',action='store_true')
    m.add_argument('--no-rebuild',action='store_true')
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        result=(build_prefix_index(db,width=args.width) if args.command=='index'
                else mine_indexed(db,width=args.width,max_modulus=args.max_modulus,
                                  from_id=args.from_id,through_id=args.through_id,
                                  reset_unary=args.reset_unary,auto_index=not args.no_rebuild))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
