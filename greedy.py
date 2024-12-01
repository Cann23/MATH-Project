import numpy as np
import time

from common import read_data

def greedy_construction(D, n, N, d, m):
    selected = []
    department_count = {dept: 0 for dept in range(1, D + 1)}

    members = sorted(range(N), key=lambda i: -sum(m[i]))

    for member in members:
        dept = d[member]

        if department_count[dept] < n[dept - 1]:
            # Check feasibility of adding this member
            if all(m[member][other] > 0 for other in selected) and all(
                m[member][other] >= 0.15 or
                any(m[member][k] > 0.85 and m[k][other] > 0.85 for k in selected)
                for other in selected
            ):
                selected.append(member)
                department_count[dept] += 1

        # If the algorithm cannot find enough participants for a department
        if department_count[dept] < n[dept - 1] and not any(
            all(m[cand][other] > 0 for other in selected) and all(
                m[cand][other] >= 0.15 or
                any(m[cand][k] > 0.85 and m[k][other] > 0.85 for k in selected)
                for other in selected
            ) for cand in range(N) if d[cand] == dept
        ):
            print(f"No feasible solution for department {dept}.")
            return None

        if len(selected) == sum(n):
            break

    # Check if a complete solution is found
    if len(selected) < sum(n):
        print("No feasible solution for the problem.")
        return None

    return selected