
class C4_5:
    def __init__(self, data):
        self.data = []
        self.classes = ["High Income", "Middle Income", "Low Income"]
        self.tree = None
        self.attributes = [];

    # Assigned to Kaleigh to filter the data.
    # 1. you may access job type by self.data["Occupation"], and please return filtered list of data
    # classified into one of the classes defined above.
    # 2. filterData should remove all the unnecessary data such as people under the age of "15".
    def filterData(self):
        print("Kaleigh's job")


    def buildC4_5Tree(self):
        self.tree = self.recursiveBuildC4_5Tree(self.data, self.attributes)


    def recursiveBuildC4_5Tree(self, data):
        someoneWillWorry = 1


    def calcEntropy(self, dataSet):
        S = len(dataSet)
        if S == 0:
            return 0
        num_classes = [0 for i in self.classes]
        for row in dataSet:
            classIndex = list(self.classes).index(row[-1])
            num_classes[classIndex] += 1
        num_classes = [x / S for x in num_classes]
        ent = 0
        for num in num_classes:
            ent += num * self.log(num)
        return ent * -1

