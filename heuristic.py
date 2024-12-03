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
    parser.add_argument("algorithm", choices=["greedy", "local_search", "grasp"], help="Algorithm to execute")
    # Adding alpha-related arguments for GRASP
    parser.add_argument("--alpha_start", type=float, default=0.1, help="Starting value of alpha for GRASP tuning")
    parser.add_argument("--alpha_end", type=float, default=1.0, help="Ending value of alpha for GRASP tuning")
    parser.add_argument("--alpha_step", type=float, default=0.1, help="Step size for alpha tuning")
    return parser.parse_args()  # Parse the arguments and return

# Your main code
def main():
    args = parse_args()  # Parse the command-line argument once

    # Define the range for alpha when using GRASP
    if args.algorithm == 'grasp':
        alpha_values = np.arange(args.alpha_start, args.alpha_end + args.alpha_step, args.alpha_step)
    else:
        alpha_values = [None]  # For greedy and local_search, alpha is not used

    results_summary = []  # List to store results summary

    # Output folder where instances are located
    outputFolder = "instanceGenerator/output/"

    # Get the list of all files in the output folder
    instance_files = [f for f in os.listdir(outputFolder) if f.endswith(".dat")]

    # Sort files based on the number in the filename using regular expression
    instance_files = sorted(instance_files, key=lambda x: int(re.search(r'(\d+)', x).group(0)))

    # Iterate over each alpha value for GRASP, or just one iteration for greedy and local_search
    for alpha in alpha_values:
        print(f"Testing {args.algorithm} algorithm with alpha = {alpha if alpha is not None else 'N/A'}")
        alpha_results = {"alpha": alpha, "instances": []}

        # Iterate over each instance in the output folder
        for instance in instance_files:
            print(f"Running {args.algorithm} algorithm for {instance}")
            start_time = time.time()  # Start time measurement

            # Read the data for the instance
            D, n, N, d, m = read_data(f"{outputFolder}/{instance}")

            # Initialize variables before using them
            best_solution = None
            best_objective = None
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
                    print(f"Objective value for {instance}:", objective)
                    print(f"Selected members for {instance}:", result)

            elif args.algorithm == 'local_search':
                result = greedy_construction(D, n, N, d, m)
                if result is not None:
                    final_result, final_objective = local_search(D, n, N, d, m, result)
                    final_result = [x + 1 for x in final_result]
                    print(f"Objective value after local search for {instance}:", final_objective)
                    print(f"Selected members after local search for {instance}:", final_result)

            elif args.algorithm == 'grasp':
                best_solution, best_objective = grasp(D, n, N, d, m, iterations=100, alpha=alpha)
                if best_solution is not None:
                    best_solution = [x + 1 for x in best_solution]  # Convert to 1-based index
                    print(f"Objective value after GRASP for {instance}:", best_objective)
                    print(f"Selected members after GRASP for {instance}:", best_solution)
                else:
                    print(f"No feasible solution found for {instance}")

            end_time = time.time()  # End time measurement
            elapsed_time = end_time - start_time  # Calculate the elapsed time
            print(f"Computation time for {instance}:", elapsed_time, "seconds")
            print("--------------------------------------------------")

            # Store results for this instance
            instance_result = {
                "instance": instance,
                "objective_value": best_objective if best_solution is not None else None,
                "feasible": best_solution is not None,
                "computation_time": elapsed_time,
                "selected_members": [x + 1 for x in best_solution] if best_solution is not None else None,
            }
            alpha_results["instances"].append(instance_result)

        # Append results for this alpha
        results_summary.append(alpha_results)

    # Print or save the summary of all results
    print("\nSummary of Results:")
    for alpha_result in results_summary:
        alpha = alpha_result["alpha"]
        feasible_count = sum(1 for r in alpha_result["instances"] if r["feasible"])
        total_instances = len(alpha_result["instances"])

        # Check if there are any feasible solutions
        feasible_solutions = [r["objective_value"] for r in alpha_result["instances"] if r["feasible"]]

        # Only calculate average if there are feasible solutions
        avg_objective = np.mean(feasible_solutions) if feasible_solutions else None
        avg_time = np.mean([r["computation_time"] for r in alpha_result["instances"]]) if feasible_solutions else None

        print(f"Alpha = {alpha if alpha is not None else 'N/A'}")
        print(f"  - Feasibility Rate: {feasible_count}/{total_instances} ({(feasible_count / total_instances) * 100:.2f}%)")
        print(f"  - Average Objective Value: {avg_objective if avg_objective is not None else 'N/A'}")
        print(f"  - Average Computation Time: {avg_time if avg_time is not None else 'N/A'} seconds")
        print("--------------------------------------------------")


if __name__ == "__main__":
    main()
