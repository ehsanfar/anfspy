from .graphdrawfunctions import checkEqual2

class EdgeBundle():
    def __init__(self, edgeilst, path):
        self.edgelist = tuple(sorted(edgeilst))
        self.parentPath = path
        self.parentTask = path.task
        self.parentFederate = self.parentTask.federateOwner
        self.opportunityCost = 0
        self.edgebundlecost = None

    def updateCost(self, cost):
        self.edgebundlecost = cost

    def getBundleCost(self):
        return self.edgebundlecost

    def updateOpportunityCost(self, cost):
        self.opportunityCost = cost

    def __eq__(self, other):
        return (self.edgelist == other.edgelist) and (self.parentTask.taskid is other.parentTask.taskid)

    def __hash__(self):
        temp = list(self.edgelist)+ [self.parentTask.taskid, self.parentFederate.name]
        # print("hash:", temp)
        return hash(tuple(temp))


class PathBundle():
    def __init__(self, pathlist):
        self.pathlist = tuple(sorted(pathlist))
        self.length = len(pathlist)
        self.bundlecost = None
        self.bundlerevenue = None
        self.time = None

        self.updateTime()
        self.updateCost()
        self.updateRevenue()

    def updateTime(self):
        tlist = [path.task.activationTime for path in self.pathlist]
        assert checkEqual2(tlist)
        self.time = tlist[0]

    def updateCost(self):
        # print([p.nodelist for p in self.pathlist])
        # print([path.pathcost for path in self.pathlist])
        self.bundlecost = sum([path.pathcost for path in self.pathlist])

    def updateRevenue(self):
        self.bundlerevenue = sum([path.task.getValue(self.time) for path in self.pathlist])

    def getBundleProfit(self):
        return self.bundlerevenue - self.bundlecost

    def __eq__(self, other):
        return self.pathlist == other.pathlist

    def __lt__(self, other):
         if len(self.pathlist) != len(other.pathlist):
             return len(self.pathlist) < len(other.pathlist)
         else:
             return self.pathlist < other.pathlist

    def __hash__(self):
        return hash(tuple(len(self.pathlist), self.pathlist))





