"""Shared binary-power packet bank for sparse exact C-finite queries.

Author: Komorebi P.

For P(X)=X^d-c1 X^(d-1)-...-cd, the residues X^n mod P(X)
are universal for all sequences with that recurrence. The cached powers
X^(2^j) are constructed once and reused across many sequences and indices.
For monotone nearby indices, an additional exact shift residue X^delta
can be cheaper than constructing X^n from scratch.
"""
from __future__ import annotations
from collections import defaultdict
from sequence_recurrence_packets import _check, multiply_mod


class SparsePacketBank:
    def __init__(self,coefficients):
        _check(coefficients)
        self.coefficients=tuple(coefficients)
        d=len(coefficients)
        self.one=(1,)+tuple(0 for _ in range(d-1))
        self.powers=[tuple([coefficients[0]] if d==1 else [0,1]+[0]*(d-2))]
        self.cached={0:self.one}
        self.multiplications=0
        self.pow2_squarings=0
        self.misses=0
        self.gap_reuses=0
        self.last_index=0
        self.last_value=self.one

    def _mul(self,a,b):
        self.multiplications+=1
        return tuple(multiply_mod(list(a),list(b),list(self.coefficients)))

    def _ensure(self,highest_bit):
        while len(self.powers)<=highest_bit:
            self.powers.append(self._mul(self.powers[-1],self.powers[-1]))
            self.pow2_squarings+=1

    def _from_bits(self,n):
        if n==0:return self.one
        self._ensure(n.bit_length()-1)
        out=self.one
        for bit in range(n.bit_length()):
            if (n>>bit)&1:out=self._mul(out,self.powers[bit])
        return out

    def packet(self,n):
        if type(n) is not int or n<0:raise ValueError('invalid packet index')
        if n in self.cached:return self.cached[n]
        self.misses+=1
        # A shift by delta is exact in the quotient ring, even with a
        # repeated or zero characteristic root. No division is performed.
        delta=n-self.last_index
        if delta>0 and delta.bit_count()+1<n.bit_count():
            result=self._mul(self.last_value,self._from_bits(delta))
            self.gap_reuses+=1
        else:
            result=self._from_bits(n)
        self.cached[n]=result
        self.last_index=n
        self.last_value=result
        return result

    def terms(self,initial,indices):
        _check(self.coefficients,initial)
        return {n:sum(a*b for a,b in zip(self.packet(n),initial))
                for n in indices}

    def receipt(self):
        return {'order':len(self.coefficients),'distinct_exponents':len(self.cached),
                'powers_of_two_cached':len(self.powers),'ring_multiplications':self.multiplications,
                'pow2_squarings':self.pow2_squarings,
                'shift_reuses':self.gap_reuses}


def shared_sparse_terms(sequences,requested):
    """Evaluate multiple sequences at sparse indices, sharing a packet bank.

    sequences: {id:(initial,coefficients)}
    requested: {id:[n,...]} where index n is local to its recurrence definition.
    """
    if not isinstance(requested,dict):raise ValueError('request mapping required')
    groups=defaultdict(list)
    for sid,indices in requested.items():
        if sid not in sequences:raise ValueError('unknown sequence')
        initial,c=sequences[sid]
        _check(c,initial)
        ns=tuple(sorted(set(indices)))
        if any(type(n) is not int or n<0 for n in ns):raise ValueError('bad sparse index')
        groups[tuple(c)].append((sid,tuple(initial),ns))
    result={};receipts={}
    for c,rows in groups.items():
        bank=SparsePacketBank(c)
        union=sorted({n for sid,iv,indices in rows for n in indices})
        packets={n:bank.packet(n) for n in union}
        for sid,iv,indices in rows:
            for n in indices:
                result[(sid,n)]=sum(x*y for x,y in zip(iv,packets[n]))
        receipts[','.join(map(str,c))]=bank.receipt()
    return result,{'reused_recurrence_kernels':len(groups),
                   'output_term_count':len(result),'banks':receipts}
