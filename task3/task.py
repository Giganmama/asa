import json
from typing import List, Union

Item = Union[int, str]
Cluster = List[Item]
Ranking = List[Union[Item, Cluster]]


def normalize(r: Ranking) -> List[Cluster]:

    res = []
    for x in r:
        if isinstance(x, list):
            res.append([str(i) for i in x])
        else:
            res.append([str(x)])
    return res


def build_matrix(clusters: List[Cluster]) -> dict:

    items = [i for c in clusters for i in c]
    pos = {}
    for idx, c in enumerate(clusters):
        for x in c:
            pos[x] = idx

    Y = {}
    for i in items:
        for j in items:
            Y[(i, j)] = 1 if pos[i] >= pos[j] else 0
    return Y, items


def main(a_json: str, b_json: str):
    A = normalize(json.loads(a_json))
    B = normalize(json.loads(b_json))

    YA, items = build_matrix(A)
    YB, _ = build_matrix(B)

    contradictions = []
    for i in items:
        for j in items:
            if i == j:
                continue
            if YA[(i, j)] == 0 and YB[(j, i)] == 0:
                pair = sorted([i, j])
                if pair not in contradictions:
                    contradictions.append(pair)

    clusters = [{i} for i in items]
    for i, j in contradictions:
        ci = next(c for c in clusters if i in c)
        cj = next(c for c in clusters if j in c)
        if ci is not cj:
            ci |= cj
            clusters.remove(cj)

    order = {x: idx for idx, c in enumerate(A) for x in c}
    clusters.sort(key=lambda c: min(order[x] for x in c))

    result = []
    for c in clusters:
        if len(c) == 1:
            result.append(int(next(iter(c))))
        else:
            result.append(sorted(int(x) for x in c))

    return result
