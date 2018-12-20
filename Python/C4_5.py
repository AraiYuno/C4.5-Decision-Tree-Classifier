import math
from Node import Node

#Author: Kyle Ahn
class C4_5:
    def __init__(self, pathToData, pathToNames):
        self.filePathToData = pathToData
        self.filePathToNames = pathToNames
        self.data = []
        self.classes = []
        self.numAttributes = -1
        self.attrValues = {}
        self.attributes = []
        self.countShit = 0
        self.tree = None


    # Author: Kyle Ahn
    #   Takes in a record of attributes and uses the decision tree to classify the record.
    #   Returns the class string (Low Income, Middle Income, High Income)
    def classify(self, record):
        return self.recursive_classify(record, self.tree)


    #Kevin's job
    def recursive_classify(self, record, node):
        if node.isLeaf:
            return node.label
        else:
            if node.label == "Race":
                race = record[0]
                for i in range(len(node.children)):
                    if race == node.children[i].category:
                        return self.recursive_classify(record, node.children[i])
            elif node.label == "Working Hours":
                hours_worked = float(record[1])
                if hours_worked <= node.threshold:
                    return self.recursive_classify(record, node.children[0])
                else:
                    return self.recursive_classify(record, node.children[1])
            elif node.label == "Education":
                if record[2] == "31" or record[2] == "32" \
                        or record[2] == "33" or record[2] == "34" or record[2] == "35" \
                        or record[2] == "36" or record[2] == "37" or record[2] == "38":
                    education = "No High School Diploma"
                elif record[2] == "39":
                    education = "High School Graduate"
                elif record[2] == "40" or record[2] == "41" or record[2] == "42":
                    education = "College"
                elif record[2] == "43":
                    education = "Bachelor's Degree"
                elif record[2] == "44":
                    education = "Master's Degree"
                elif record[2] == "45":
                    education = "MD/DDS/JD"
                elif record[2] == "46":
                    education = "Doctorate Degree"
                for i in range(len(node.children)):
                    if education == node.children[i].category:
                        return self.recursive_classify(record, node.children[i])
            elif node.label == "Marital Status":
                marital_status = record[3]
                for i in range(len(node.children)):
                    if marital_status == node.children[i].category:
                        return self.recursive_classify(record, node.children[i])
            elif node.label == "IsBusinessOwner":
                if record[4] == "B1":
                    return self.recursive_classify(record, node.children[0])
                else:
                    return self.recursive_classify(record, node.children[1])
            elif node.label == "livesInCity":
                lives_in_city = record[5]
                for i in range(len(node.children)):
                    if lives_in_city == node.children[i].category:
                        return self.recursive_classify(record, node.children[i])
            elif node.label == "Medical Condition":
                if record[6] == "M0":
                    return self.recursive_classify(record, node.children[0])
                else:
                    return self.recursive_classify(record, node.children[1])
            elif node.label == "Age":
                age = float(record[7])
                if age <= node.threshold:
                    return self.recursive_classify(record, node.children[0])
                else:
                    return self.recursive_classify(record, node.children[1])
            elif node.label == "Job Begin  Year":
                job_begin_year = float(record[8])
                if job_begin_year <= node.threshold:
                    return self.recursive_classify(record, node.children[0])
                else:
                    return self.recursive_classify(record, node.children[1])
            elif node.label == "Sex":
                if record[9] == "S1":
                    return self.recursive_classify(record, node.children[0])
                else:
                    return self.recursive_classify(record, node.children[1])


    def fetchData(self):
        with open(self.filePathToNames, "r") as file:
            classes = file.readline()
            self.classes = [x.strip() for x in classes.split(",")]
            #add attributes
            for line in file:
                [attribute, values] = [x.strip() for x in line.split(":")]
                values = [x.strip() for x in values.split(",")]
                self.attrValues[attribute] = values
        self.numAttributes = len(self.attrValues.keys())
        self.attributes = list(self.attrValues.keys())
        with open(self.filePathToData, "r") as file:
            for line in file:
                row = [x.strip() for x in line.split(",")]
                if row != [] or row != [""]:
                    self.data.append(row)


    def preprocessData(self):
        for index,row in enumerate(self.data):
            for attr_index in range(self.numAttributes):
                if(not self.isAttrDiscrete(self.attributes[attr_index])):
                    self.data[index][attr_index] = float(self.data[index][attr_index])


    def generateTree(self):
        self.tree = self.recursiveGenerateTree(self.data, self.attributes)

    def recursiveGenerateTree(self, curData, curAttributes):
        allSame = self.allSameClass(curData)
        if len(curData) == 0:
            #Fail
            return Node(True, "Fail", None)
        elif allSame is not False:
            #return a node with that class
            return Node(True, allSame, None)
        elif len(curAttributes) == 0:
            #return a node with the majority class
            majClass = self.getMajClass(curData)
            return Node(True, majClass, None)
        else:
            (best,best_threshold,splitted) = self.splitAttribute(curData, curAttributes)
            remainingAttributes = curAttributes[:]
            if best is not -1:
                remainingAttributes.remove(best)
            node = Node(False, best, best_threshold)

            for index in range(len(splitted)):
                subset = splitted[index]
                if len(subset) != 0:
                    child = self.recursiveGenerateTree(subset, remainingAttributes)
                    self.set_category(child, best, subset, False, index)
                    node.children.append(child)
                else:
                    child = Node(True, self.getMajClass(curData), None)
                    self.set_category(child, best, subset, True, index)
                    node.children.append(child)

        return node

    def getMajClass(self, curData):
        freq = [0]*len(self.classes)
        for row in curData:
            index = self.classes.index(row[-1])
            freq[index] += 1
        maxInd = freq.index(max(freq))
        return self.classes[maxInd]


    def allSameClass(self, data):
        for row in data:
            if row[-1] != data[0][-1]:
                return False
        return data[0][-1]


    def isAttrDiscrete(self, attribute):
        if attribute not in self.attributes:
            raise ValueError("Attribute not listed")
        elif len(self.attrValues[attribute]) == 1 and self.attrValues[attribute][0] == "continuous":
            return False
        else:
            return True


    def set_category(self, child, best, subset, is_empty, index):
        if not is_empty:
            if best == 'Race':
                child.category = subset[0][0]
            elif best == 'Education':
                child.category = subset[0][2]
            elif best == 'Marital Status':
                child.category = subset[0][3]
            elif best == 'IsBusinessOwner':
                child.category = subset[0][4]
            elif best == 'livesInCity':
                child.category = subset[0][5]
            elif best == 'Medical Condition':
                child.category = subset[0][6]
            elif best == 'Sex':
                child.category = subset[0][9]
        else:
            if best == 'Race':
                child.category = 'R' + str(index)
            elif best == 'Education':
                if index is 0:
                    child.category = 'No High School Diploma'
                elif index is 1:
                    child.category = 'High School Graduate'
                elif index is 2:
                    child.category = 'College'
                elif index is 3:
                    child.category = "Bachelor's Degree'"
                elif index is 4:
                    child.category = "Master's Degree"
                elif index is 5:
                    child.category = "MD/DDS/JD"
                elif index is 6:
                    child.category = "Doctorate Degree"
            elif best == 'Marital Status':
                child.category = str(index + 1)
            elif best == 'IsBusinessOwner':
                child.category = "B" + str(index + 1)
            elif best == 'livesInCity':
                child.category = "L" + str(index)
            elif best == 'Medical Condition':
                child.category = "M" + str(index)
            elif best == 'Sex':
                child.category = "S" + str(index + 1)


    def splitAttribute(self, curData, curAttributes):
        splitted = []
        maxEnt = -1*float("inf")
        best_attribute = -1
        #None for discrete attributes, threshold value for continuous attributes
        best_threshold = None
        for attribute in curAttributes:
            indexOfAttribute = self.attributes.index(attribute)
            if self.isAttrDiscrete(attribute):
                #split curData into n-subsets, where n is the number of
                #different values of attribute i. Choose the attribute with
                #the max gain
                valuesForAttribute = self.attrValues[attribute]
                subsets = [[] for attribute in valuesForAttribute]

                for row in curData:
                    for rowIndex in range(len(row)):
                        for attrValueIndex in range(len(valuesForAttribute)):
                            if row[rowIndex] == valuesForAttribute[attrValueIndex]:
                                subsets[attrValueIndex].append(row)
                                break

                e = self.gain(curData, subsets)
                if e > maxEnt:
                    maxEnt = e
                    splitted = subsets
                    best_attribute = attribute
                    best_threshold = None
            else:
                #sort the data according to the column.Then try all
                #possible adjacent pairs. Choose the one that
                #yields maximum gain
                curData.sort(key = lambda x: x[indexOfAttribute])
                for j in range(0, len(curData) - 1):
                    if curData[j][indexOfAttribute] != curData[j+1][indexOfAttribute]:
                        threshold = (curData[j][indexOfAttribute] + curData[j+1][indexOfAttribute]) / 2
                        less = []
                        greater = []
                        for row in curData:
                            if(row[indexOfAttribute] > threshold):
                                greater.append(row)
                            else:
                                less.append(row)

                        e = self.gain(curData, [less, greater])
                        if e >= maxEnt:
                            splitted = [less, greater]
                            maxEnt = e
                            best_attribute = attribute
                            best_threshold = threshold

        return (best_attribute,best_threshold,splitted)


    def gain(self,unionSet, subsets):
        #input : data and disjoint subsets of it
        #output : information gain
        S = len(unionSet)
        #calculate impurity before split
        impurityBeforeSplit = self.entropy(unionSet)
        impurityBeforeSplit = self.entropy(unionSet)
        #calculate impurity after split
        weights = [len(subset)/S for subset in subsets]
        impurityAfterSplit = 0
        for i in range(len(subsets)):
            impurityAfterSplit += weights[i]*self.entropy(subsets[i])
        #calculate total gain
        totalGain = impurityBeforeSplit - impurityAfterSplit
        return totalGain

    def entropy(self, dataSet):
        S = len(dataSet)
        if S == 0:
            return 0
        num_classes = [0 for i in self.classes]
        for row in dataSet:
            classIndex = list(self.classes).index(row[-1])
            num_classes[classIndex] += 1
        num_classes = [x/S for x in num_classes]
        ent = 0
        for num in num_classes:
            ent += num*self.log(num)
        return ent*-1


    def log(self, x):
        if x == 0:
            return 0
        else:
            return math.log(x,2)



    def printTree(self):
        self.printNode(self.tree)


    def printNode(self, node, indent=""):
        if not node.isLeaf:
            if node.threshold is None:
                #discrete
                for index,child in enumerate(node.children):
                    if child.isLeaf:
                        print(indent + node.label + " = " + child.category + " : " + child.label)
                    else:
                        print(indent + node.label + " = " + child.category + " : ")
                        self.printNode(child, indent + "	")
            else:
                leftChild = node.children[0]
                rightChild = node.children[1]


                if leftChild.isLeaf:
                    print(indent + node.label + " <= " + str(node.threshold) + " : " + leftChild.label)
                else:
                    print(indent + node.label + " <= " + str(node.threshold)+" : ")
                    self.printNode(leftChild, indent + "	")

                if rightChild.isLeaf:
                    print(indent + node.label + " > " + str(node.threshold) + " : " + rightChild.label)
                else:
                    print(indent + node.label + " > " + str(node.threshold) + " : ")
                    self.printNode(rightChild , indent + "	")
