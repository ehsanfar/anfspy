
import re

from .operationLite import OperationLite
from .elementLite import Satellite, GroundStation


class FederateLite():
    def __init__(self, name, context, initialCash=0, operation =OperationLite(), costSGL = 200., costISL = 100.):
        """
        @param name: the name of this federate
        @type name: L{str}
        @param initialCash: the initial cash for this federate
        @type initialCash: L{float}
        @param elements: the elements controlled by this federate
        @type elements: L{list}
        @param contracts: the contracts owned by this federate
        @type contracts: L{list}
        @param operations: the operations model of this federate
        @type operations: L{Operations}
        """
        self.name = name
        self.initialCash = initialCash
        self.cash = self.initialCash
        self.elements = []
        self.satellites = []
        self.stations = []
        self.operation = operation
        self.costDic = {'oSGL': costSGL, 'oISL': costISL}
        self.tasks = {}
        self.transcounter = 0
        self.transrevenue = 0.
        self.time = context.time

        self.taskduration  = {i: 2. for i in range(1,7)}
        self.taskvalue = {i: 500. for i in range(1,7)}
        self.taskcounter = {i: 10 for i in range(1,7)}

        self.activeTasks = set([])
        self.supperGraph = None
        self.pickupProbability = context.pickupProbability

    def getElements(self):
        """
        Gets the elements controlled by this controller.
        @return L{list}
        """
        return self.elements[:]


    def getTasks(self):
        """
        Gets the contracts controlled by this controller.
        @return L{list}
        """
        return self.tasks


    def ticktock(self, time):
        """
        Ticks this federate in a simulation.
        @param sim: the simulator
        """
        # print "federete tick tock"
        self.time = time
        for element in self.elements:
            element.ticktock()

    def setCost(self, protocol, cost):
        self.costDic[protocol] = cost

    def getCost(self, protocol, federate=None, type=None):
        if self == federate:
            return 0.
        key = '{}-{}'.format(federate, protocol)
        return self.costDic[protocol] if key not in self.costDic else self.costDic[key]

    def addTransRevenue(self, protocol, amount):
        if protocol in self.transCounter:
            self.transrevenue[protocol] += amount
            self.transcounter[protocol] += 1
        else:
            self.transrevenue[protocol] = amount
            self.transcounter[protocol] = 1

    def getTransRevenue(self):
        return self.transrevenue

    def getTransCounter(self):
        return self.transcounter

    def getStorageCostList(self, task, section):
        assert section in range(1, 7)
        storagecostlist = []
        temptime = self.time
        for i in range(1, 7):
            storagecostlist.append(self.pickupProbability*(self.taskvalue[section]/self.taskduration[section] + task.getValue(temptime+1) - task.getValue(temptime)))
            temptime += 1
            section = section%6+1

        # print storagecostlist
        return storagecostlist

    def discardTask(self):
        for e in self.elements:
            for stask in e.savedtasks:
                if stask.getValue(self.time)<=0:
                    self.defaultTask(self, stask)

    def reportPickup(self, task):
        self.activeTasks.add(task)

    def finishTask(self, task):
        taskvalue = task.getValue(self.time) - task.pathcost
        self.cash += taskvalue
        assert task in self.activeTasks
        section = task.getSection()
        assert self.time >= task.initTime
        duration = max(1, self.time - task.initTime)
        assert section in range(1, 7)

        # print "Finished tasks (section, taskvalue, taskduration):", section, taskvalue, duration
        self.taskduration[section] = (self.taskduration[section]*self.taskcounter[section] + duration)/(self.taskcounter[section] + 1.)
        self.taskvalue[section]  = (self.taskvalue[section]*self.taskcounter[section] + taskvalue)/(self.taskcounter[section] + 1.)
        self.taskcounter[section] += 1
        self.activeTasks.remove(task)

    def defaultTask(self, task):
        # print "defaulted task:", task.taskid
        element = task.elementOwner
        element.removeSavedTask(task)
        task.pathcost = 0.
        self.finishTask(task)

    def addElement(self, element, location):
        orbit, section = (re.search(r'(\w)\w+(\d)', location).group(1), int(re.search(r'(\w)\w+(\d)', location).group(2)))
        if 'Ground' in element:
            gs = GroundStation(self, 'GS.%s.%d'%(self.name, len(self.stations)+1), location, 600)
            self.elements.append(gs)
            self.stations.append(gs)

        elif 'Sat' in element:
            ss = Satellite(self, 'S%s.%s.%d'%(orbit, self.name, len(self.satellites)+1), location, 800)
            self.elements.append(ss)
            self.satellites.append(ss)

    def convertPath2StaticPath(self, path):
        temppath = [e[:-2] for e in path]
        ends = [e[-1] for e in path]
        seen = set([])
        seen_add = seen.add
        staticpath = [e for e in temppath if not (e in seen or seen_add(e))]
        # print "convert path 2 static path:", path, staticpath
        deltatime = len(path) - len(seen)
        assert len(set(ends[deltatime:])) == 1
        return (staticpath, deltatime)

    def deliverTasks(self, context):
        for element in self.elements:
            # print "deliver task in Federate:", element
            if element.isSpace():
                element.updateGraph(context)
                # print "graph updated"
                # element.Graph.setGraphList(context)
                if element.queuedTasks.qsize() > 0:
                    task = element.queuedTasks.get()
                    # print element.name, task.taskid, task.initTime
                    element.Graph.updateSuperGraph(task)
                    pathcost, pathname = element.Graph.findcheapestpath(task)
                    # print "element and path:    ", element.name, pathname
                    staticpath, deltatime = self.convertPath2StaticPath(pathname)
                    # print staticpath
                    # print [e.name for e in self.elements]
                    elementpath = [next((e for e in context.elements if e.name == p)) for p in staticpath]
                    task.updatePath(elementpath, pathcost)
                    element.saveTask(task, deltatime)
                    # element.deliverTasks(task)
                savedtasks = element.savedTasks[:]
                for task in savedtasks:
                    # print  "time and task activation time:", self.time, task.activationTime
                    assert task.activationTime >= self.time
                    if self.time == task.activationTime:
                        element.deliverTask(task)
                        # print "len of saved tasks:", len(element.savedTasks),
                        element.removeSavedTask(task)
                        # print len(element.savedTasks)

    def getBundleListCost(self, bundlelist, elementDict, federateDict):
        alltuple = [edge for bundle in bundlelist for edge in bundle]
        print "getBundleCost: ", alltuple
        tuplecostdict = {tupe: self.getCost('oISL', federateDict[tup[1]]) if elementDict[tup[1]].isSpace() else self.getCost('oSGL', federateDict[tup[1]]) for tup in alltuple}

        costlist = []
        for bundle in bundlelist:
            costlist.append(sum([tuplecostdict[b] for b in bundle]))

        return costlist















