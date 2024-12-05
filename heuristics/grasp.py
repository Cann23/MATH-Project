import random
from greedy_localSearch import local_search

# Greedy construction phase with randomization
def greedy_construction_grasp(D, n, N, d, m, alpha=0.2):
    partial_solution = []
    department_participantCount = {dept: 0 for dept in range(1, D + 1)}

    # Calculate the sum of compatibilities for each member
    compatibilities = [sum(m[i]) for i in range(N)]

    # Sort members by compatibilities in descending order
    candidates = sorted(range(N), key=lambda i: compatibilities[i], reverse=True)
    
    while len(partial_solution) < sum(n) and candidates:
        # Calculate RCL (Restricted Candidate List)
        max_compatibility = compatibilities[candidates[0]]
        min_compatibility = compatibilities[candidates[-1]]

        # Create RCL with members within alpha of the best compatibility
        rcl_max = [
            member for member in candidates 
            if compatibilities[member] >= max_compatibility - alpha * (max_compatibility - min_compatibility)
        ]
        
        # Randomly select a member from RCL
        selected_member = random.choice(rcl_max)
        
        #detemine the department of the selected member
        department = d[selected_member]
        
        # Check if the department has reached its limit
        if department_participantCount[department] < n[department - 1]:
            # Check compatibility constraints
            if (all(m[selected_member][other] > 0 for other in partial_solution) and 
                all(m[selected_member][other] >= 0.15 or 
                    any(m[selected_member][k] > 0.85 and m[k][other] > 0.85 for k in partial_solution)
                    for other in partial_solution)):
                
                # Add the selected member to the solution
                partial_solution.append(selected_member)
                department_participantCount[department] += 1
        
        # Remove the selected member from the candidate list
        candidates.remove(selected_member)
    
    # Check if the solution is feasible
    if len(partial_solution) < sum(n):
        return None
    
    return partial_solution

# GRASP main function
def grasp(D, n, N, d, m, iterations=100, alpha=0.2):
    best_solution = None
    best_objective = -float('inf')

    for _ in range(iterations):
        # Greedy construction phase with randomness
        initial_solution = greedy_construction_grasp(D, n, N, d, m, alpha)

        # Check if the solution is feasible
        if initial_solution is None:
            continue
        
        # Local search phase
        local_best_solution,local_best_objective = local_search(D, n, N, d, m, initial_solution)

        # Update the best solution found
        if local_best_objective > best_objective:
            best_solution = local_best_solution
            best_objective = local_best_objective

    return best_solution, best_objective
