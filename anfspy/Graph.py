import networkx as nx
import re
import matplotlib.pyplot as plt
import networkx.algorithms.isomorphism as iso
import math
import numpy as np
import time
from itertools import cycle
from graphdrawfunctions import *


class Graph():
    def __init__(self):
        self.graphList = []
        self.nodeLocations = []
        self.shortestPathes = []
        self.shortestPathCost = []
        self.elements = []
        self.federates = []
        self.elementOwners = {}
        self.graphOrder = None


    # def findShortestPathes(self, G):
    #     pathdict = {}
    #     costdict = {}
    #
    #     nodes = G.nodes()
    #     # print "nodes:", nodes
    #     satellites = [n for n in nodes if 'GS' not in n]
    #     groundstations = [n for n in nodes if 'GS' in n]
    #     for s in satellites:
    #         temppathlist = []
    #         pathcostlist = []
    #         for g in groundstations:
    #             if nx.has_path(G, source=s,target=g):
    #                 sh = nx.shortest_path(G, s, g)
    #                 temppathlist.append(sh)
    #                 tuplist = convertPath2Edge(sh)
    #                 # print tuplist
    #                 costlist = []
    #                 for (source, target) in tuplist:
    #                     cost = 0 if self.elementOwners[s] == self.elementOwners[target] else G[source][target]['weight']
    #                     costlist.append(cost)
    #
    #                 pathcostlist.append(costlist)
    #
    #
    #         pathdict[s] = temppathlist#min(temppathlist, key = lambda x: len(x)) if temppathlist else None
    #         costdict[s] = pathcostlist
    #         # print "pathtuplist:", tuplist
    #         # print "designCost:", costlist
    #
    #
    #     # print "graphList all paths:"
    #     # print pathdict[satellites[0]]
    #     # print costdict[satellites[0]]
    #     return pathdict, costdict
    #
    # def findcheapestpath(self, s):
    #     # print self.getShortestPathes(), s
    #     pathlist = self.getShortestPathes()[s]
    #     costlist = self.getShortestPathCost()[s]
    #     sortedpath = [x for (y,x) in sorted(zip([sum(c) for c in costlist], pathlist))]
    #     # print "cost vs path:", sorted(zip([sum(c) for c in costlist], pathlist))
    #
    #     # return convertPath2Edge(sortedpath[0])
    #     return sortedpath[0]

    def addNewGraph(self, G):
        nodes2 = G.nodes()
        out_deg2 = G.out_degree(nodes2)
        equallist = []
        for i, g in enumerate(self.graphList):
            nodes1 = g.nodes()
            out_deg1 = g.out_degree(nodes1)
            # print [(out_deg1[k], out_deg2[k]) for k in out_deg2]
            if out_deg1 == out_deg2:
                # print [(set(g.neighbors(n)), set(G.neighbors(n))) for n in nodes1]
                # print any(map(lambda x: x[0] != x[1], [(set(g.neighbors(n)), set(G.neighbors(n))) for n in nodes1]))
                # print map(lambda x: x[0] != x[1], [(set(g.neighbors(n)), set(G.neighbors(n))) for n in nodes1])
                if any(map(lambda x: x[0] != x[1], [(set(g.neighbors(n)), set(G.neighbors(n))) for n in nodes1])):
                    continue
                else:
                    if len(self.graphList) == 6:
                        return i

        # print "Not equal to eigther"
        self.graphList.append(G)
        # self.nodeLocations.append([e.getLocation() for e in self.elements])
        # pathdict, costdict = self.findShortestPathes(G)
        # self.shortestPathes.append(pathdict)
        # self.shortestPathCost.append(costdict)
        return len(self.graphList) - 1

        # print len(self.graphList), G.number_of_nodes(), G.number_of_edges()



    def canTransmit(self, txElement, rxElement):

        txsection = int(re.search(r'.+(\d)', txElement.getLocation()).group(1))
        rxsection = int(re.search(r'.+(\d)', rxElement.getLocation()).group(1))
        canT = False

        if txElement.isSpace() and rxElement.isSpace():
            if abs(txsection - rxsection) <= 1 or abs(txsection - rxsection) == 5:
                canT = True

        elif txElement.isSpace() and rxElement.isGround():
            if txsection == rxsection:
                canT = True

        return canT



    def createGraph(self, context):
        self.federates = context.federates[:]
        self.elements = elements = context.elements[:]
        self.elementOwners = {element: federate for (element, federate) in
                         zip([e.name for e in self.elements], [e.getOwner().name for e in self.elements])}

        elementlocations = [e.getLocation() for e in elements]
        # print elementlocations

        G = nx.DiGraph()
        # elementsnames = ['%s.%d'%(e.name, len(self.graphList)) for e in elements]
        elementsnames = [e.name for e in elements]

        G.add_nodes_from(elementsnames)
        # print [e.name for e in elements]

        for tx in elements:
            for rx in elements:
                if tx == rx:
                    continue

                if self.canTransmit(tx, rx):
                    txowner = context.getElementOwner(tx)
                    rxowner = context.getElementOwner(rx)
                    cost = 0.
                    if txowner != rxowner:
                        if rx.isSpace():
                            cost = rxowner.getCost('oISL')
                        elif rx.isGround():
                            cost = rxowner.getCost('oSGL')

                    G.add_edge(tx.name, rx.name, weight=cost)

        self.graphOrder = self.addNewGraph(G)
        # print "graphList order:", self.graphOrder
        # self.drawGraph()

    def getGraph(self):
        return self.graphList[self.graphOrder]

    def getGraphList(self):
        return self.graphList

    def getGraphOrder(self):
        return self.graphOrder

    def getElementOwners(self):
        return self.elementOwners

    def getShortestPathes(self):
        return self.shortestPathes[self.graphOrder]

    def getShortestPathCost(self):
        return self.shortestPathCost[self.graphOrder]

    def drawGraph(self, context):
        drawGraph(self, context)

    def drawGraphs(self):
        drawGraphs(self)


