import csv
from collections import defaultdict
from C4_5 import C4_5

def read_in_file( path ):
    columns = defaultdict(list)  # each value in each column is appended to a list
    with open(path) as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                columns[k].append(v) # append the value into the appropriate list
                                     # based on column name k
    return columns

def main():
    c1 = C4_5("./data/attributes.data", "./data/attributes.names")
    c1.fetchData()
    c1.preprocessData()
    c1.generateTree()
    c1.printTree()


main()
