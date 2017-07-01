
"""
Elements classes.
"""
import re
import Queue
from .Graph import SuperGraph
from .Graph import SuperGraph
import random

class Element():
    def __init__(self, federate, name, location, cost=0):
        self.name = name
        self.location = re.search('(\w+)(\d)', location).group(1)
        self.section = int(re.search('(\w+)(\d)', location).group(2))
        self.designCost = cost
        self.federateOwner = federate
        self.savedTasks = []
        self.pickupprobablity = self.federateOwner.pickupProbability

    def getOwner(self):
        return self.federateOwner

    def getLocation(self):
        return str(self.location)+str(self.section)

    def getSection(self):
        return self.section

    def getSectionAt(self, time):
        if 'LEO' in self.location:
            return (time*2+self.section-1)%6+1

        elif 'MEO' in self.location:
            return (time+self.section-1)%6+1

        else:
            return self.section

    def ticktock(self):
        if 'LEO' in self.location:
            self.section = (self.section + 2 - 1)%6 + 1
        elif 'MEO' in self.location:
            self.section = (self.section + 1 - 1)%6 + 1


    def getDesignCost(self):
        return self.designCost


    def canSave(self, task):
        if self.isGround():
            return True

        # print "capacity and content:", self.capacity, self.content
        if task.datasize <= (self.capacity - self.content):
            return True

        return False

    def canTransmit(self, rxElement, task):
        return rxElement.couldReceive(self, task)

    def transmitTask(self, task, pathiter):
        # print self.name, task.taskid
        if self.isGround():
            self.saveTask(task)
            return True

        # assert len(pathlist)>=1
        # if len(pathlist)<2:
        #     federate = task.federateOwner
        #     federate.discardTask(self, task)
        task.nextstop = nextstop = next(pathiter)

        received = nextstop.transmitTask(task, pathiter)
        return received

    def isGEO(self):
        if self.isSpace() and 'GEO' in self.location:
            return True

        return False




class GroundStation(Element):
    def __init__(self, federate, name, location, cost):
        Element.__init__(self, federate, name, location, cost)

    def isGround(self):
        return True

    def isSpace(self):
        return False

    def saveTask(self, task, nextstop = None):
        self.savedTasks.append(task)
        task.federateOwner.finishTask(task)
        return True




class Satellite(Element):
    def __init__(self, federate, name, location, cost, capacity=1.):
        Element.__init__(self, federate, name, location, cost)
        self.capacity = capacity
        self.content = 0.
        self.queuedTasks = Queue.Queue()
        self.Graph = SuperGraph(self)

    def getCapacity(self):
        return self.capacity

    def getContentsSize(self):
        return self.content

    def isGround(self):
        return False

    def isSpace(self):
        return True

    def deliverTask(self, task):
        self.transmitTask(task, iter(task.pathlist[1:]))

    def saveTask(self, task, deltatime):
        if self.canSave(task):
            task.updateActivationTime(task.initTime + deltatime)
            self.savedTasks.append(task)
            self.content += task.datasize
            return True

        # task.federateOwner.discardTask(self, task)
        return False

    def removeSavedTask(self, task):
        assert task in self.savedTasks
        self.content -= task.datasize
        self.savedTasks.remove(task)

    def updateGraph(self, context):
        self.Graph.graphList = context.Graph.getGraphList()
        self.Graph.graphOrder = context.Graph.getGraphOrder()
        self.Graph.elementOwners = context.Graph.getElementOwners()
        self.Graph.createGraph()

    def pickupTask(self, currentTasks, taskid):
        # print "elementLite - taskid:", self.name, taskid, self.section
        if not self.isGEO() or random.random()<self.pickupprobablity:
            # print "it is satellite"
            # print "current tasks:", currentTasks
            # print self.section
            # print currentTasks[self.section].qsize()
            # assert not currentTasks[self.section].empty()
            tempqueue = currentTasks[self.section].queue
            temptask = tempqueue[0]
            if not self.canSave(temptask):
                # print "cannot save"
                return False

            nextTask = currentTasks[self.section].get()
            # print nextTask
            # print "task time:", nextTask.initTime, nextTask.federateOwner
            nextTask.setID(taskid)
            nextTask.updateFederateOwner(self.federateOwner)
            nextTask.setSection(self.section)
            nextTask.setTime(self.federateOwner.time)
            # print "element next task inittime:", self.name, taskid, nextTask.initTime
            self.queuedTasks.put(nextTask)
            self.federateOwner.reportPickup(nextTask)
            return True

        return False






