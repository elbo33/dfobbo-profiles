import sys
import re
from typing import Dict, Tuple
from utils import DataProcessor

TOTAL_PROBLEMS = 159  
FILENAME_PATTERN = re.compile(r"stats(\d+)\.txt")  

def precompute_eval_numbers(tau):
    """
    Precompute the smallest evaluation number for each problem and algorithm.
    """
    eval_numbers = {algo_dir: {} for algo_dir in DataProcessor.ALGORITHM_DIRS}

    for file_num in range(1, 160): 
        file_name = f"stats{file_num}.txt"

        for algo_dir in DataProcessor.ALGORITHM_DIRS:
            parsed_values = DataProcessor.parsed_data.get(algo_dir, {})  
            
            if file_name in parsed_values:
                eval_numbers[algo_dir][file_name] = DataProcessor.findSmallestEvalTauSolved(algo_dir, file_name, tau)
            else:
                eval_numbers[algo_dir][file_name] = None 

    return eval_numbers


def count_valid_instances(eval_numbers: Dict[str, Dict[str, int]], k: int) -> Tuple[Dict[str, int], int]:
    """
    Counts instances where the lowest evaluation number is <= k * file_number for each algorithm.

    """
    count_valid = {algo_dir: 0 for algo_dir in DataProcessor.ALGORITHM_DIRS}

    for file_name in eval_numbers.get(DataProcessor.ALGORITHM_DIRS[0], {}):
        match = FILENAME_PATTERN.match(file_name) 
        if match:
            file_number = int(match.group(1))  
        else:
            continue 

        for algo_dir in DataProcessor.ALGORITHM_DIRS:
            eval_num = eval_numbers.get(algo_dir, {}).get(file_name)

            if eval_num is not None and eval_num <= k * file_number / 3:
                count_valid[algo_dir] += 1

    return count_valid, TOTAL_PROBLEMS


def calculate_k_ratios(eval_numbers, max_k):
    """
    Computes k ratios for a range of k values from 1 to max_k.
    """
    k_ratios = {}
    
    for k in range(0, max_k):
        count_valid, total_problems = count_valid_instances(eval_numbers, k)
        k_ratios[k] = {algo_dir: (count_valid[algo_dir] / total_problems)*100 for algo_dir in DataProcessor.ALGORITHM_DIRS}
    
    return k_ratios

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <tau> <k>")
        sys.exit(1)
    tau = float(sys.argv[1])
    k_value = int(sys.argv[2])
    DataProcessor.load_parsed_data()
    eval_numbers = precompute_eval_numbers(tau)
    k_ratios = calculate_k_ratios(eval_numbers, k_value)
    DataProcessor.print_formatted_percentages(k_ratios)

if __name__ == "__main__":
    main()
