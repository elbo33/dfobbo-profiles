import sys
import math
from utils import *

def calculate_decimal_accuracy(file_key, last_eval):
    """
    Calculates the decimal accuracy for a given file key.
    """
    accuracy = DataProcessor.get_accuracy_value(file_key, last_eval)
    if accuracy is None or accuracy >= 1:
        return float('inf')  
    return -math.log10(1 - accuracy)

def calculate_d_ratio(file_key, last_eval, d):
    """
    Checks if the decimal accuracy is within the threshold d.
    """
    return calculate_decimal_accuracy(file_key, last_eval) >= d

def compute_d_ratios(max_d):
    """
    Computes the d ratios for all values of d in range 0 to max_d.
    """
    DataProcessor.load_parsed_data()
    all_d_ratios = {}
    
    for d in range(max_d + 1):
        all_d_ratios[d] = calculate_d_ratios(d)
    
    DataProcessor.print_formatted_percentages(all_d_ratios)

def calculate_d_ratios(d):
    """
    Computes the ratio of instances where the decimal accuracy is within d for each algorithm.
    """
    count_valid = {algo_dir: 0 for algo_dir in DataProcessor.ALGORITHM_DIRS}
    total_problems = 159
    
    for file_num in range(1, 160):
        file_name = f"stats{file_num}.txt"
        
        for algo_dir, parsed_values in DataProcessor.parsed_data.items():
            if file_name in parsed_values:
                last_eval = parsed_values[file_name][-1][0] 
                if calculate_d_ratio(file_name, last_eval, d):
                    count_valid[algo_dir] += 1
    
    return {algo_dir: (count_valid[algo_dir] / total_problems) * 100 for algo_dir in DataProcessor.ALGORITHM_DIRS}

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <d>")
        sys.exit(1)
        
    d = int(sys.argv[1])
    compute_d_ratios(d)

if __name__ == "__main__":
    main()

