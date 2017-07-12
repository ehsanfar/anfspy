import random
import numpy as np
from .task import Task
import queue
from .federateLite import FederateLite
import re

from .graph import Graph

class ContextLite():
    def __init__(self):
        """
        @param locations: the locations in this context
        @type locations: L{list}
        @param events: the events in this context
        @type events: L{list}
        @param federations: the federations in this context
        @type federations: L{list}
        @param seed: the seed for stochastic events
        @type seed: L{int}
        """
        self.initTime = 0
        self.maxTime = 0
        self.time = 0
        self.federates = []
        self.elements = []
        self.masterfederate = []
        self.seed = 0
        self.currentTasks = {i: queue.Queue(maxsize = 3) for i in range(1,7)}
        self.graph = []
        self.nodeLocations = []
        self.shortestPathes = []
        self.Graph = None
        self.taskid = 0
        self.pickupProbability = 0.1



    def init(self, ofs):
        self.time = ofs.initTime
        self.initTime = ofs.initTime
        self.maxTime = ofs.maxTime

        self.masterStream = random.Random(self.seed)
        self.shuffleStream = random.Random(self.masterStream.random())
        self.orderStream = random.Random(self.masterStream.random())


        self.generateFederates(ofs.elements)
        self.generateTasks()
        self.elements = self.getElements()

        self.Graph = Graph()
        self.Graph.createGraph(self)


    def getElementOwner(self, element):
        return next((federate for federate in self.federates
                     if element in federate.elements), None)

    def getTaskOwner(self, task):
        return task.federateOwner

    def findTask(self, task):

        return next((element for federate in self.federates
                     for element in federate.elements
                     if task in element.savedTasks), None)

    def executeOperations(self, scheme = 'federated'):
        """
        Executes operational models.
        """
        if scheme == 'federated':
            federates = self.federates
            random.shuffle(federates, random=self.orderStream.random)
            for federate in federates:
                # print "Pre federate operation cash:", federate.cash
                federate.ticktock(self.time)
                # print "Post federate operation cash:", federate.cash
        elif scheme == 'centralized':
            self.masterfederate.ticktock()


    def ticktock(self, ofs):
        """
        Tocks this context in a simulation.
        """
        self.time = ofs.time
        self.executeOperations()
        self.Graph.createGraph(self)
        # self.Graph.drawGraphs()
        # print "picked up tasks"
        if self.time>=6:
            self.pickupTasks()
            self.Graph.drawGraph(self)
            # print [e.queuedTasks.qsize() for e in self.elements if e.isSpace()]
            # print [len(e.savedTasks) for e in self.elements if e.isSpace()]
            # print "Graphorder:", [e.Graph.graphOrder for e in self.elements if e.isSpace()], self.Graph.graphOrder
            self.deliverTasks()




        # print "Context - Assigned Tasks:", self.taskid
        # print self.time, [a.getLocation() for a in self.elements]

    def generateTasks(self, N=6):
        # tasklocations = np.random.choice(range(1,7), N)
        for l in self.currentTasks:
            if self.currentTasks[l].full():
                self.currentTasks[l].get()

            while not self.currentTasks[l].full():
                self.currentTasks[l].put(Task(self.time))

        # print "current tasks size:", [c.qsize() for c in self.currentTasks.values()]

    def generateFederates(self, elements):
        # elist = elements.split(' ')
        elementgroups = []
        for e in elements:
            elementgroups.append(re.search(r'\b(\d+)\.(\w+)@(\w+\d).+\b', e).groups())
        fedset = sorted(list(set([e[0] for e in elementgroups])))
        # print elementgroups
        # print fedset
        self.federates = [FederateLite(name = 'F'+i, context = self) for i in fedset]
        for element in elementgroups:
            index = fedset.index(element[0])
            self.federates[index].addElement(element[1], element[2])

    def getElements(self):
        elements = []
        for f in self.federates:
            elements += f.getElements()[:]
        return elements

    def pickupTasks(self):
        self.generateTasks()
        # print "pickupTasks elements:", self.elements
        # print "current tasks size:", [c.qsize() for c in self.currentTasks.values()]
        for element in self.elements:
            if element.isSpace():
                # print element.name, self.taskid
                if element.pickupTask(self.currentTasks, self.taskid):
                    # print "pick up task in context:", element
                    self.taskid += 1
                    # print "pickupTasks taskid:", self.taskid
                # else:
                    # print "No pickup"

    def deliverTasks(self):
        # print "delivering tasks"
        # # G = self.Graph.getGraph()
        # graphorder = self.Graph.graphOrder
        for federate in self.federates:
            federate.deliverTasks(self)













