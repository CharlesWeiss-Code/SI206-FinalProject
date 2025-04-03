"""
handles csv data
"""

import csv

def read_csv(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        return list(reader)
    

def main():
    print(read_csv)

if __name__ == "__main__":
    main()