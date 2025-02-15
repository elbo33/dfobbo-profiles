from utils import *

def count_valid_instances(parsed_data, k):
    """
    Counts instances where the lowest evaluation number is <= k for each algorithm.
    """
    count_valid = {algo_dir: 0 for algo_dir in ALGORITHM_DIRS}
    total_problems = 159
    
    for file_num in range(1, 160): 
        file_name = f"stats{file_num}.txt"
        
        for algo_dir, parsed_values in parsed_data.items():
            if file_name in parsed_values:
                eval_num = findSmallestEvalTauSolved(file_name, parsed_values, 0.1)  # Assuming tau=0.1
                if eval_num is not None and eval_num <= k * (k + 1) / 2:
                    count_valid[algo_dir] += 1
    
    return count_valid, total_problems

def calculate_k_ratio_per_algorithm(parsed_data, k):
    """
    Calculates the ratio of valid instances for each algorithm.
    """
    count_valid, total_problems = count_valid_instances(parsed_data, k)
    return {algo_dir: round(count_valid[algo_dir] / total_problems, 3) for algo_dir in ALGORITHM_DIRS}

def main():
    parsed_data = load_parsed_data()
    for i in range(1,100):
        ratios = calculate_k_ratio_per_algorithm(parsed_data, i)
        
        print(f"Ratio of instances where best evaluation <= {i} per algorithm:")
        for algo, ratio in ratios.items():
            print(f"{algo}: {ratio}")

if __name__ == "__main__":
    main()
