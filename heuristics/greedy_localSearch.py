import numpy as np
import time

from common import read_data, calculate_objective, is_feasible

def local_search(D, n, N, d, m, solution):
    # Initialize the best solution and objective
    best_solution = solution
    best_objective = calculate_objective(D, n, N, d, m, best_solution)
    is_improved = True

    # Local search loop - reassignment neighborhood (one element exchange)
    while is_improved:
        is_improved = False
        for i in range(len(solution)):
            current_member = best_solution[i]
            current_department = d[current_member]

            for j in range(N):
                # Check if the member is in the solution or belongs to the same department
                if j in best_solution or d[j] != current_department:
                    continue
                
                # Create a new solution by replacing the current member with j
                new_solution = best_solution[:]
                new_solution[i] = j

                # check the new solution is feasible
                if is_feasible(D, n, N, d, m, new_solution):
                    # Check the new objective
                    new_objective = calculate_objective(D, n, N, d, m, new_solution)

                    if new_objective > best_objective:
                        best_solution = new_solution
                        best_objective = new_objective
                        is_improved = True
                        break
                
    return best_solution, best_objective
