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
    data = read_in_file("./data/data.csv")
    c45 = C4_5(data)

    # filter + preprocess data
    c45.filterData()

    # c45.generateTree()
    c45.generateC4_5Tree()

    # print Tree
    # c45.printTree()


main()
