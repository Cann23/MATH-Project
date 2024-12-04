import numpy as np
import time

from common import read_data

def greedy_construction(D, n, N, d, m):
    partial_solution = []
    department_participantCount = {department: 0 for department in range(1, D + 1)}

    # calculate the sum of the compatibilities of each member
    compatibilities = [sum(m[i]) for i in range(N)]
    # sort the members in decreasing order of their sum of compatibilities
    members = sorted(range(N), key=lambda i: compatibilities[i], reverse=True)

    for member in members:
        department = d[member]

        # Check if the department has reached its limit (constraint 1)
        if department_participantCount[department] < n[department - 1]:
            # Check compatibility with the partial_solution members (constraint 2 and 3)
            if all(m[member][other] > 0 for other in partial_solution) and all(
                m[member][other] >= 0.15 or
                any(m[member][k] > 0.85 and m[k][other] > 0.85 for k in partial_solution)
                for other in partial_solution
            ):
                partial_solution.append(member)
                department_participantCount[department] += 1

        # Check if a complete solution is found (constraint 1)
        if len(partial_solution) == sum(n):
            break

    # Check if a feasible solution is found
    if len(partial_solution) < sum(n):
        print("No feasible solution for the problem.")
        return None

    return partial_solution