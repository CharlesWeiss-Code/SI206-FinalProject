import os
import csv
import re

# Get the absolute path of the project root (where the script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the csv
CSV_PATH = os.path.join(BASE_DIR, 'data', 'time_series_covid19_confirmed_US.csv')

def read_csv(path):
    try:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: The file at {path} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_time_series_dict(data, skip_value=1):
    """
    Converts a list of lists representing CSV time series data into a dictionary.
    
    Args:
        data (list of list): The input data from the CSV file, where each inner list
        represents a row with the first element being a key and the remaining elements
        being the associated time series values.
        skip_value (int, optional): The number of elements to skip between each time series value.
        Defaults to 1.
    
    Returns:
        dict: A dictionary where keys are a touple of (Combined_Key, lat, lon) 
        and values is a list of the difference between time series data
    """

    res = {}
    for row in data:
        current_list = []
        # print(row)
        for i in range(12, len(row), skip_value):
            value = int(row[i]) - int(row[i-1])
            value = 0 if value < 0 else value
            current_list.append(value)
        
        res[(row[10], row[8], row[9])] = current_list
        
    return res



# def main():
#     csv_data = read_csv(CSV_PATH)
#     time_series_dict = get_time_series_dict(csv_data, 100)
#     print(time_series_dict)

# if __name__ == "__main__":
#     main()
