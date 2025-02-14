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

def get_best_known_value(file):
    """
    Retrieves the last objective value from a file.
    """
    with open(file, 'r') as f:
        lines = f.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip().split()
        if len(last_line) == 2:
            return float(last_line[1])
    return None

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
    """
    if file_key not in all_values:
        return None
    
    for eval_num, _ in all_values[file_key]:
        accuracy = get_accuracy_value(file_key, all_values, eval_num)
        if isTauSolved(accuracy, tau):
            return eval_num
    
    return None


