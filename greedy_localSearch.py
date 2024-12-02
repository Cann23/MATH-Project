import numpy as np
import time

from common import read_data, calculate_objective

def local_search(D, n, N, d, m, selected):
    best_solution = selected
    best_objective = calculate_objective(D, n, N, d, m, best_solution)
    improved = True

    # Local search loop
    while improved:
        improved = False
        for i in range(len(selected)):
            for j in range(i + 1, len(selected)):
                # Swap members i and j to create a neighbor solution
                new_solution = best_solution[:]
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

                # Check the new objective
                new_objective = calculate_objective(D, n, N, d, m, new_solution)

                if new_objective > best_objective:
                    best_solution = new_solution
                    best_objective = new_objective
                    improved = True
                    break

        # Stop the search if no improvement
        if not improved:
            break

    return best_solution, best_objective
