import csv
import os
from collections import defaultdict
from C4_5 import C4_5


def read_in_file(path):
    columns = defaultdict(list)  # each value in each column is appended to a list
    with open(path) as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                columns[k].append(v)  # append the value into the appropriate list
                # based on column name k
    return columns


def train_data():
    data = read_in_file("./data/training_data.csv")
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
            education = "No High School Diploma"
            if data["Medical Condition"][i] is not "0":
                medical_condition = "1"
            if data["Education"][i] == data["Education"][i] == "31" or data["Education"][i] == "32" \
                or data["Education"][i] == "33" or data["Education"][i] == "34" or data["Education"][i] == "35" \
                    or data["Education"][i] == "36" or data["Education"][i] == "37" or data["Education"][i] == "38":
                education = "No High School Diploma"
            elif data["Education"][i] == "39":
                education = "High School Graduate"
            elif data["Education"][i] == "40" or data["Education"][i] == "41" or data["Education"][i] == "42":
                education = "College"
            elif data["Education"][i] == "43":
                education = "Bachelor's Degree"
            elif data["Education"][i] == "44":
                education = "Master's Degree"
            elif data["Education"][i] == "45":
                education = "MD/DDS/JD"
            elif data["Education"][i] == "46":
                education = "Doctorate Degree"

            file.write(
                "R" + data["Race"][i] + "," + data["Working Hours"][i] + "," + education + "," + data["Marital Status"][i]
                + "," + "B" + data["IsBusinessOwner"][i] + "," + "L" + data["livesInCity"][i] + "," + "M" + medical_condition
                + "," + data["Age"][i] + "," + data["Job Begin Year"][i] + "," + "S" + data["Sex"][i]
                + "," + mapped_class_list[i] + "\n")


def write_to_attributes_names(data, mapped_class_list):
    if os.path.exists("./data/attributes_names.txt"):
        os.remove("./data/attributes_names.txt")
    file = open("./data/attributes_names.txt", "w+")
    education = "No High School Diploma,High School Graduate,College,Bachelor's Degree,Master's Degree," \
                "MD/DDS/JD,Doctorate Degree"
    marital_status = get_discrete_categories(data["Marital Status"])
    medical_condition = get_discrete_categories(data["Medical Condition"])
    state = get_discrete_categories(data["State"])
    file.write("Low Income, Middle Income, High Income\nRace : R0, R1, R2, R3, R4\nWorking Hours : continuous\nEducation : "
               + education + "\nMarital Status : " + marital_status + "\nIsBusinessOwner : B1,B2\nlivesInCity : L0,L1,L2\n"
               + "Medical Condition : M0,M1\nAge : continuous\nJob Begin  Year : continuous\nSex : S1,S2")


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


def classify_record(c45_tree):
    data = read_in_file("./data/testing_data.csv")
    for i in range(len(data["Race"])):
        record = []
        record.append(data["Race"][i])
        record.append(data["Working Hours"][i])
        record.append(data["Education"][i])
        record.append(data["Marital Status"][i])
        record.append(data["IsBusinessOwner"][i])
        record.append(data["livesInCity"][i])
        record.append(data["Medical Condition"][i])
        record.append(data["Age"][i])
        record.append(data["Job Begin Year"][i])
        record.append(data["Sex"][i])
        income_level = c45_tree.classify(record)
        print(income_level)


def test_data():
    c1 = C4_5("./data/attributes_data.txt", "./data/attributes_names.txt")
    c1.fetchData()
    c1.preprocessData()
    c1.generateTree()
    c1.printTree()
    classify_record(c1)


train_data()
test_data()
