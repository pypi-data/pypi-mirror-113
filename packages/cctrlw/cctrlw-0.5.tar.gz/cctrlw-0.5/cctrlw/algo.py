from typing import Iterable, Generic, TypeVar, Dict, List
from string import printable as _P
from itertools import chain
import sys
from json import loads
from typing import Dict

X = TypeVar('X')
START = 'S'


class dsu(Generic[X]):
    """
    https://en.wikipedia.org/wiki/Disjoint-set_data_structure
    Some implementations here have bad asymptotic complexity, that's ok:
    sets this dsu will be used on are comically small.
    """
    def __init__(self,
                 initial_U: Iterable[X] = None,
                 _copy_entries: Dict[X, X] = None):
        self.p = {
            **{x: x
               for x in initial_U or {}},
            **(_copy_entries or {})
        }

    def _ensure_exist(self, x: X) -> X:
        return self.p.setdefault(x, x)

    def as_set_of_sets(self, set=frozenset) -> Iterable[Iterable[X]]:
        R = {}
        for u in list(self.p.keys()):
            v = self._find(u)
            R.setdefault(
                v,
                {
                    v,
                },
            ).add(u)
        return set(set(S) for S in R.values())

    def get_U(self, set=frozenset) -> Iterable[X]:
        S = self.as_set_of_sets(set)
        if S:
            return set.union(*S)
        else:
            return set()

    def get_set_of(self, y, set=frozenset):
        S = self.as_set_of_sets()
        for x in S:
            if y in x:
                return x
        return set({
            y,
        })

    def __repr__(self):
        P = set(_P.encode("utf-8"))
        S, R, t_card, U = self.as_set_of_sets(), [], 0, self.get_U()
        for cur_set in S:
            ss = list(sorted(cur_set))
            if len(ss) == 1:
                continue

            def rep_byte(x):
                c = bytes((x, )).decode("utf-8")
                return f"'{c}'" if x in P else x

            runs, i = [0], 0
            while i != len(ss):
                j = i
                while j < len(ss) and ss[j] == ss[i] + j - i:
                    j += 1
                # [i, j)
                runs.append(j)
                i = j
            r = []
            for i, j in zip(runs, runs[1:]):
                assert j - i > 0
                if j - i == 1:
                    r.append(rep_byte(ss[i]))
                else:
                    r.append(f"{rep_byte(ss[i])}:{rep_byte(ss[j - 1])}")
            r = ", ".join(r)
            r = f'{{{r}}}'
            R.append(r)
            t_card += len(ss)
        singletons = len(U) - t_card
        if singletons:
            R.append(f"<{singletons} singletons ignored>")
        return f"{{{', '.join(R)}}}"

    def union_two(self, x: X, y: X):
        """
          Union __sets__ containing x and y.
        """
        for z in (x, y):
            if z not in self.p:
                self.p[z] = z
        self.p[self._find(x)] = self._find(y)

    def union(self, head: X, *tail: Iterable[X]):
        for x in tail:
            self.union_two(head, x)

    def _find(self, x: X):
        self.p.setdefault(x, x)
        if self.p[x] == x:
            return x
        self.p[x] = self._find(self.p[x])
        return self.p[x]

    def clone(self) -> 'dsu[X]':
        return dsu(_copy_entries=self.p)

    def equiv(self, x: X, y: X) -> bool:
        for z in (x, y):
            if z not in self.p:
                self.p[z] = z
        return self._find(x) == self._find(y)


def topsort(adj: Dict[X, List[X]]) -> List[X]:
    """
    Return a topological sort of a DAG defined by adjacency list `adj`.
    """
    used, V = {}, set()
    for u, v in adj.items():
        V.update(chain(v, (u, )))
    for u in V:
        used[u] = 0
        if u not in adj:
            adj[u] = []
    stack = []
    def dfs_run(u, g):
        if used[u] == 2:
            return
        if used[u] == 1:
            raise ValueError(
                f'there\' a cyclic dependency: {" -> ".join(str(x) for x in chain(stack, [u]))}'
            )
        used[u] = 1
        stack.append(u)
        for v in g[u]:
            yield from dfs_run(v, g)
        yield u
        stack.pop()
        used[u] = 2

    ts = []
    for v in V:
        if len(adj[v]) == 1 and not used[v]:
            ts.extend(dfs_run(v, adj))
    ts.reverse()

    ord = {v: i for i, v in enumerate(ts)}
    for u, v in zip(ts[0:], ts[1:]):
        assert (
            ord[u] < ord[v]
        ), "somebody couldn't write a correct topsort; this is a bug, report it"
    return ts


def load_partitions(definitions) -> Dict[str, dsu]:
    """
    Partition <-> dsu.

    How to define partitions?

    One could simply enumerate them as sets of sets in a json every time, but there's a (subjectively) better approach, which allows to specify them without copy-pasting, in a consice and clean fashion.

    Say we already have a partition M (named m, stored in dsu d_M), and want to derive from it a new partition M', which is strictly less fine than M. In M' we want to copy M and union sets containing letters u_1 and v_1, sets containing u_2 and v_2, etc.

    So config entry that defines M looks as following:
      M := (m, [(u_i, v_i)...]).

    The base case is the partition 'S', which is the partition into singletons.

    There are several approaches to turn config entries into dsus: one used here is to build partitions in the order of some topological sort of the dependency graph, this way it is guaranteed that the dsu for parent is already constructed by the time it is needed for the child to copy. Also, it checks for cyclic dependencies, and prints a cycle if it is found, raising an exception.

    One could also do a lazy dp with memoization.
    """
    adj, parent, diff = {}, {}, {}
    for v, (u, d) in definitions.items():
        adj.setdefault(u, []).append(v)
        parent[v], diff[v] = u, d
    S, ts, parts = dsu(), topsort(adj), {}
    for x in range(2**8):
        S.union_two(x, x)
    parts[START] = S
    for part_name in ts:
        if part_name == START:
            continue
        m = parts[parent[part_name]].clone()
        for u, v in diff[part_name]:
            m.union(u, v)
        parts[part_name] = m
    return parts


def get_streak(s: str, m: dsu) -> int:
    """Return the length of largest prefix of s that has letters equivalent to first letter with regards to partition m.
    """
    L = 0
    while L < len(s) and m.equiv(s[0], s[L]):
        L += 1
    return L
