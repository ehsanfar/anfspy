class Path():
    def __init__(self, task, nodelist):
        self.nodelist = nodelist
        self.federates = []
        self.federateCost = {}
        self.federatePrice = {}
        self.federateEdge = {}
        self.task = task

    def updateCost(self, fed, cost):
        self.federateCost[fed] = cost

    def updatePrice(self, fed, price):
        self.federatePrice[fed] = price

    def updateEdge(self, federateEdge):
        self.federateEdge = federateEdge

    def getNodeList(self):
        return self.nodelist

    def getFederateEdge(self):
        return self.federateEdge


