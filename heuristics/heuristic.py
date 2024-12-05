import os
import time
import argparse
import numpy as np
import re

from greedy import greedy_construction
from greedy_localSearch import local_search
from grasp import grasp
from common import read_data, calculate_objective

# Function to parse the command-line argument
def parse_args():
    parser = argparse.ArgumentParser(description="Heuristic algorithm runner.")
    parser.add_argument("--config_file", help="Path to configuration file", default="config/config.dat")

    return parser.parse_args()  # Parse the arguments and return


def create_solution_folder():
    # Create the solutions folder if it does not exist
    if not os.path.exists("solutions"):
        os.makedirs("solutions")

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Yorum veya boş satırları atla
            if line.startswith('#') or line == '':
                continue
            key, value = line.split('=')
            # Otomatik veri tipi dönüşümü
            if value.isdigit():
                config[key] = int(value)
            elif value.replace('.', '', 1).isdigit():
                config[key] = float(value)
            elif value.lower() in ['true', 'false']:
                config[key] = value.lower() == 'true'
            else:
                config[key] = value
    return config


# Your main code
def main():
    arguments = parse_args()  # Parse the command-line argument once
    config = read_config(arguments.config_file)  # Read the configuration file
    create_solution_folder()  # Create the solutions folder if it does not exist

    start_time = time.time()  # Start time measurement
    # Read the instance data
    D, n, N, d, m = read_data(config["input_file"])


    # Initialize variables before using them
    solution = None
    objective = None


    # Run the algorithm based on the argument
    if config["algorithm"] == 'greedy':
        solution = greedy_construction(D, n, N, d, m)
        if solution is not None:
            objective = calculate_objective(D, n, N, d, m, solution)

    elif config["algorithm"] == 'local_search':
        solution = greedy_construction(D, n, N, d, m)
        if solution is not None:
            solution, objective = local_search(D, n, N, d, m, solution)

    elif config["algorithm"] == 'grasp':
        solution, objective = grasp(D, n, N, d, m, iterations=config["max_iterations"], alpha=config["alpha"])


    end_time = time.time()  # End time measurement
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    #sort the solution
    if solution is not None:
        # Make objective 2 decimal places
        objective = round(objective, 2)
        solution = [x + 1 for x in solution] # Convert the solution to 1-based index
        solution.sort()
    # Write the solution to the output file
    solution_file = config["solution_file"]
    with open(f"solutions/{solution_file}", "w") as f:
        if solution is not None:
            f.write("OBJECTIVE: " + str(objective) + "\n")
            f.write("Commission: ")
            f.write(" ".join(str(x) for x in solution))
        #close the file
        f.close()

    # Print the solution and other information
    if config["verbose"]:
        print("Algorithm:", config["algorithm"])
        print("Objective Value:", objective)
        print("Selected Members:", [x  for x in solution] if solution is not None else None)
        print("Computation Time:", elapsed_time, "seconds")


if __name__ == "__main__":
    main()
