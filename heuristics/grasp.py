import random
import numpy as np
import time

from common import read_data, calculate_objective, is_feasible

# Local search function (reuse the one from previous code)
def local_search(D, n, N, d, m, selected):
    best_solution = selected
    improved = True
    while improved:
        improved = False
        # Try swapping each selected member with others outside the solution set
        for i in range(len(best_solution)):
            for j in range(N):
                if j not in best_solution:
                    new_solution = best_solution[:]
                    new_solution[i] = j
                    # Check if the new solution is feasible
                    if is_feasible(D, n, N, d, m, new_solution):
                        current_objective = calculate_objective(D, n, N, d, m, best_solution)
                        new_objective = calculate_objective(D, n, N, d, m, new_solution)
                        if new_objective > current_objective:
                            best_solution = new_solution
                            improved = True
    return best_solution  # Move this outside the while loop

# Greedy construction phase with randomization
def greedy_construction_grasp(D, n, N, d, m, alpha=0.2):
    selected = []
    department_count = {dept: 0 for dept in range(1, D + 1)}

    members = list(range(N))
    
    while len(selected) < sum(n):
        candidate_list = []
        
        # Construct the restricted candidate list (RCL)
        for member in members:
            dept = d[member]
            if department_count[dept] < n[dept - 1]:
                # Check feasibility
                if all(m[member][other] > 0 for other in selected) and all(
                    m[member][other] >= 0.15 or
                    any(m[member][k] > 0.85 and m[k][other] > 0.85 for k in selected)
                    for other in selected
                ):
                    candidate_list.append(member)
        
        if not candidate_list:
            break
        
        # Select a candidate randomly from the RCL based on greedy criteria
        best_score = max(sum(m[member]) for member in candidate_list)
        best_candidates = [member for member in candidate_list if sum(m[member]) == best_score]
        selected_member = random.choice(best_candidates)
        
        selected.append(selected_member)
        department_count[d[selected_member]] += 1
        members.remove(selected_member)
        
    # Check if the length of selected matches the total required participants (sum of n)
    if len(selected) != sum(n):
        return None
    
    return selected

# GRASP main function
def grasp(D, n, N, d, m, iterations=100, alpha=0.2):
    best_solution = None
    best_objective = -float('inf')

    for _ in range(iterations):
        # Greedy construction phase with randomness
        initial_solution = greedy_construction_grasp(D, n, N, d, m, alpha)
        
        if initial_solution is None:
            continue
        
        # Local search phase
        local_best_solution = local_search(D, n, N, d, m, initial_solution)
        
        # Calculate objective value
        local_best_objective = calculate_objective(D, n, N, d, m, local_best_solution)

        # Update the best solution found
        if local_best_objective > best_objective:
            best_solution = local_best_solution
            best_objective = local_best_objective

    return best_solution, best_objective
