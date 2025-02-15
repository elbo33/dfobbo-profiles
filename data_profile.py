import sys
from utils import *

def precompute_eval_numbers(parsed_data, tau):
    """
    Precompute the smallest evaluation number for each problem and algorithm.
    """
    eval_numbers = {algo_dir: {} for algo_dir in ALGORITHM_DIRS}
    
    for file_num in range(1, 160): 
        file_name = f"stats{file_num}.txt"
        
        for algo_dir, parsed_values in parsed_data.items():
            if file_name in parsed_values:
                eval_numbers[algo_dir][file_name] = findSmallestEvalTauSolved(file_name, parsed_values, tau)
            else:
                eval_numbers[algo_dir][file_name] = None
    
    return eval_numbers

def count_valid_instances(eval_numbers, k):
    """
    Counts instances where the lowest evaluation number is <= k for each algorithm.
    """
    count_valid = {algo_dir: 0 for algo_dir in ALGORITHM_DIRS}
    total_problems = 159
    
    for file_name in eval_numbers[ALGORITHM_DIRS[0]]:  # Iterate through problem instances
        for algo_dir in ALGORITHM_DIRS:
            eval_num = eval_numbers[algo_dir][file_name]
            if eval_num is not None and eval_num <= k * (k + 1) / 2:
                count_valid[algo_dir] += 1
    
    return count_valid, total_problems

def calculate_k_ratios(eval_numbers, max_k):
    """
    Computes k ratios for a range of k values from 1 to max_k.
    """
    k_ratios = {}
    
    for k in range(0, max_k):
        count_valid, total_problems = count_valid_instances(eval_numbers, k)
        k_ratios[k] = {algo_dir: (count_valid[algo_dir] / total_problems)*100 for algo_dir in ALGORITHM_DIRS}
    
    return k_ratios

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <tau> <k>")
        sys.exit(1)
    tau = float(sys.argv[1])
    k_value = int(sys.argv[2])
    parsed_data = load_parsed_data()
    eval_numbers = precompute_eval_numbers(parsed_data, tau)
    k_ratios = calculate_k_ratios(eval_numbers, k_value)
    print_formatted_percentages(k_ratios)

if __name__ == "__main__":
    main()
