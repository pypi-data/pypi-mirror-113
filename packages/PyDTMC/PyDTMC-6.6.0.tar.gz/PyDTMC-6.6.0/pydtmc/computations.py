# -*- coding: utf-8 -*-

__all__ = [
    'calculate_periods',
    'eigenvalues_sorted',
    'find_cyclic_classes',
    'find_lumping_partitions',
    'gth_solve',
    'rdl_decomposition',
    'slem'
]


###########
# IMPORTS #
###########

# Standard

from itertools import (
    chain
)

from math import (
    gcd
)

# Libraries

import networkx as nx
import numpy as np
import numpy.linalg as npl

# Internal

from .custom_types import (
    ofloat,
    tarray,
    tgraph,
    tlist_int,
    tparts,
    trdl
)


#############
# FUNCTIONS #
#############

def _calculate_period(graph: tgraph) -> int:

    g = 0

    for scc in nx.strongly_connected_components(graph):

        scc = list(scc)

        levels = {scc: None for scc in scc}
        vertices = levels.copy()

        x = scc[0]
        levels[x] = 0

        current_level = [x]
        previous_level = 1

        while current_level:

            next_level = []

            for u in current_level:
                for v in graph[u]:

                    if v not in vertices:  # pragma: no cover
                        continue

                    level = levels[v]

                    if level is not None:

                        g = gcd(g, previous_level - level)

                        if g == 1:
                            return 1

                    else:

                        next_level.append(v)
                        levels[v] = previous_level

            current_level = next_level
            previous_level += 1

    return g


def calculate_periods(graph: tgraph) -> tlist_int:

    sccs = list(nx.strongly_connected_components(graph))

    classes = [sorted(scc) for scc in sccs]
    indices = sorted(classes, key=lambda x: (-len(x), x[0]))

    periods = [0] * len(indices)

    for scc in sccs:

        scc_reachable = scc.copy()

        for c in scc_reachable:
            spl = nx.shortest_path_length(graph, c).keys()
            scc_reachable = scc_reachable.union(spl)

        index = indices.index(sorted(scc))

        if (scc_reachable - scc) == set():
            periods[index] = _calculate_period(graph.subgraph(scc))
        else:
            periods[index] = 1

    return periods


def eigenvalues_sorted(m: tarray) -> tarray:

    ev = npl.eigvals(m)
    ev = np.sort(np.abs(ev))

    return ev


def find_cyclic_classes(p: tarray) -> tarray:

    size = p.shape[0]

    v = np.zeros(size, dtype=int)
    v[0] = 1

    w = np.array([], dtype=int)
    t = np.array([0], dtype=int)

    d = 0
    m = 1

    while (m > 0) and (d != 1):

        i = t[0]
        j = 0

        t = np.delete(t, 0)
        w = np.append(w, i)

        while j < size:

            if p[i, j] > 0.0:
                r = np.append(w, t)
                k = np.sum(r == j)

                if k > 0:
                    b = v[i] - v[j] + 1
                    d = gcd(d, b)
                else:
                    t = np.append(t, j)
                    v[j] = v[i] + 1

            j += 1

        m = t.size

    v = np.remainder(v, d)

    indices = []

    for u in np.unique(v):
        indices.append(list(chain.from_iterable(np.argwhere(v == u))))

    return indices


def find_lumping_partitions(p: tarray) -> tparts:

    size = p.shape[0]

    if size == 2:
        return []

    k = size - 1
    indices = list(range(size))

    possible_partitions = []

    for i in range(2**k):

        partition = []
        subset = []

        for position in range(size):

            subset.append(indices[position])

            if ((1 << position) & i) or position == k:
                partition.append(subset)
                subset = []

        partition_length = len(partition)

        if 2 <= partition_length < size:
            possible_partitions.append(partition)

    partitions = []

    for partition in possible_partitions:

        r = np.zeros((size, len(partition)), dtype=float)

        for index, lumping in enumerate(partition):
            for state in lumping:
                r[state, index] = 1.0

        # noinspection PyBroadException
        try:
            k = np.dot(np.linalg.inv(np.dot(np.transpose(r), r)), np.transpose(r))
        except Exception:  # pragma: no cover
            continue

        left = np.dot(np.dot(np.dot(r, k), p), r)
        right = np.dot(p, r)
        is_lumpable = np.array_equal(left, right)

        if is_lumpable:
            partitions.append(partition)

    return partitions


def gth_solve(p: tarray) -> tarray:

    a = np.copy(p)
    n = a.shape[0]

    for i in range(n - 1):

        scale = np.sum(a[i, i + 1:n])

        if scale <= 0.0:  # pragma: no cover
            n = i + 1
            break

        a[i + 1:n, i] /= scale
        a[i + 1:n, i + 1:n] += np.dot(a[i + 1:n, i:i + 1], a[i:i + 1, i + 1:n])

    x = np.zeros(n, dtype=float)
    x[n - 1] = 1.0

    for i in range(n - 2, -1, -1):
        x[i] = np.dot(x[i + 1:n], a[i + 1:n, i])

    x /= np.sum(x)

    return x


def rdl_decomposition(p: tarray) -> trdl:

    values, vectors = npl.eig(p)

    indices = np.argsort(np.abs(values))[::-1]
    values = values[indices]
    vectors = vectors[:, indices]

    r = np.copy(vectors)
    d = np.diag(values)
    l = npl.solve(np.transpose(r), np.eye(p.shape[0], dtype=float))  # noqa

    k = np.sum(l[:, 0])

    if not np.isclose(k, 0.0):
        r[:, 0] *= k
        l[:, 0] /= k

    r = np.real(r)
    d = np.real(d)
    l = np.transpose(np.real(l))  # noqa

    return r, d, l


def slem(m: tarray) -> ofloat:

    ev = eigenvalues_sorted(m)
    value = ev[~np.isclose(ev, 1.0)][-1]

    if np.isclose(value, 0.0):
        return None

    return value
