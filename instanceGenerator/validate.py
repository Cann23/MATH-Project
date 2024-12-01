from itertools import combinations

def is_valid(instance):
    D, N, n, d, m = instance['D'], instance['N'], instance['n'], instance['d'], instance['m']
    selected = select_commission(D, n, d, m)
    return selected is not None

def select_commission(D, n, d, m):
    candidates = [i for i in range(len(d))]

    for selected in combinations(candidates, sum(n)):
        department_count = [0] * D
        for i in selected:
            department_count[d[i] - 1] += 1

        if department_count != n:
            continue

        if any(m[i][j] == 0 for i, j in combinations(selected, 2)):
            continue

        if not all(
            any(m[i][k] > 0.85 and m[j][k] > 0.85 for k in selected if k != i and k != j)
            for i, j in combinations(selected, 2) if 0 < m[i][j] < 0.15
        ):
            continue

        return selected
    return None
