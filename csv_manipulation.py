import os
import csv

# Get the absolute path of the project root (where the script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the csv
CSV_PATH = os.path.join(BASE_DIR, 'data', 'time_series_covid19_confirmed_US.csv')

def read_csv(path=CSV_PATH):
    try:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            return list(reader)
    except FileNotFoundError:
        print(f"Error: The file at {path} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_time_series_dict(data, skip_value=1, threshold=3):
    """
    Converts a list of lists representing CSV time series data into a list of daily new cases.
    
    Args:
        data (list of lists): The input data from the CSV file.
        skip_value (int, optional): The number of days to skip between each time step. Defaults to 1.
        threshold (int, optional): Minimum number of new cases to consider a location as having new cases.
                                   Smaller changes are set to 0. Defaults to 3.
    
    Returns:
        list: Triple nested array of time series data, where each entry is [lat, lon, intensity],
              and intensity represents daily new cases.
              Format: res[date][location_idx] = [lat, lon, intensity]
    """
    res = []
    for col in range(11, len(data[0]), skip_value):
        day = []
        for row in range(1, len(data)):
            current_cases = int(data[row][col])
            intensity = max(0, current_cases)
            lat = float(data[row][8])
            lon = float(data[row][9])
            day.append([lat, lon, intensity])
        res.append(day)
    return res