# Compute the minimal set of indices required to bind any n-pattern
# in one hop.
#
# Based on https://stackoverflow.com/a/55148433/140837
#
# Taken from hoply.
import itertools
from math import factorial

from immutables import Map

import okdb as db


bc = lambda n, k: factorial(n) // factorial(k) // factorial(n - k) if k < n else 0


def stringify(iterable):
    return "".join(str(x) for x in iterable)


def combinations(tab):
    out = []
    for i in range(1, len(tab) + 1):
        out.extend(stringify(x) for x in itertools.combinations(tab, i))
    assert len(out) == 2 ** len(tab) - 1
    return out


def ok(solutions, tab):
    """Check that SOLUTIONS of TAB is a correct solution"""
    cx = combinations(tab)

    px = [stringify(x) for x in itertools.permutations(tab)]

    for combination in cx:
        pcx = ["".join(x) for x in itertools.permutations(combination)]
        # check for existing solution
        for solution in solutions:
            if any(solution.startswith(p) for p in pcx):
                # yeah, there is an existing solution
                break
        else:
            print("failed with combination={}".format(combination))
            break
    else:
        return True
    return False


def _compute_indices(n):
    tab = list(range(n))
    cx = list(itertools.combinations(tab, n // 2))
    for c in cx:
        L = [(i, i in c) for i in tab]
        A = []
        B = []
        while True:
            for i in range(len(L) - 1):
                if (not L[i][1]) and L[i + 1][1]:
                    A.append(L[i + 1][0])
                    B.append(L[i][0])
                    L.remove((L[i + 1][0], True))
                    L.remove((L[i][0], False))
                    break
            else:
                break
        l = [i for (i, _) in L]
        yield tuple(A + l + B)


def compute_indices(n):
    return list(_compute_indices(n))


# Taken from hoply/hoply.py

class Variable:

    __slots__ = ("name",)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<var %r>" % self.name


var = Variable


def stringify(list):
    return "".join(str(x) for x in list)


def is_permutation_prefix(combination, index):
    index = stringify(index)
    out = any(index.startswith(stringify(x)) for x in itertools.permutations(combination))
    return out


def init(name, prefix, n):
    out = dict(
        type="dbext",
        subtype="nstore2",
        name=name,
        prefix=prefix,
        indices=compute_indices(n),
    )
    return out


def add(cnx, nstore2, *items, value=None):
    for subspace, index in enumerate(nstore2["indices"]):
        permutation = list(items[i] for i in index)
        key = nstore2["prefix"] + [subspace] + permutation
        db.set(cnx, db.pack(key), value)


def delete(cnx, nstore2, *items):
    for subspace, index in enumerate(nstore2['indices']):
        permutation = list(items[i] for i in index)
        key = nstore2['prefix'] + [subspace] + permutation
        db.delete(cnx, db.pack(key))


def get(cnx, nstore2, *items):
    subspace = 0
    key = nstore2["prefix"] + [subspace] + list(items)
    out = db.get(cnx, db.pack(key))
    return out


def _from(cnx, nstore2, *pattern, seed=Map()):  # seed is immutable
    variable = tuple(isinstance(x, Variable) for x in pattern)
    # find the first index suitable for the query
    combination = tuple(x for x in range(len(pattern)) if not variable[x])
    for subspace, index in enumerate(nstore2["indices"]):
        if is_permutation_prefix(combination, index):
            break
    else:
        raise Exception("Oops! Mathematics failed!")
    # `index` variable holds the permutation suitable for the
    # query. `subspace` is the "prefix" of that index.
    prefix = list(pattern[i] for i in index if not isinstance(pattern[i], Variable))
    prefix = nstore2["prefix"] + [subspace] + prefix
    prefix = db.pack(prefix)
    db.unpack(prefix)
    for key, _ in db.query(cnx, prefix, db.next_prefix(prefix)):
        items = db.unpack(key)[len(nstore2["prefix"]) + 1:]
        # re-order the items
        items = tuple(items[index.index(i)] for i in range(len(pattern)))
        bindings = seed
        for i, item in enumerate(pattern):
            if isinstance(item, Variable):
                bindings = bindings.set(item.name, items[i])
        yield bindings


def _where(cnx, nstore2, iterator, pattern):
    for bindings in iterator:
        # bind PATTERN against BINDINGS
        bound = []
        for item in pattern:
            # if ITEM is variable try to bind
            if isinstance(item, Variable):
                try:
                    value = bindings[item.name]
                except KeyError:
                    # no bindings
                    bound.append(item)
                else:
                    # pick the value in bindings
                    bound.append(value)
            else:
                # otherwise keep item as is
                bound.append(item)
        # hey!
        yield from _from(cnx, nstore2, *bound, seed=bindings)


def query(cnx, nstore2, *patterns):
    out = _from(cnx, nstore2, *patterns[0])

    for pattern in patterns[1:]:
        out = _where(cnx, nstore2, out, pattern)

    return out
