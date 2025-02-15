import os

def get_files_from_directory(directory):
    """
    Retrieves a sorted list of file paths from the given directory.
    """
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return []
    
    files = [file for file in os.listdir(directory) if file.startswith("stats") and file.endswith(".txt")]
    files.sort(key=lambda x: int(x.replace("stats", "").replace(".txt", "")))
    return [os.path.join(directory, file) for file in files]

def read_and_parse_files(directory):
    """
    Reads and parses function evaluation files from a given directory.
    Returns a dictionary with filenames as keys and lists of tuples (eval_num, obj_value) as values.
    """
    files = get_files_from_directory(directory)
    if not files:
        return {}
    
    all_values = {}
    
    for file in files:
        file_key = os.path.basename(file)
        all_values[file_key] = []
        
        with open(file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    eval_num, obj_value = int(parts[0]), float(parts[1])
                    all_values[file_key].append((eval_num, obj_value))
    
    return all_values

def get_accuracy_value(file_key, all_values, current_eval):
    """
    Computes the accuracy value based on the evaluation number.
    """
    if file_key not in all_values:
        return None
    
    first_value = all_values[file_key][0][1]
    best_value = all_values[file_key][-1][1]
    
    current_value = next((obj_value for eval_num, obj_value in all_values[file_key] if eval_num == current_eval), None)
    if current_value is None or best_value == first_value:
        return None 
    
    accuracy_value = (current_value - first_value) / (best_value - first_value)
    return accuracy_value

def isTauSolved(accuracy, tau):
    return accuracy is not None and accuracy >= 1 - tau

def findSmallestEvalTauSolved(file_key, all_values, tau):
    """
    Finds the smallest evaluation number where tau is solved.
    If tau is not solved, returns infinity.
    """
    if file_key not in all_values:
        return float('inf') 

    for eval_num, _ in all_values[file_key]:
        accuracy = get_accuracy_value(file_key, all_values, eval_num)
        if isTauSolved(accuracy, tau):
            return eval_num

    return float('inf')  

def print_formatted_percentages(percentages_below_alpha):
    """
    Prints the percentages_below_alpha dictionary in the format:
    AlgoX: (1, value1) (2, value2) ...
    """
    algo_names = list(percentages_below_alpha[1].keys())

    for algo in algo_names:
        algo_label = algo.replace("./", "")  
        print(f"{algo_label}: ", end="")
        print(" ".join(f"({key}, {values[algo]:.2f})" for key, values in percentages_below_alpha.items()))
        print()  




