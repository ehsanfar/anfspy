
"""
Operations class.
"""

import math
import itertools
import re
import sys

class Operations(object):
    def __init__(self):
        self.penaltyMemo = {}
        self.costISL = None
        self.costSGL = None
        self.groundSections = None
    
    def execute(self, controller, context):
        """
        Executes this operations model.
        @param controller: the controller for this operations model
        @type controller: L{Entity}
        @param context: the context of operations
        @type context: L{Context}
        """
        pass

    def findpossiblelocations(self, mylocation):
        possiblelocs = []
        element_section = int(re.search(r'.+(\d)', mylocation).group(1))
        if 'LE' in mylocation:
            return ['LE%d'%((i-1)%6+1) for i in range(element_section, element_section+6, 2)]
        elif 'ME' in mylocation:
            return ['ME%d'%((i-1)%6+1) for i in range(element_section, element_section+6)]


    # def finddeltatime(self, stationloc, elementloc, groundSections):
    #     station_section = int(re.search(r'.+(\d)', stationloc).group(1))
    #     element_section = int(re.search(r'.+(\d)', elementloc).group(1))
    #
    #     contract_deltatime = []
    #     loc_diff = 0
    #     if 'LE' in elementloc:
    #         if element_section % 2 != station_section % 2:
    #             return None
    #
    #     if element_section == station_section:
    #         return None
    #
    #     for i in range(element_section+1, station_section+1) if station_section>element_section else range(element_section+1, 7)+range(0, station_section+1):
    #             if 'LE' in elementloc:
    #                 if i%2 == element_section%2 and i in groundSections:
    #                     contract_deltatime.append(station_section-i if station_section>i else (6-i)+station_section)
    #                     loc_diff += 1
    #
    #             if 'ME' in elementloc and i in groundSections:
    #                 contract_deltatime.append(station_section - i if station_section > i else (6 - i) + station_section)
    #                 loc_diff += 1
    #
    #     return contract_deltatime

    def findnextstationandsteps(self, elementloc, groundSections):
        element_section = int(re.search(r'.+(\d)', elementloc).group(1))
        steps = []
        N = 0
        if 'LE' in elementloc:
            N = 3
        elif 'ME' in elementloc:
            N = 6

        for i in range(N):
            element_section += 6/N
            element_section = (element_section-1)%6+1
            steps.append(element_section)
            if element_section in groundSections:
                return (element_section, steps)

        return (None, [])





    def getStoragePenalty(self, phenomenon, element, context, time, timestep, type = None):
        # print element, element.time, time, timestep
        if element.time[phenomenon] == time:
            storagelist = element.storagePenalty[phenomenon]
            return storagelist[timestep%len(storagelist)]
        # else:
        #
        #     element.time = time
        # if not element in self.penaltyMemo:
        #     demands = [e for e in context.events
        #                if e.isDemand()
        #                and element.couldSense(e.generateData())]
        #                #and (element.couldSense(e.generateData())
        #                #     or (any(m.isTransceiver() and m.isISL()
        #                #             for m in element.modules)))]
        #     values = [0]
        #     values.extend(map(lambda d: d.getValueAt(0), demands))
        #     values = list(set(values))
        #     values.sort()
        #     counts = map(lambda v: len([d for d in demands
        #                                 if d.getValueAt(0) == v]), values)
        #     counts[0] += len(context.events) - len(demands)
        #     print math.pow(sum(counts[0:values.index(values[-1])+1]), 1), math.pow(sum(counts[0:values.index(values[-1])]), 1)
        #     expValMax = reduce(lambda e, v:
        #                        e + v*(math.pow(sum(counts[0:values.index(v)+1]), 1)
        #                               - math.pow(sum(counts[0:values.index(v)]), 1))
        #                        / math.pow(sum(counts),1), values)
        #
        #     print values
        #     print counts
        #     print expValMax
        #     self.penaltyMemo[element] = -1*max(100, expValMax) # minimum penalty 100
        # print "time:", time
        myfederate = context.getElementOwner(element)
        federation = context.federations
        allfederates = [f.federates for f in context.federations][0]

        # print "Objective type:", type
        if type == 'independent':
            allstations = [e for e in myfederate.getElements() if e.isGround()]
            if not myfederate.groundSections:
                myfederate.groundSections = [int(re.search(r'.+(\d)', s.getLocation()).group(1)) for s in allstations]
                # print "Element ground Sections:", myfederate.groundSections

            groundSections = myfederate.groundSections

        else:
            allstations = list(itertools.chain.from_iterable([[e for e in f.getElements() if e.isGround()] for f in allfederates]))
            # print [s.getLocation() for s in allstations]
            if not self.groundSections:
                self.groundSections = [int(re.search(r'.+(\d)', s.getLocation()).group(1)) for s in allstations]
                # print "All Ground Sections:", self.groundSections

            groundSections = self.groundSections

        element.time[phenomenon] = time
        possiblelocations = self.findpossiblelocations(element.getLocation())
        storagepenaltylist = []
        demand_value = element.getDemandValue(phenomenon)

        nextstation, step = self.findnextstationandsteps(element.getLocation(), groundSections)

        prob = element.getDemandProb(phenomenon)
        # print element.getLocation(), groundSections, nextstation, step

        storagepenaltylist = []

        for mylocation in possiblelocations:
            nextstation, step = self.findnextstationandsteps(mylocation, groundSections)
            # print "Operation: mylocation, nextstation, steps:", mylocation, nextstation, step
            owners = [context.getElementOwner(st) for st in allstations if int(re.search(r'.+(\d)', st.getLocation()).group(1)) == nextstation]
            # print "Owners: ", owners
            costSGLlist = [0 if o is myfederate else o.getCost('oSGL', type = type) for o in owners]
            costSGL = min(costSGLlist)
            deltatime = [nextstation - s if nextstation>=s else nextstation+6-s for s in step]
            # print mylocation, nextstation, step, deltatime
            storagepenalty = -1*int(sum([max((demand_value[min(dt, 5)] - costSGL)*prob, 0) for dt in deltatime]))
            storagepenaltylist.append(storagepenalty)

        #     for st in allstations:
        #         st_loc = st.getLocation()
        #         # print st_loc, mylocation
        #         deltatime = self.finddeltatime(st_loc, mylocation, groundSections)
        #         # print "My location, station location, groundSecitons, delta time:", mylocation, st_loc, groundSections, deltatime
        #         # print "Mylocation, stationlocation, allground locations:", mylocation, st_loc, deltatime
        #         prob = element.getDemandProb()
        #         # print element, " probability:", prob
        #         owner = context.getElementOwner(st)
        #         # print owner, myfederate
        #         costSGL = 0 if owner is myfederate else owner.getCost('oSGL')
        #         # print "counter:", counter
        #         newstorageopportunitycost = 0
        #         # print demand_value, deltatime
        #         if deltatime:
        #             # print [(demand_value[min(dt, 5)] - costSGL) * prob for dt in deltatime]
        #             newstorageopportunitycost = sum([max((demand_value[min(dt, 5)] - costSGL)*prob, 0) for dt in deltatime])
        #
        #         # print "New storage opportunity designCost:", prob, costSGL, newstorageopportunitycost
        #         storage_opportunitycost.append(max(0, newstorageopportunitycost))
        #
        #     # print "Storage Opportunity designCost:", storage_opportunitycost
        #     storagepenaltylist.append(-round(max(storage_opportunitycost),2))
        #
        # # print "Update storage penalty:", storagepenaltylist
        # element.storageOpportunity = storagepenaltylist
        element.storagePenalty[phenomenon] = storagepenaltylist
        # print element, time, element.storagePenalty
        return storagepenaltylist[timestep%len(storagepenaltylist)]

