import os

class DataProcessor:
    ALGORITHM_DIRS = ["./Algo1", "./Algo2", "./Algo3"] 
    best_values = {}
    parsed_data = {}

    @classmethod
    def load_parsed_data(cls):
        """
        Loads and parses data for each algorithm and computes the minimal value per file immediately.
        """
        cls.parsed_data = {algo_dir: cls.read_and_parse_files(algo_dir) for algo_dir in cls.ALGORITHM_DIRS}
        cls.compute_best_values()

    @classmethod
    def compute_best_values(cls):
        """
        Computes the minimal value per file across all algorithms.
        """
        cls.best_values = {}
        for algo_values in cls.parsed_data.values():
            for file_key, values in algo_values.items():
                min_value = cls.get_min_value(values)
                if file_key not in cls.best_values or min_value < cls.best_values[file_key]:
                    cls.best_values[file_key] = min_value
    
    @staticmethod
    def get_min_value(values):
        """
        Returns the minimum value from a list of (eval_num, obj_value) tuples.
        """
        return min((obj_value for _, obj_value in values), default=float('inf'))

    @staticmethod
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

    @classmethod
    def read_and_parse_files(cls, directory):
        """
        Reads and parses function evaluation files from a given directory.
        Returns a dictionary with filenames as keys and lists of tuples (eval_num, obj_value) as values.
        """
        files = cls.get_files_from_directory(directory)
        if not files:
            return {}
        
        return {os.path.basename(file): cls.parse_file(file) for file in files}
    
    @staticmethod
    def parse_file(file_path):
        """
        Parses a single file and returns a list of tuples (eval_num, obj_value).
        """
        values = []
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    eval_num, obj_value = int(parts[0]), float(parts[1])
                    values.append((eval_num, obj_value))
        return values

    @classmethod
    def get_accuracy_value(cls, file_key, current_eval):
        """
        Computes the accuracy value based on the evaluation number.
        """
        combined_values = cls.get_combined_values(file_key)
        
        if not combined_values:
            raise ValueError(f"No data found for file_key: {file_key}")
        
        first_value = combined_values[0][1]
        best_value = cls.best_values.get(file_key, first_value)
        
        current_value = next((obj_value for eval_num, obj_value in combined_values if eval_num == current_eval), None)
        
        if current_value is None:
            raise ValueError(f"No data found for eval_num: {current_eval} in file_key: {file_key}")
        
        if best_value == first_value:
            return None 
        
        return (current_value - first_value) / (best_value - first_value)

    @classmethod
    def get_combined_values(cls, file_key):
        """
        Combines values from all algorithms for a given file_key and sorts them by evaluation number.
        """
        all_data = [cls.parsed_data[algo].get(file_key, []) for algo in cls.ALGORITHM_DIRS]
        return sorted([item for sublist in all_data for item in sublist], key=lambda x: x[0])

    @classmethod
    def isTauSolved(cls, accuracy, tau):
        return accuracy is not None and accuracy >= 1 - tau

    @classmethod
    def findSmallestEvalTauSolved(cls, algo_dir, file_key, tau):
        """
        Finds the smallest evaluation number where tau is solved for a specific algorithm.
        """
        if algo_dir not in cls.parsed_data or file_key not in cls.parsed_data[algo_dir]:
            return float('inf') 
    
        for eval_num, _ in cls.parsed_data[algo_dir][file_key]:
            accuracy = cls.get_accuracy_value(file_key, eval_num)  
            if cls.isTauSolved(accuracy, tau):
                return eval_num

        return float('inf')
    
    @classmethod
    def print_formatted_percentages(cls, percentages_below_alpha):
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
