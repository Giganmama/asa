import json
from typing import List

def membership(x: float, points: List[List[float]]) -> float:
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= x <= x2 or x2 <= x <= x1:
            if x1 == x2:
                return max(y1, y2)
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return 0.0


def main(
    temp_json: str,
    heat_json: str,
    rules_json: str,
    temperature: float
) -> float:

    temp_data = json.loads(temp_json)["температура"]
    heat_data = json.loads(heat_json)["температура"]
    rules = json.loads(rules_json)

    temp_mu = {}
    for term in temp_data:
        temp_mu[term["id"]] = membership(temperature, term["points"])

    all_points = []
    for term in heat_data:
        for p in term["points"]:
            all_points.append(p[0])

    s_min, s_max = min(all_points), max(all_points)

    step = 0.1
    s_values = [
        round(s_min + i * step, 2)
        for i in range(int((s_max - s_min) / step) + 1)
    ]

    mu_out = {s: 0.0 for s in s_values}

    heat_terms = {t["id"]: t["points"] for t in heat_data}

    for temp_term, heat_term in rules:
        activation = temp_mu.get(temp_term, 0.0)
        if activation == 0:
            continue

        for s in s_values:
            mu = membership(s, heat_terms[heat_term])
            mu_out[s] = max(mu_out[s], min(activation, mu))

    max_mu = max(mu_out.values())
    eps = 1e-6

    for s in s_values:
        if abs(mu_out[s] - max_mu) < eps:
            return s

    return 0.0
