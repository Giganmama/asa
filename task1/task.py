from typing import List, Tuple
from collections import deque

def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    # Разберём входную строку в ребра графа
    edges = [tuple(map(int, line.split(','))) for line in s.strip().split('\n')]
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    n = max(nodes)
    # Инициализация всех матриц n x n
    r1 = [[False]*n for _ in range(n)]  # непосредственное управление
    r2 = [[False]*n for _ in range(n)]  # непосредственное подчинение
    r3 = [[False]*n for _ in range(n)]  # опосредованное управление
    r4 = [[False]*n for _ in range(n)]  # опосредованное подчинение
    r5 = [[False]*n for _ in range(n)]  # соподчинение

    # Строим дерево и находим родителей для каждого узла, а также уровни
    tree = [[] for _ in range(n)]
    parents = [None] * n
    level = [None] * n
    for u, v in edges:
        tree[u-1].append(v-1)
        parents[v-1] = u-1

    # Найти уровни узлов и потомков каждого узла
    root = int(e)-1
    level[root] = 0
    queue = deque([root])
    while queue:
        cur = queue.popleft()
        for child in tree[cur]:
            level[child] = level[cur]+1
            queue.append(child)

    # Заполняем r1 и r2 (непосредственные связи)
    for u, v in edges:
        r1[u-1][v-1] = True
        r2[v-1][u-1] = True

    # Предварительно считаем всех предков (для опосредованных)
    ancestors = [set() for _ in range(n)]
    for v in range(n):
        cur = v
        while parents[cur] is not None:
            ancestors[v].add(parents[cur])
            cur = parents[cur]

    # Заполняем r3 и r4 (опосредованные)
    for v in range(n):
        for anc in ancestors[v]:
            if not r1[anc][v]:
                r3[anc][v] = True  # опосредованное управление
                r4[v][anc] = True  # опосредованное подчинение

    # Для r5 (соподчинение): общие непосредственные родители
    for i in range(n):
        for j in range(n):
            if i != j and parents[i] is not None and parents[j] is not None and parents[i] == parents[j]:
                r5[i][j] = True

    return (r1, r2, r3, r4, r5)
