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