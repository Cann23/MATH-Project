import numpy as np
import time

# read the data from the file
def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # parsing values
    D = int(lines[0].split('=')[1].strip('; \n'))
    n = list(map(int, lines[1].split('=')[1].replace('[', '').replace(']', '').replace(';', '').split()))
    N = int(lines[3].split('=')[1].strip('; \n'))
    d = list(map(int, lines[4].split('=')[1].replace('[', '').replace(']', '').replace(';', '').split()))

    # Parse matrix m
    matrix_lines = lines[6:6+N]
    # Process matrix_lines
    processed_matrix = [
        list(map(float, line.replace('[', '').replace(']', '').replace(';', '').split()))
        for line in matrix_lines
    ]

    # Now create the NumPy array directly
    m = np.array(processed_matrix)

    return D, n, N, d, m

# calculate the objective value
def calculate_objective(D, n, N, d, m, selected):
    number_of_members = len(selected)
    number_of_pairs = number_of_members * (number_of_members - 1) // 2
    objective = sum(m[i][j] for i in selected for j in selected if i < j) / number_of_pairs
    return objective

# Feasibility check for the solution
def is_feasible(D, n, N, d, m, solution):
    # check if the size of selected members is correct (Constraint 2)
    if len(solution) != sum(n):
        return False
    
    # check if the number of members in each department is correct (Constraint 1)
    department_participantCount = {department: 0 for department in range(1, D + 1)}
    for member in solution:
            department = d[member]
            department_participantCount[department] += 1
            if department_participantCount[department] < n[department - 1]:
                # Check feasibility (Constraint 3 and 4)
                if not all(m[member][other] > 0 for other in solution) and all(
                    m[member][other] >= 0.15 or
                    any(m[member][k] > 0.85 and m[k][other] > 0.85 for k in solution)
                    for other in solution
                ):
                    return False
            else:
                return False
    return True