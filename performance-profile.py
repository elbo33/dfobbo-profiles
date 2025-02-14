import os
from utils import read_and_parse_files, findSmallestEvalTauSolved

ALGORITHM_DIRS = ["./Algo1", "./Algo2", "./Algo3"] 
TAU = 0.1

def compare_algorithms_tau_solved():
    """
    Determines which algorithm solves tau first for each file.
    Keeps track of the smallest tau solved value for each algorithm at each iteration.
    """
    parsed_data = {algo_dir: read_and_parse_files(algo_dir) for algo_dir in ALGORITHM_DIRS}
    results = {}
    eval_counts = {algo_dir: [] for algo_dir in ALGORITHM_DIRS}
    min_tau_solved = {algo_dir: [] for algo_dir in ALGORITHM_DIRS}  
    
    for file_num in range(1, 160): 
        file_name = f"stats{file_num}.txt"
        best_eval = float('inf')
        evals = {}
        
        for algo_dir, parsed_values in parsed_data.items():
            if file_name not in parsed_values:
                continue
            
            eval_num = findSmallestEvalTauSolved(file_name, parsed_values, TAU)
            if eval_num is not None:
                evals[algo_dir] = eval_num
                best_eval = min(best_eval, eval_num)
                min_tau_solved[algo_dir].append(eval_num)  
        
        results[file_name] = evals
        for algo_dir, eval_num in evals.items():
            eval_counts[algo_dir].append(eval_num / best_eval if best_eval > 0 else 1)
    
    return results, min_tau_solved

def calculate_algorithm_ratios(min_tau_solved):
    """
    Calculates the ratio of each algorithm's min tau solved value compared to the global min tau at each iteration.
    Returns a list of ratios for each algorithm over all iterations.
    """
    algo_ratios = {algo: [] for algo in ALGORITHM_DIRS}
    
    num_iterations = max(len(values) for values in min_tau_solved.values())
    
    for i in range(num_iterations):
        global_min = float('inf')
        current_values = {}
        
        for algo in ALGORITHM_DIRS:
            if i < len(min_tau_solved[algo]):
                current_values[algo] = min_tau_solved[algo][i]
                global_min = min(global_min, min_tau_solved[algo][i])
        
        if global_min == float('inf'):
            continue
        
        for algo in ALGORITHM_DIRS:
            if i < len(min_tau_solved[algo]):
                algo_ratios[algo].append(min_tau_solved[algo][i] / global_min if global_min > 0 else 1)
    
    return algo_ratios

def calculate_percentage_below_alpha(algo_ratios, alpha):
    """
    Calculates the percentage of ratios per algorithm that are smaller than alpha.
    """
    percentage_below_alpha = {}
    
    for algo, ratios in algo_ratios.items():
        count_below_alpha = sum(1 for ratio in ratios if ratio <= alpha)
        percentage_below_alpha[algo] = (count_below_alpha / len(ratios)) * 100 if ratios else 0
    
    return percentage_below_alpha

def main():
    results, min_tau_solved = compare_algorithms_tau_solved()
    
    for file, evals in results.items():
        best_algo = min(evals, key=evals.get, default="None")
        print(f"{file}: Solved first by {best_algo}")
    
    algo_ratios = calculate_algorithm_ratios(min_tau_solved)
    print("\nAlgorithm Performance Ratios per Iteration:")
    for algo, ratios in algo_ratios.items():
        print(f"{algo}: {ratios}")
    
    alpha = 1.0 
    percentages = calculate_percentage_below_alpha(algo_ratios, alpha)
    print(f"\nPercentage of Ratios Below Alpha <= {alpha}")
    for algo, percentage in percentages.items():
        print(f"{algo}: {percentage}%")

if __name__ == "__main__":
    main()
