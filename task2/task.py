from typing import Tuple
import math

def task(s: str, e: str) -> Tuple[float, float]:
    edges = [tuple(map(int, line.strip().split(','))) for line in s.strip().split('
')]
    elements = set()
    for u, v in edges:
        elements.add(u)
        elements.add(v)
    elements = sorted(list(elements))
    n = len(elements)

    r1 = set(edges)
    r2 = set((v, u) for u, v in edges)

    from collections import defaultdict, deque

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    node_level = {}
    root = int(e)
    queue = deque()
    queue.append((root, 0))
    node_level[root] = 0
    while queue:
        node, lvl = queue.popleft()
        node_level[node] = lvl
        for nei in graph.get(node, []):
            if nei not in node_level:
                queue.append((nei, lvl + 1))

    def descendants(node):
        desc = set()
        stack = [node]
        while stack:
            curr = stack.pop()
            for nei in graph.get(curr, []):
                if nei not in desc:
                    desc.add(nei)
                    stack.append(nei)
        desc -= set(graph.get(node, []))  
        return desc

    r3 = set()
    for u in elements:
        for v in descendants(u):
            r3.add((u, v))
    
    r4 = set((v, u) for (u, v) in r3)

    r5 = set()
    level_groups = defaultdict(list)
    for node, lvl in node_level.items():
        level_groups[lvl].append(node)
    for group in level_groups.values():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                r5.add((group[i], group[j]))
                r5.add((group[j], group[i]))

    relations = [r1, r2, r3, r4, r5]
    k = len(relations)
    
    l = {mj: [0]*k for mj in elements}
    for rel_idx, rel in enumerate(relations):
        for (u, v) in rel:
            l[u][rel_idx] += 1

    entropies = {}
    max_links = n - 1   
    for mj in elements:
        Hm = 0
        for rel_idx in range(k):
            lij = l[mj][rel_idx]
            if lij == 0:
                continue
            P = lij / max_links
            H = -P * math.log2(P)
            Hm += H
        entropies[mj] = Hm

    H_total = sum(entropies.values())

    c = 1 / (math.e * math.log(2))
    H_ref = c * n * k

    h_norm = H_total / H_ref if H_ref > 0 else 0
    return (round(H_total, 1), round(h_norm, 2))
