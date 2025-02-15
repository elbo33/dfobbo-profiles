import sys
from utils import *

def compare_algorithms_tau_solved(tau):
    """
    Determines which algorithm solves tau first for each file.
    Keeps track of the smallest tau solved value for each algorithm at each iteration.
    """
    parsed_data = load_parsed_data()
    min_tau_solved = {algo_dir: [] for algo_dir in ALGORITHM_DIRS}  
    
    for file_num in range(1, 160): 
        file_name = f"stats{file_num}.txt"
        evals = {}
        best_eval = float('inf')

        for algo_dir, parsed_values in parsed_data.items():
            eval_num = findSmallestEvalTauSolved(file_name, parsed_values, tau)
            evals[algo_dir] = eval_num  
            
            if eval_num != float('inf'):  
                best_eval = min(best_eval, eval_num)

        for algo_dir, eval_num in evals.items():
            min_tau_solved[algo_dir].append(eval_num)  

    return min_tau_solved


def calculate_algorithm_ratios(min_tau_solved):
    """
    Calculates the ratio of each algorithm's min tau solved value compared to the global min tau at each iteration.
    Returns a list of ratios for each algorithm over all iterations.
    If an algorithm doesn't solve tau in an iteration, writes 'inf'.
    """
    algo_ratios = {algo: [] for algo in ALGORITHM_DIRS}
    
    num_iterations = max(len(values) for values in min_tau_solved.values())

    for i in range(num_iterations):
        current_values = {
            algo: min_tau_solved[algo][i] 
            for algo in ALGORITHM_DIRS if i < len(min_tau_solved[algo]) and min_tau_solved[algo][i] != float('inf')
        }

        global_min = min(current_values.values()) if current_values else float('inf')

        for algo in ALGORITHM_DIRS:
            if i < len(min_tau_solved[algo]):
                if min_tau_solved[algo][i] == float('inf') or global_min == float('inf'):
                    algo_ratios[algo].append("inf") 
                else:
                    algo_ratios[algo].append(min_tau_solved[algo][i] / global_min if global_min > 0 else 1)
    
    return algo_ratios

def calculate_percentage_below_alpha(algo_ratios, alpha_range):
    """
    Calculates the percentage of ratios per algorithm that are smaller than different alpha values.

    """
    percentages_below_alpha = {alpha: {} for alpha in range(1, alpha_range)}

    for alpha in range(1, alpha_range):
        for algo, ratios in algo_ratios.items():
            valid_ratios = [float(ratio) for ratio in ratios if ratio != "inf"]
            count_below_alpha = sum(1 for ratio in valid_ratios if ratio <= alpha)
            
            percentages_below_alpha[alpha][algo] = (count_below_alpha / len(ratios)) * 100 if valid_ratios else 0

    return percentages_below_alpha

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <tau> <alpha>")
        sys.exit(1)
    tau = float(sys.argv[1])
    alpha = int(sys.argv[2])
    min_tau_solved = compare_algorithms_tau_solved(tau)
    algo_ratios = calculate_algorithm_ratios(min_tau_solved)
    percentages_below_alpha = calculate_percentage_below_alpha(algo_ratios, alpha)
    print_formatted_percentages(percentages_below_alpha)

if __name__ == "__main__":
    main()
