"""Exact Q(x) replay of the user's older v0.8 Riordan source certificates.

Author: Komorebi P.
Original construction and normalization source:
  Komorebi_OEIS_All_Versions_Through_v0_8.zip
  current/komorebi_oeis_v08/transfer_engines_v08.py
  current/komorebi_oeis_v08/rational_operators.py

Cross-version matching against OEIS finite term excerpts is a source check,
NOT an all-index derivation of the OEIS sequence labels.
"""
from __future__ import annotations
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sqlite3
from sequence_archive_rational_operators import RatOGF, add, mul, pow_poly, poly_shift
from sequence_archive_v08_bridge import riordan_nth, quadratic_pair


def riordan_ogf(source, *, c:int,s:int,r:int,t:int):
    """Exact formal rational substitution (1-cx)^(-s) A(x^r/(1-cx)^t)."""
    if any(type(x) is not int for x in (c,s,r,t)) or s<0 or r<1 or t<1:
        raise ValueError('invalid Riordan parameters')
    if not isinstance(source,RatOGF):raise TypeError('rational OGF required')
    d=max(len(source.num),len(source.den))-1
    first=[Fraction(1),Fraction(-c)]
    def lift(poly):
        result=[Fraction(0)]
        for i,coef in enumerate(poly):
            if coef:
                product=poly_shift(pow_poly(first,t*(d-i)),r*i)
                result=add(result,[coef*x for x in product])
        return result
    return RatOGF(tuple(lift(source.num)),
                  tuple(mul(lift(source.den),pow_poly(first,s))))


def _source_terms(db,sid):
    row=db.execute('SELECT name,offset,terms_json,source_sha256 FROM sequences WHERE oeis_id=?',(sid,)).fetchone()
    if row is None:raise ValueError('source record missing: '+sid)
    return {'name':row[0], 'offset':row[1], 'terms':[int(v) for v in json.loads(row[2])],
            'source_sha256':row[3]}


def replay_riordan_archive(archive_csv,oeis_db,*,term_count=25):
    """Reprove every rational OGF identity and independently compare source terms."""
    if type(term_count) is not int or term_count<1:raise ValueError('positive term count required')
    archive_csv=Path(archive_csv);oeis_db=Path(oeis_db)
    out=[]
    with sqlite3.connect(f'file:{oeis_db}?mode=ro',uri=True) as db:
        if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
            raise ValueError('source database failed integrity check')
        with archive_csv.open(newline='',encoding='utf8') as f:
            for row in csv.DictReader(f):
                a,b=row['source_id'],row['target_id']
                c,s,r,t=(int(row[k]) for k in ('c','s','r','t'))
                original=RatOGF.from_json(json.loads(row['source_ogf_json']))
                target=RatOGF.from_json(json.loads(row['target_ogf_json']))
                derived=riordan_ogf(original,c=c,s=s,r=r,t=t)
                if derived.num!=target.num or derived.den!=target.den:
                    raise ArithmeticError('archived rational identity no longer holds: '+row['cert_key'])
                source=_source_terms(db,a);dest=_source_terms(db,b)
                if len(source['terms'])<term_count or len(dest['terms'])<term_count:
                    raise ValueError('insufficient current OEIS term excerpts')
                if original.terms(term_count)!=source['terms'][:term_count] or \
                   target.terms(term_count)!=dest['terms'][:term_count]:
                    raise ArithmeticError('source OGF disagrees with current OEIS finite terms')
                generated=[riordan_nth(source['terms'].__getitem__,n,c=c,s=s,r=r,t=t)
                           for n in range(term_count)]
                if generated!=dest['terms'][:term_count]:
                    raise ArithmeticError('Riordan coefficient formula disagrees with current OEIS')
                out.append({'archived_certificate_key':row['cert_key'],
                    'source_oeis_id':a,'target_oeis_id':b,'c':c,'s':s,'r':r,'t':t,
                    'archived_premise_status':row['premise_state'],
                    'source_formula_sha256_current':source['source_sha256'],
                    'target_formula_sha256_current':dest['source_sha256'],
                    'exact_rational_identity':True,'finite_terms_replayed':term_count,
                    'source_offset':source['offset'],'target_offset':dest['offset'],
                    'invertible_unramified':bool(r==1 and t==1),
                    'proof_scope':'all-index Q(x) identity conditional on source and target OGF premise; OEIS identification finitely checked'})
    return {'schema':1,'author':'Komorebi P.','archive_sha256':hashlib.sha256(archive_csv.read_bytes()).hexdigest(),
        'archive_riordan_certificates':len(out),'exact_rational_identities':len(out),
        'cross_snapshot_source_term_comparisons':2*len(out)*term_count,
        'cross_snapshot_riordan_output_comparisons':len(out)*term_count,
        'all_index_oeis_sequence_identifications_proved':0,
        'source_attribution':'OEIS Foundation Inc.; CC BY-SA 4.0',
        'certificates':out}


def verify_quadratic_oeis_channels(db_path,term_count=30):
    """Recheck two archived quadratic channels against current OEIS excerpts."""
    out=[]
    with sqlite3.connect(f'file:{Path(db_path)}?mode=ro',uri=True) as db:
        for q,c,power,even,odd in [
            (2,1,'A000079','A001333','A000129'),
            (3,2,'A000244','A001075','A001353'),
        ]:
            source=_source_terms(db,power)
            e=_source_terms(db,even);o=_source_terms(db,odd)
            N=min(term_count,len(source['terms']),len(e['terms']),len(o['terms']))
            for n in range(N):
                if source['terms'][n]!=q**n:
                    raise ArithmeticError('power source inconsistent')
                B,D=quadratic_pair(c,q,n)
                if B!=e['terms'][n] or D!=o['terms'][n]:
                    raise ArithmeticError('quadratic specialization inconsistent')
                if B*B-q*D*D!=(c*c-q)**n:
                    raise ArithmeticError('quadratic norm inconsistent')
            out.append({'q':q,'c':c,'source_id':power,'B_id':even,'D_id':odd,
                        'checked_indices':N,
                        'source_sha256':[source['source_sha256'],e['source_sha256'],o['source_sha256']],
                        'scope':'quadratic-extension identity exact; OEIS identification checked at finite terms'})
    return out
