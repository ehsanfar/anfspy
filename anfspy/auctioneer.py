from .graphdrawfunctions import convertPath2Edge
from .path import Path


class Auctioneer():
    def __init__(self, federates, elements, nodes):
        self.federates = federates
        self.elements = elements
        self.nodes = nodes
        self.federateDict = {n: f for (n,f) in zip(self.nodes, self.federates)}
        self.elementsDict = {n: e for (n,e) in zip(self.nodes, self.elements)}
        self.pathdict = {}
        self.pathlist = []
        self.federateEdgeBundles = {}

    def reset(self):
        self.pathdict = {}

    def addPath(self, task, nodelist):
        obj = None
        print "Task nodelist:", task.taskid, nodelist
        if task in self.pathdict:
            obj = Path(task, nodelist)
            self.pathdict[task].append(obj)
        else:
            obj = Path(task, nodelist)
            self.pathdict[task] = [obj]

        self.pathlist.append(obj)

    def findPathFederateEdgeDict(self, path):
        nodelist = path.getNodeList()
        print "auctioneer: nodelist:", nodelist
        edgelist = convertPath2Edge(nodelist)
        federateEdgesDict = {}
        for edge in edgelist:
            print "auctioneer: edge:", edge
            federate = self.federateDict[edge[1]]
            if federate not in federateEdgesDict:
                federateEdgesDict[federate] = []

            federateEdgesDict[federate].append((edge))

        federateEdgesDict = {k: sorted(v) for (k,v) in federateEdgesDict.items()}

        path.updateEdge(federateEdgesDict)
        return federateEdgesDict

    def addDict2Dict(self, dict1, dict2):
        for key in dict2:
            if key in dict1:
                dict1[key] = dict1[key].union(set(dict2[key]))
            else:
                dict1[key] = set(dict2[key]).deepcopy()

        return dict1

    def inquirePrice(self):
        federateEdgeDict = {}
        for path in self.pathlist:
            tempdict = self.findPathFederateEdgeDict(path)
            federateEdgeDict = self.addDict2Dict(federateEdgeDict, tempdict)


        for fed, bundleset in federateEdgeDict.items():
            bundlelist = list(bundleset)
            print "Federate:", fed.name
            print "Inquireprice: bundle list federates:", [[(self.federateDict[x].name, self.federateDict[y].name) for (x,y) in bundle] for bundle in bundlelist]
            costlist = fed.getBundleListcost(bundlelist, self.elementDict)
            bundleCostDict = {x: y for x,y in zip(bundlelist, costlist)}
            for path in self.pathlist:
                pathFederateEdgeDict = path.getFederateEdge()
                if fed in pathFederateEdgeDict:
                    cost = bundleCostDict[tuple(pathFederateEdgeDict[fed])]
                    path.updateCost(fed, cost)













