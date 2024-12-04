import numpy as np
import time

from common import read_data, calculate_objective, is_feasible

def local_search(D, n, N, d, m, solution):
    # Initialize the best solution and objective
    best_solution = solution
    best_objective = calculate_objective(D, n, N, d, m, best_solution)
    is_improved = True

    # Local search loop
    while is_improved:
        is_improved = False
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                # for finding neighbor solution swap members i and j in the solution 
                new_solution = best_solution[:]
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

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
