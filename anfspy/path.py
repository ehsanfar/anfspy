from .edgebundle import EdgeBundle

class Path():
    def __init__(self, task, nodelist):
        self.nodelist = nodelist
        self.federates = []
        self.federateCost = {}
        self.federatePrice = {}
        self.federateBundleDict = {}
        self.edgebundles = []
        self.task = task
        self.pathcost = None

    def updateCost(self):
        cost_list = [b.edgebundlecost for b in self.edgebundles]
        # print("Path: nodelist and costlist:", self.nodelist, cost_list)
        if all(isinstance(c, float) or isinstance(c, int) for c in cost_list):
            self.pathcost = sum(cost_list)
        else:
            self.pathcost = None

        # print("update pathcost:", self.nodelist, self.pathcost)
        return self.pathcost

    def updatePrice(self, price):
        self.pathprice = price

    def updateBundles(self, federatebundledict):
        self.federateBundleDict = federatebundledict
        self.edgebundles = federatebundledict.values()

    def getPathCost(self):
        return self.updateCost()

    def getNodeList(self):
        return self.nodelist

    def getFederateBundle(self):
        return self.federateEdge

    def __eq__(self, other):
        return tuple(self.nodelist) == tuple(other.nodelist)

    def __lt__(self, other):
        if len(self.nodelist) != len(other.nodelist):
            return len(self.nodelist) < len(other.nodelist)
        else:
            return self.nodelist < other.nodelist

    def __hash__(self):
        return hash(tuple(len(self.nodelist), self.nodelist))


