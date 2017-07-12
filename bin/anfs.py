
import argparse
import itertools
import logging
import pymongo
# from scoop import futures
import sys, os
import re
import networkx as nx
import random
# add ofspy to system path
sys.path.append(os.path.abspath('..'))

db = None  # lazy-load if required

from anfspy.elementLite import Satellite, GroundStation
from anfspy.federateLite import FederateLite
from anfspy.federateLite import FederateLite
from anfspy.contextLite import ContextLite
from anfspy.graphdrawfunctions import findAllPaths
from anfspy.task import Task
from anfspy.auctioneer import Auctioneer

import socket
import json

"""
def queryCase((dbHost, dbPort, dbName, elements, numPlayers, initialCash, numTurns, seed, ops, fops)):
    pass
    Queries and retrieves existing results or executes an OFS simulation.
    @param dbHost: the database host
    @type dbHost: L{str}
    @param dbPort: the database port
    @type dbPort: L{int}
    @param dbName: the database collection name
    @type dbName: L{str}
    @param elements: the design specifications
    @type elements: L{list}
    @param numPlayers: the number of players
    @type numPlayers: L{int}
    @param initialCash: the initial cash
    @type initialCash: L{int}
    @param numTurns: the number of turns
    @type numTurns: L{int}
    @param seed: the random number seed
    @type seed: L{int}
    @param ops: the operations definition
    @type ops: L{str}
    @param fops: the federation operations definition
    @type fops: L{str}
    @return: L{list}
    # print "elements:", elements
    global db
    dbHost = socket.gethostbyname(socket.gethostname())
    # print dbHost, dbPort, dbName, db
    # print "fops:", fops
    if re.match('x\d+,\d+,.', fops) is not None:
        args = re.search('x(\d+),(\d+),.',
                         fops)
        costSGL = int(args.group(1))
        costISL = int(args.group(2))
    elif 'xv,v' in fops:
        costSGL = 'v'
        costISL = 'v'
    else:
        costSGL = 0
        costISL = 0

    # print costISL, costSGL

    if db is None and dbHost is None:
        # print "db is None adn dbHOst is None"
        return executeCase((elements, numPlayers, initialCash,
                            numTurns, seed, ops, fops))
    elif db is None and dbHost is not None:
        # print "read from database"
        db = pymongo.MongoClient(dbHost, dbPort).ofs

    query = {u'experiment': experiment,
             u'elements': ' '.join(elements),
             u'numPlayers': numPlayers,
             u'initialCash': initialCash,
             u'numTurns': numTurns,
             u'seed': seed,
             u'ops': ops,
             u'fops': fops,
             u'costSGL': costSGL,
             u'costISL': costISL,
             }

    doc = None
    if dbName is not None:
        doc = db[dbName].find_one(query)
    if doc is None:
        db.results.remove({}) #this is temporary, should be removed afterwards
        doc = db.results.find_one(query)
        if doc is None:
            results, transRevenue, transCounter = executeCase((elements, numPlayers, initialCash,
                                   numTurns, seed, ops, fops))

            doc = {u'experiment': experiment,
                   u'elements': ' '.join(elements),
                   u'numPlayers': numPlayers,
                   u'initialCash': initialCash,
                   u'numTurns': numTurns,
                   u'seed': seed,
                   u'ops': ops,
                   u'fops': fops,
                   u'costSGL': costSGL,
                   u'costISL': costISL,
                   u'results': results,
                   u'transRevenue': json.dumps(transRevenue),
                   u'tarnsCounter': json.dumps(transCounter)
                    }
            db.results.insert_one(doc)

        if dbName is not None:
            db[dbName].insert_one(doc)

    return [tuple(result) for result in doc[u'results']]
"""

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="This program runs an OFS experiment.")

    args = parser.parse_args()

        # count number of players

    numPlayers = args.numPlayers if 'numPlayers' in args else 2

    # with open('designs.txt', 'r') as f:
    #     hardcoded_designs = f.readlines()
    #     # for l in f:
    #     #     print l
    #     #     hardcoded_designs.append(l)
    # hardcoded_designs = [x.strip() for x in hardcoded_designs]
    networks = ([
        {"nodes": [(4, "1.MediumSat"), (5, "1.MediumSat"), (6, "2.MediumSat"), (7, "2.MediumSat"), (8, "2.MediumSat"),
                    (1, "3.MediumSat"), (2, "3.MediumSat"), (3, "3.MediumSat"), (10, "1.GroundSta"), (11, "2.GroundSta"), (9, "3.GraundSta")],
         "edges": [(1,7), (4,7), (4,2), (6,2), (7,3), (7,5), (2,5), (2,8), (3,11), (5,9), (8,10), (3,9), (5,11), (5,10), (8,9)],
        "sources": [1, 4, 6],
        "destinations": [9, 10, 11]
         }
    ])
    context = ContextLite()

    for net in networks:
        elements = []
        numelemenentdict = {}
        nodes = [a[0] for a in net["nodes"]]
        fednum = sorted(list(set([a[1][0] for a in net["nodes"]])))
        federates = [FederateLite(name = 'F'+i, context = context) for i in fednum]
        namefederatedict = {f.name: f for f in federates}
        numfeddict = {n:f for (n, f) in zip(fednum, federates)}
        for node in net["nodes"]:
            n = node[1][0]
            federate = numfeddict[n]
            if 'Sat' in node[1]:
                element = Satellite(federate = federate, name = 'S.%s.%d'%(federate.name, len(federate.satellites)+1), location = 'MEO1', cost = 800)
                federate.satellites.append(element)
            else:
                element = GroundStation(federate = federate, name = 'G.%s.%d'%(federate.name, len(federate.stations)+1), location = 'SUR1', cost = 800)
                federate.stations.append(element)

            federate.elements.append(element)
            elements.append(element)
            numelemenentdict[node[0]] = element.name

        # print("numelementdict:", numelemenentdict)
        edges = [(numelemenentdict[x], numelemenentdict[y]) for (x,y) in net["edges"]]
        G = nx.DiGraph()
        names = [e.name for e in elements]
        G.add_nodes_from(names)
        G.add_edges_from(edges)
        sources = [numelemenentdict[x] for x in net["sources"]]
        destinations = [numelemenentdict[x] for x in net["destinations"]]

        nodeelementdict = {e.name: e for e in elements}
        # print("ndoe element dict:", 'S.F3.1' in nodeelementdict, namefederatedict.keys())

        # sourcetasks = [(s, Task(time = 0, id = i, element = nodeelementdict[s],federate = namefederatedict[re.search(r'.+\.(F\d)\..+', s).group(1)])) for i, s in enumerate(sources)]

        nodefederatedict = {n: namefederatedict[re.search(r'.+\.(F\d)\..+', n).group(1)] for n in names}

        for f in federates:
            f.nodeElementDict = nodeelementdict

        auctioneer = Auctioneer(nodes = names, nodefederatedict = nodefederatedict, nodeelementdict = nodeelementdict)

        # print "name to federate dict: ", namefederatedict
        T = 3
        taskid = 0

        for t in range(T):
            p = 0.3
            sources = []
            sourcetasks = []
            while not sources:
                sources = [numelemenentdict[r] for r in range(1,9) if random.random()<p]
            for s in sources:
                sourcetasks.append((s, Task(time = 0, id = taskid, element = nodeelementdict[s],federate = namefederatedict[re.search(r'.+\.(F\d)\..+', s).group(1)])))
                taskid += 1

            for source, task in sourcetasks:
                nodelists = findAllPaths(G, [source], destinations)
                for nodelist in nodelists:
                    # print("Add path:", nodelist)
                    auctioneer.addPath(task, [nodeelementdict[n] for n in nodelist])

            # print [(x.taskid, y) for (x, y) in auctioneer.pathdict.items()]
            # print("auctioneer path dictionary:", auctioneer.pathdict)
            auctioneer.inquirePrice()
            # for path in auctioneer.pathlist:
            #     # print("Task federate:", path.task.federateOwner.name)
            #     # print("path list:", path.nodelist)
            #     print("path cost and nodelist:", path.pathBid, path.nodelist)
            # print("anfs: auctioneer path cost:", [path.pathBid for path in auctioneer.pathlist])
            # auctioneer.findCompatibleBundles()
            auctioneer.findBestBundle()
            print("Best bundle cost:", auctioneer.currentBestPathBundle.bundleCost, auctioneer.currentBestPathBundle.bundleRevenue)
            auctioneer.evolveBundles()
            auctioneer.deliverTasks()

        for f in federates:
            print(f.name, f.cash)
        for path in auctioneer.currentBestPathBundle.pathlist:
            print(path.nodelist ,path.getPathPrice())





