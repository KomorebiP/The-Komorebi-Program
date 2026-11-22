"""Incremental, non-extracting archive import for official OEIS `.seq` files.

Author: Komorebi P.

Accepts a local ZIP or .tar[.gz/.xz] archive of oeisdata/seq tree, retains
raw formula and program fields without evaluating them, optionally stages
%Y references for the transfer graph. Handles errors per-entry transactionally.
OEIS Foundation data/adaptations require CC BY-SA 4.0 attribution.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sqlite3
import tarfile
import zipfile

from oeis_formula_database import connect, parse_seq, store_seq
from sequence_transfer_graph import ensure_schema, OEIS_ID, FORMULA

ARCHIVE_ENTRY_MAX_BYTES = 8 * 1024 * 1024


def sha256_file(path):
    d=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):d.update(block)
    return d.hexdigest()


def _valid_entry(path):
    """Constrain archive members; never unpack arbitrary paths."""
    parts=PurePosixPath(path).parts
    return (len(parts)>=3 and 'seq' in parts and
            re.fullmatch(r'A\d{6}\.seq',parts[-1]) is not None and
            'b-files' not in parts and '..' not in parts)


@contextmanager
def _members(archive):
    archive=Path(archive)
    if zipfile.is_zipfile(archive):
        z=zipfile.ZipFile(archive,'r')
        try:
            def items():
                for member in z.infolist():
                    if member.is_dir() or not _valid_entry(member.filename):continue
                    if member.file_size>ARCHIVE_ENTRY_MAX_BYTES:
                        yield member.filename,None,'oversize'
                        continue
                    with z.open(member) as fh:
                        raw=fh.read(ARCHIVE_ENTRY_MAX_BYTES+1)
                    yield member.filename,raw,'ok' if len(raw)<=ARCHIVE_ENTRY_MAX_BYTES else 'oversize'
            yield items()
        finally:z.close()
    elif tarfile.is_tarfile(archive):
        tar=tarfile.open(archive,mode='r:*')
        try:
            def items():
                for member in tar:
                    if not member.isfile() or not _valid_entry(member.name):continue
                    if member.size>ARCHIVE_ENTRY_MAX_BYTES:
                        yield member.name,None,'oversize';continue
                    with tar.extractfile(member) as fh:
                        raw=fh.read(ARCHIVE_ENTRY_MAX_BYTES+1)
                    yield member.name,raw,'ok' if len(raw)<=ARCHIVE_ENTRY_MAX_BYTES else 'oversize'
            yield items()
        finally:tar.close()
    else:raise ValueError('Source must be a valid zip or tar archive')


def _stage_y_refs(db, entry, raw, path):
    sid=entry['oeis_id']
    db.execute('DELETE FROM oeis_xrefs WHERE source_id=?',(sid,))
    found=0
    for line in raw.splitlines():
        m=FORMULA.match(line)
        if m and m[1]=='Y':
            for other in sorted(set(OEIS_ID.findall(m[3])) - {sid}):
                db.execute('INSERT OR REPLACE INTO oeis_xrefs VALUES (?,?,?,?)',
                           (sid,other,m[3][:1000],PurePosixPath(path).name))
                found+=1
    return found


def import_archive(db, path, *, limit=None, with_xrefs=True, batch_size=1000):
    """Low-memory archive import. Transactions roll back a malformed entry."""
    if batch_size<1 or limit is not None and limit<0:
        raise ValueError('invalid limit or batch size')
    if with_xrefs:ensure_schema(db)
    stats={'scanned':0,'inserted':0,'updated':0,'unchanged':0,
           'failed':0,'references_staged':0,'error_samples':[]}
    with _members(path) as items:
        for name,source,status in items:
            if limit is not None and stats['scanned']>=limit:break
            stats['scanned']+=1
            db.execute('SAVEPOINT import_entry')
            try:
                if status!='ok':raise ValueError('entry exceeds maximum size')
                raw=source.decode('utf-8')
                entry=parse_seq(raw)
                if name.rsplit('/',1)[-1] != entry['oeis_id']+'.seq':
                    raise ValueError('archive member filename does not match internal OEIS ID')
                stage=store_seq(db,entry,raw)
                if with_xrefs:stats['references_staged']+=_stage_y_refs(db,entry,raw,name)
                stats[stage]+=1
            except (ValueError,UnicodeError,sqlite3.Error,OSError) as exc:
                db.execute('ROLLBACK TO SAVEPOINT import_entry')
                stats['failed']+=1
                if len(stats['error_samples'])<12:
                    stats['error_samples'].append({'file':name,'reason':str(exc)[:250]})
            finally:db.execute('RELEASE SAVEPOINT import_entry')
            if stats['scanned']%batch_size==0:db.commit()
    db.commit()
    stats['archive_sha256']=sha256_file(path)
    stats['source_archive']=str(path)
    stats['disclaimer']='Raw OEIS formulas and programs are source text, not executed nor automatically proven'
    return stats


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--limit',type=int)
    p.add_argument('--no-xrefs',action='store_true')
    p.add_argument('--batch-size',type=int,default=1000)
    args=p.parse_args(argv)
    with connect(args.db) as db:
        r=import_archive(db,args.archive,limit=args.limit,
                         with_xrefs=not args.no_xrefs,batch_size=args.batch_size)
    print(json.dumps(r,indent=2))


if __name__=='__main__':main()
