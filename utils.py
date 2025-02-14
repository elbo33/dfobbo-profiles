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
                    eval_num, obj_value = int(parts[0]), round(float(parts[1]), 3)
                    all_values[file_key].append((eval_num, obj_value))
    
    return all_values

def get_accuracy_value(file_key, all_values, current):
    """
    Computes the accuracy value.
    """

    best_value = all_values[file_key][-1][1]
    first_value = all_values[file_key][0][1]
    current_value = all_values[file_key][current][1]

    if best_value == first_value:
        return None  
    accuracy_value = (current_value - first_value) / (best_value - first_value)
    return accuracy_value

def isTauSolved(accuracy, tau):
    return accuracy >= 1-tau

def main():
    directory = "./Algo1"
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    parsed_values = read_and_parse_files(directory)
    if not parsed_values:
        print("No valid data found in the provided directory.")
    else:
        accuracy = get_accuracy_value('stats1.txt', parsed_values, 0)
        print(accuracy)
        print(isTauSolved(accuracy, 0))
if __name__ == "__main__":
    main()
