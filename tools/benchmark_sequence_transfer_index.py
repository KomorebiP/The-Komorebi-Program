"""Optional local throughput benchmark on synthetic sources, never OEIS claims."""
import argparse
import json
from pathlib import Path
import sqlite3
import tempfile
import time

from oeis_formula_database import connect
from sequence_transfer_index import build_prefix_index,mine_indexed


def benchmark(n=3000):
    with tempfile.TemporaryDirectory() as tmp:
        db=connect(Path(tmp)/'benchmark.sqlite3')
        for i in range(n):
            terms=[str((i+1)*(j+2)**2+17*j**3+4*j+1) for j in range(28)]
            db.execute('''INSERT INTO sequences VALUES (?,?,?,?,?,?,?,?,?)''',
               (f'A{600000+i:06d}',f'SYNTHETIC_#{i}',0,None,json.dumps(terms),
                '','synthetic_fixture','synthetic://not-oeis','CC-BY-SA-4.0'))
        db.commit()
        t=time.perf_counter()
        index=build_prefix_index(db)
        indexed_seconds=time.perf_counter()-t
        t=time.perf_counter()
        discovered=mine_indexed(db,from_id='A600000',through_id='A600299',auto_index=False)
        mining_seconds=time.perf_counter()-t
        db.close()
        return {'synthetic_only':True,'input_sequence_count':n,
                'source_rows_mined':discovered['sources_scanned'],
                'index_rows':index['stored'],
                'index_seconds':round(indexed_seconds,3),
                'partial_scan_seconds':round(mining_seconds,3),
                'generated_candidates':discovered['exact_prefix_hits'],
                'machine_dependent':True,
                'disclaimer':'Synthetic throughput check, not a proof of full OEIS corpus ingestion or bounded worst-case time'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sequences',type=int,default=3000)
    p.add_argument('--output',type=Path);args=p.parse_args()
    result=benchmark(args.sequences)
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