class SuperGraph(Graph):
    def __init__(self, element):
        Graph.__init__(self)
        self.storagePenalty = 6*[0]
        self.rawSuperGraph = None
        self.SuperGaph = None
        self.elementOwner = element
        self.superShorestPaths = None
        self.superPathsCost = None
        self.graphList = []


    def createGraph(self):
        G = nx.DiGraph()
        for i, g in enumerate(self.graphList):
            mapping = {n: '%s.%d'%(n, i) for n in g.nodes()}
            H = nx.relabel_nodes(g, mapping)
            # print "create Graph:", i
            # for n in H.nodes():
            #     print n, H.neighbors(n),
            # print ''

            G = nx.compose(G, H)

        self.rawSuperGraph = G
        self.addStorgeEdges(self.rawSuperGraph)

        self.updatePaths()

    def addStorgeEdges(self, G):
        # print "Add storage penalty:", [int(e) for e in self.storagePenalty]
        for i, s in enumerate(self.storagePenalty):
            name1 = '%s.%d'%(self.elementOwner.name, i%6)
            name2 = '%s.%d'%(self.elementOwner.name, (i+1)%6)
            # print name1, name2, s
            G.add_edge(name1, name2, weight= s)

        self.SuperGaph = G
        # print "create Graph:", self.elementOwner.name
        # for n in self.SuperGaph.nodes():
        #     if self.elementOwner.name in n:
        #         print n, self.SuperGaph.neighbors(n),
        # print ''

    def updateSuperGraph(self, task):
        storagepenalty = self.elementOwner.federateOwner.getStorageCostList(task, self.elementOwner.section)
        # print "Element Storage penalty:", self.elementOwner.name, task.federateOwner.name, storagepenalty, self.graphOrder
        assert len(storagepenalty) == len(self.storagePenalty)

        for i in range(self.graphOrder):
            storagepenalty.append(storagepenalty.pop(0))

        self.storagePenalty = storagepenalty[:]
        self.addStorgeEdges(self.rawSuperGraph)
        self.updatePaths()

    def updatePaths(self):
        pathlist, costlist = self.findShortestPathes(self.SuperGaph)
        self.superShorestPaths = pathlist
        self.superPathsCost = costlist
        # print "Updatepaths:", pathlist, costlist

    def findShortestPathes(self, G):
        nodes = G.nodes()
        # print "nodes:", nodes
        sourcename = '%s.%d'%(self.elementOwner.name, self.graphOrder)

        groundstations = [n for n in nodes if 'GS' in n]
        # print "ground stations:", groundstations
        temppathlist = []
        pathcostlist = []
        for i in range(len(self.storagePenalty)):
            for g in groundstations:
                # print sourcename, g
                if nx.has_path(G, source=sourcename,target=g):
                    sh = nx.shortest_path(G, sourcename, g)
                    temppathlist.append(sh)
                    tuplist = convertPath2Edge(sh)
                    # print tuplist
                    costlist = []
                    for (source, target) in tuplist:
                        cost = (0 if (self.elementOwners[sourcename[:-2]] == self.elementOwners[target[:-2]] and sourcename[:-2] != target[:-2])
                                else G[source][target]['weight'])
                        costlist.append(cost)

                    pathcostlist.append(costlist)

        # print pathcostlist
        # print "find shortest paths:", temppathlist, pathcostlist
        return temppathlist, pathcostlist

    def findcheapestpath(self, task):
        time = self.elementOwner.federateOwner.time
        activationtime = task.activationTime
        assert activationtime >= time
        deltatime = activationtime - time
        future = (self.graphOrder + deltatime)%6
        futurename = '%s.%d'%(self.elementOwner.name, future)

        pathlist = self.superShorestPaths
        costlist = self.superPathsCost
        pathcost = [tup for tup in zip(costlist, pathlist) if futurename in tup[1]]

        sortedpath = sorted([(sum(x), y) for x,y in pathcost])
        # print "cost vs path:", sorted(zip([sum(c) for c in costlist], pathlist))

        # return convertPath2Edge(sortedpath[0])
        return sortedpath[0]

        # def setGraphList(self, context):
        #     self.graphList = context.Graph.graphList
        #     self.graphOrder = context.Graph.graphOrder









