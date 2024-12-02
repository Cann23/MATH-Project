import numpy as np
import time
import argparse

from greedy import greedy_construction
from greedy_localSearch import local_search
from grasp import grasp
from common import read_data, calculate_objective

# Function to parse the command-line argument
def parse_args():
    parser = argparse.ArgumentParser(description="Heuristic algorithm runner.")
    parser.add_argument("algorithm", choices=["greedy", "local_search", "grasp"], help="Algorithm to execute")
    return parser.parse_args()  # Parse the arguments and return

# Your main code
def main():
    args = parse_args()  # Parse the command-line argument once
    for i in range(8):
        print(f"Running {args.algorithm} algorithm for project.{i+1}.dat")
        start_time = time.time()  # Start time measurement
        D, n, N, d, m = read_data(f"project.{i+1}.dat")
        
        # Common parts
        result = None
        objective = None
        final_result = None
        final_objective = None
        
        # Run the algorithm based on the argument
        if args.algorithm == 'greedy':
            result = greedy_construction(D, n, N, d, m)
            if result is not None:
                objective = calculate_objective(D, n, N, d, m, result)
                result = [x + 1 for x in result]
                print(f"Objective value for project.{i+1}.dat:", objective)
            print(f"Selected members for project.{i+1}.dat:", result)

        elif args.algorithm == 'local_search':
            result = greedy_construction(D, n, N, d, m)
            if result is not None:
                final_result, final_objective = local_search(D, n, N, d, m, result)
                final_result = [x + 1 for x in final_result]
                print(f"Objective value after local search for project.{i+1}.dat:", final_objective)
                print(f"Selected members after local search for project.{i+1}.dat:", final_result)
        
        elif args.algorithm == 'grasp':
            best_solution, best_objective = grasp(D, n, N, d, m, iterations=100, alpha=0.2)
            if best_solution is not None:
                best_solution = [x + 1 for x in best_solution]  # Convert to 1-based index
                print(f"Objective value after GRASP for project.{i+1}.dat:", best_objective)
                print(f"Selected members after GRASP for project.{i+1}.dat:", best_solution)
            else:
                print(f"No feasible solution found for project.{i+1}.dat")

        end_time = time.time()  # End time measurement
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Computation time for project.{i+1}.dat:", elapsed_time, "seconds")
        print("--------------------------------------------------")
        print()

if __name__ == "__main__":
    main()
