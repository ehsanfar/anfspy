
from .contextLite import ContextLite


class OFSL(object):
    def __init__(self, elements, numPlayers,
                 numTurns, seed, ops, fops):

        self.context = ContextLite()

        self.time = 0
        self.initTime = 0
        self.maxTime = numTurns
        self.elements = elements
        # print "OFSL elements:", elements

        self.context.init(self)
        self.execute()



    def execute(self):
        """
        Executes an OFS.
        @return: L{list}
        """
        self.time = self.initTime
        for i in range(self.initTime, self.maxTime):
            # print self.time
            self.time += 1
            self.context.ticktock(self)

        # self.context.Graph.drawGraphs()
        for e in self.context.elements:
            print e.name, len(e.savedTasks)

        for f in self.context.federates:
            print f.name, f.cash
            print "task duration and value dictionary and counter:"
            print f.taskduration
            print f.taskvalue
            print f.taskcounter


