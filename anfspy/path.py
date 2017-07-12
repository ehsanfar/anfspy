from .bundle import EdgeBundle

class Path():
    def __init__(self, task, elementlist):
        self.nodelist = [e.name for e in elementlist]
        self.elements = elementlist
        self.federates = []
        self.federateCost = {}
        self.federatePrice = {}
        self.federateBundleDict = {}
        self.edgebundles = []
        self.task = task
        self.pathBid = None
        self.pathPrice = None

    def updateValues(self):
        bid_list = [b.bid for b in self.edgebundles]
        price_list = [b.price for b in self.edgebundles]
        # print("Path: nodelist and costlist:", self.nodelist, bid_list)
        if all(isinstance(c, float) or isinstance(c, int) for c in bid_list):
            self.pathBid = sum(bid_list)
            self.pathPrice = sum(price_list)
        else:
            self.pathBid = None
            self.pathPrice = None
        # print("update pathBid:", self.nodelist, self.pathBid)

    def updatePrice(self, price):
        self.pathPrice = price

    def updateBundles(self, federatebundledict):
        self.federateBundleDict = federatebundledict
        self.edgebundles = list(federatebundledict.values())

    def getPathBid(self):
        if self.pathBid is None:
            self.updateValues()
        return self.pathBid

    def getPathPrice(self):
        if self.pathPrice is None:
            self.updateValues()
        return self.pathPrice

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


