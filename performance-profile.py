import os
from utils import read_and_parse_files, findSmallestEvalTauSolved

ALGORITHM_DIRS = ["./Algo1", "./Algo2", "./Algo3"] 
TAU = 0.01

def compare_algorithms_tau_solved(parsed_data):
    """
    Determines which algorithm solves tau first for each file.
    """
    results = {}
    
    for file_num in range(1, 160): 
        file_name = f"stats{file_num}.txt"
        best_algorithm = None
        best_eval = float('inf')
        
        for algo_dir, parsed_values in parsed_data.items():
            if file_name not in parsed_values:
                continue
            
            eval_num = findSmallestEvalTauSolved(file_name, parsed_values, TAU)
            if eval_num is not None and eval_num < best_eval:
                best_eval = eval_num
                best_algorithm = algo_dir
        
        results[file_name] = best_algorithm if best_algorithm else "None"
    
    return results

def calculate_algorithm_ratios(results):
    """
    Calculates the percentage of problems solved first by each algorithm.
    """
    algo_counts = {algo: 0 for algo in ALGORITHM_DIRS}
    total_files = len(results)
    
    for best_algo in results.values():
        if best_algo in algo_counts:
            algo_counts[best_algo] += 1
    
    algo_ratios = {algo: round((count / total_files) * 100, 2) for algo, count in algo_counts.items()}
    return algo_ratios

def main():
    parsed_data = {algo_dir: read_and_parse_files(algo_dir) for algo_dir in ALGORITHM_DIRS}
    results = compare_algorithms_tau_solved(parsed_data)
    
    for file, best_algo in results.items():
        print(f"{file}: Solved first by {best_algo}")
    
    algo_ratios = calculate_algorithm_ratios(results)
    print("\nAlgorithm Performance Ratios:")
    for algo, ratio in algo_ratios.items():
        print(f"{algo}: {ratio}%")

if __name__ == "__main__":
    main()