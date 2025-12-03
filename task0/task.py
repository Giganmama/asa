
import csv
from io import StringIO

def main(csv_string):
    reader = csv.reader(StringIO(csv_string), delimiter=',')
    edges = []
    header_skipped = False
    for row in reader:
        if not header_skipped:
            header_skipped = True
            continue
        edges.append((int(row[0]), int(row[1])))
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    n = max(nodes)
    matrix = [[0]*n for _ in range(n)]
    for u, v in edges:
        matrix[u-1][v-1] = 1
        matrix[v-1][u-1] = 1
    return matrix
