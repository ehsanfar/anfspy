
class Task():
    def __init__(self, time, id = None, federate = None, value = 1000, computational = 1., expirationtime = 5, datasize = 1.):
        """
        @param demand: the demand for this contract
        @type demand: L{Demand}
        """
        self.taskid = id
        self.value = value
        self.computationresource = computational
        self.datasize = datasize
        self.expirationtime = expirationtime
        self.duration = 1
        self.elapsedTime = 0
        self.initTime = time
        self.activationTime = time + 1
        self.active = True
        self.nextstop = None
        self.federateOwner = federate
        self.initSection = None
        self.pathlist = []
        self.pathcost = 0.
        self.defaultvalue = -1*self.value / 5.

    def getValue(self, time):
        """
        Gets the current value of this contract.
        @return: L{float}
        """
        # print time, self.initTime
        self.elapsedTime = time - self.initTime
        revisedvalue = self.value if self.elapsedTime<=self.duration else -self.value/5. if self.elapsedTime>self.expirationtime \
            else self.value*(1. - (self.elapsedTime-self.duration)/(2.*(self.expirationtime-self.duration)))
        return revisedvalue

    def updateFederateOwner(self, federate):
        self.federateOwner = federate

    def setID(self, id):
        self.taskid = id

    def getID(self):
        return self.taskid

    def setSection(self, loc):
        self.initSection = loc

    def getSection(self):
        return self.initSection

    def updateActivationTime(self, activationtime):
        self.activationTime = activationtime

    def updatePath(self, pathlist, pathcost):
        self.pathlist = pathlist
        self.pathcost = pathcost

    def setTime(self, time):
        # print "task setTime:", time
        self.initTime = time
        self.activationTime = self.initTime + self.duration



