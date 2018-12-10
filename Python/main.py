import csv
import os
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


def map_income_classes():
    data = read_in_file("./data/mapIncomeClassData.csv")
    income_class = read_in_file("./data/occupation_classes.csv")
    mapped_class_list = []
    for occupation_value in data["Occupation"]:
        income_level = find_income_level(occupation_value, income_class)
        mapped_class_list.append(income_level)
    write_to_attributes_data(data, mapped_class_list)
    write_to_attributes_names(data, mapped_class_list)


def find_income_level(occupation_value, income_class):
    income_level = "Low Income"
    occupation_type_found = False
    index = 0
    for curr_value in income_class["value"]:
        if occupation_value == curr_value:
            occupation_type_found = True
            break
        else:
            index = index + 1

    if occupation_type_found:
        income_level = income_class["class"][index]
    return income_level


def write_to_attributes_data(data, mapped_class_list):
    if os.path.exists("./data/attributes_data.txt"):
        os.remove("./data/attributes_data.txt")
    file = open("./data/attributes_data.txt", "w+")
    for i in range(len(data["Race"])):
        if mapped_class_list[i] == "Low Income" or mapped_class_list[i] == "Middle Income" or mapped_class_list[i] == "High Income":
            medical_condition = "0"
            if( data["Medical Condition"][i] is not "0"):
                medical_condition = "1"

            file.write(data["Race"][i] + "," + data["Working Hours"][i] + "," + data["Education"][i] + "," + data["Marital Status"][i]
                       + "," + data["IsBusinessOwner"][i] + ","+ data["livesInCity"][i] + "," + medical_condition
                       + "," + data["Age"][i] + "," + mapped_class_list[i] + "\n")


def write_to_attributes_names(data, mapped_class_list):
    if os.path.exists("./data/attributes_names.txt"):
        os.remove("./data/attributes_names.txt")
    file = open("./data/attributes_names.txt", "w+")
    education = get_discrete_categories(data["Education"])
    marital_status = get_discrete_categories(data["Marital Status"])
    medical_condition = get_discrete_categories(data["Medical Condition"])
    state = get_discrete_categories(data["State"])
    file.write("Low Income, Middle Income, High Income\nRace : 0, 1, 2, 3, 4\nWorking Hours : continuous\nEducation : "
               + education + "\nMarital Status : " + marital_status + "\nIsBusinessOwner : 0,1,2\nlivesInCity : 0,1,2\n"
               + "Medical Condition : 0,1\nAge : continuous")


def get_discrete_categories(column):
    discrete_categories = []
    for i in range(len(column)):
        found = False
        for j in range(len(discrete_categories)):
            if column[i] == discrete_categories[j]:
                found = True
        if not found:
            discrete_categories.append(column[i])

    discrete_categories_str = ""
    for i in range(len(discrete_categories)):
        if i is 0:
            discrete_categories_str += discrete_categories[i]
        else:
            discrete_categories_str += "," + discrete_categories[i]
    return discrete_categories_str


def main():
    c1 = C4_5("./data/attributes_data.txt", "./data/attributes_names.txt")
    c1.fetchData()
    c1.preprocessData()
    c1.generateTree()
    c1.printTree()


map_income_classes()
main()