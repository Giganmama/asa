from typing import Tuple, List
import math

def build_relations(s: str):
    edges = []
    vertices = set()

    for line in s.strip().splitlines():
        u, v = map(int, line.split(','))
        edges.append((u, v))
        vertices.add(u)
        vertices.add(v)

    vertices = sorted(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)

    parent = {v: None for v in vertices}
    children = {v: [] for v in vertices}

    for u, v in edges:
        parent[v] = u
        children[u].append(v)

    def empty():
        return [[False] * n for _ in range(n)]

    r1 = empty()
    r2 = empty()
    r3 = empty()
    r4 = empty()
    r5 = empty()

    for u, v in edges:
        r1[idx[u]][idx[v]] = True
        r2[idx[v]][idx[u]] = True

    for v in vertices:
        cur = parent[v]
        while cur is not None:
            if parent[v] != cur:
                r3[idx[cur]][idx[v]] = True
                r4[idx[v]][idx[cur]] = True
            cur = parent[cur]

    for p, ch in children.items():
        for i in ch:
            for j in ch:
                if i != j:
                    r5[idx[i]][idx[j]] = True

    return [r1, r2, r3, r4, r5]


def main(s: str, e: str) -> Tuple[float, float]:
    relations = build_relations(s)
    n = len(relations[0])
    k = len(relations)

    H = 0.0
    denom = n - 1

    for r in relations:
        for i in range(n):
            lij = sum(r[i])
            if lij == 0:
                continue
            p = lij / denom
            H += -p * math.log2(p)

    c = 1 / (math.e * math.log(2))
    H_ref = c * n * k

    return round(H, 1), round(H / H_ref, 1)
