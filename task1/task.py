from typing import List, Tuple

def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
]:
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

    r1 = empty()  # непосредственное управление
    r2 = empty()  # непосредственное подчинение
    r3 = empty()  # опосредованное управление
    r4 = empty()  # опосредованное подчинение
    r5 = empty()  # соподчинение

    # r1, r2
    for u, v in edges:
        i, j = idx[u], idx[v]
        r1[i][j] = True
        r2[j][i] = True

    # r3, r4
    for v in vertices:
        cur = parent[v]
        while cur is not None:
            if parent[v] != cur:
                r3[idx[cur]][idx[v]] = True
                r4[idx[v]][idx[cur]] = True
            cur = parent[cur]

    # r5
    for p, childs in children.items():
        for i in childs:
            for j in childs:
                if i != j:
                    r5[idx[i]][idx[j]] = True

    return r1, r2, r3, r4, r5
