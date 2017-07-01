
import argparse
import itertools
import logging
import pymongo
from scoop import futures
import sys, os
import re

# add ofspy to system path
sys.path.append(os.path.abspath('..'))

db = None  # lazy-load if required

from ofspy.ofsLite import OFSL
import socket
import json



def execute(dbHost, dbPort, dbName, start, stop, cases, numPlayers,
            initialCash, numTurns, ops, fops):
    """
    Executes a general experiment.
    @param dbHost: the database host
    @type dbHost: L{str}
    @param dbPort: the database port
    @type dbPort: L{int}
    @param dbName: the database collection name
    @type dbName: L{str}
    @param start: the starting seed
    @type start: L{int}
    @param stop: the stopping seed
    @type stop: L{int}
    @param cases: the list of designs to execute
    @type cases: L{list}
    @param numPlayers: the number of players
    @type numPlayers: L{int}
    @param initialCash: the initial cash
    @type initialCash: L{int}
    @param numTurns: the number of turns
    @param numTurns: the number of turns
    @type numTurns: L{int}
    @param ops: the operations definition
    @type ops: L{str}
    @param fops: the federation operations definition
    @type fops: L{str}
    """
    # print "cases:", cases
    # print start, stop
    executions = [(dbHost, dbPort, dbName,
                   [e for e in elements.split(' ') if e != ''],
                   numPlayers, initialCash, numTurns, seed, ops, fops)
                  for (seed, elements) in itertools.product(range(start, stop), cases)]
    numComplete = 0.0
    logging.info('Executing {} cases with seeds from {} to {} for {} total executions.'
                 .format(len(cases), start, stop, len(executions)))
    # for results in futures.map(queryCase, executions):
    # results = futures.map(queryCase, executions)
    futures.map(queryCase, executions)
    # print "results :", results
    # N = len(results[0])
    # This line calculates the average of each element of each tuple for all the lists in the results, in other words assuming that each tuple of each results shows one seed of the same identity
    # print [[sum(x)/float(N) for x in zip(*l)] for l in [[l[j] for l in results] for j in range(N)]]


def queryCase((dbHost, dbPort, dbName, elements, numPlayers,
              initialCash, numTurns, seed, ops, fops)):
    """
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
    """
    # print "elements:", elements
    executeCase((elements, numPlayers, initialCash,
                 numTurns, seed, ops, fops))
    """
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

def executeCase((elements, numPlayers, initialCash, numTurns, seed, ops, fops)):
    """
    Executes an OFS simulation.
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
    """
    # print "ofs-exp-vs elements: ", elements
    #
    # return OFSL(elements=elements, numPlayers=numPlayers, initialCash=initialCash, numTurns=numTurns, seed=seed, ops=ops, fops=fops).execute()
    OFSL(elements=elements, numPlayers=numPlayers, numTurns=numTurns, seed=seed, ops=ops, fops=fops)




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="This program runs an OFS experiment.")
    # parser.add_argument('experiment', type=str, nargs='+',
    #                     help='the experiment to run: masv or bvc')
    parser.add_argument('-d', '--numTurns', type=int, default=24,
                        help='simulation duration (number of turns)')
    parser.add_argument('-p', '--numPlayers', type=int, default=None,
                        help='number of players')
    parser.add_argument('-i', '--initialCash', type=int, default=None,
                        help='initial cash')
    parser.add_argument('-o', '--ops', type=str, default='d6',
                        help='federate operations model specification')
    parser.add_argument('-f', '--fops', type=str, default='',
                        help='federation operations model specification')
    parser.add_argument('-l', '--logging', type=str, default='error',
                        choices=['debug', 'info', 'warning', 'error'],
                        help='logging level')
    parser.add_argument('-s', '--start', type=int, default=0,
                        help='starting random number seed')
    parser.add_argument('-t', '--stop', type=int, default=20,
                        help='stopping random number seed')
    parser.add_argument('--dbHost', type=str, default=None,
                        help='database host')
    parser.add_argument('--dbPort', type=int, default=27017,
                        help='database port')

    args = parser.parse_args()

        # count number of players

    numPlayers = args.numPlayers if 'numPlayers' in args else 2

    # with open('designs.txt', 'r') as f:
    #     hardcoded_designs = f.readlines()
    #     # for l in f:
    #     #     print l
    #     #     hardcoded_designs.append(l)
    # hardcoded_designs = [x.strip() for x in hardcoded_designs]
    hardcoded_designs = (
        # "1.GroundSta@SUR1,oSGL 2.GroundSta@SUR3,oSGL 1.MediumSat@MEO3,VIS,SAR,oSGL,oISL  2.MediumSat@MEO5,VIS,SAR,oSGL,oISL",
        "1.SmallSat@MEO6,oSGL,oISL 1.MediumSat@MEO4,VIS,SAR,oSGL,oISL 2.SmallSat@MEO2,oSGL,oISL 2.MediumSat@MEO1,VIS,SAR,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        # "1.SmasllSat@MEO6,oSGL,oISL 1.SmallSat@MEO5,oSGL,oISL 1.LargeSat@MEO4,VIS,SAR,DAT,oSGL,oISL 2.SmallSat@MEO3,oSGL,oISL 2.SmallSat@MEO2,oSGL,oISL 2.LargeSat@MEO1,VIS,SAR,DAT,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        # "1.SmallSat@MEO6,oSGL,oISL 1.MediumSat@MEO5,DAT,oSGL,oISL 1.MediumSat@MEO4,VIS,SAR,oSGL,oISL 2.SmallSat@MEO3,oSGL,oISL 2.MediumSat@MEO2,DAT,oSGL,oISL 2.MediumSat@MEO1,VIS,SAR,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        # "1.SmallSat@MEO6,oSGL,oISL 1.MediumSat@MEO5,DAT,oSGL,oISL 1.LargeSat@MEO4,VIS,SAR,DAT,oSGL,oISL 2.SmallSat@MEO3,oSGL,oISL 2.MediumSat@MEO2,DAT,oSGL,oISL 2.LargeSat@MEO1,VIS,SAR,DAT,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        "1.SmallSat@LEO6,oSGL,oISL 1.MediumSat@MEO5,VIS,SAR,oSGL,oISL 1.MediumSat@MEO4,VIS,SAR,oSGL,oISL 2.SmallSat@MEO3,oSGL,oISL 2.MediumSat@MEO2,VIS,SAR,oSGL,oISL 2.MediumSat@MEO1,VIS,SAR,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        # "1.SmallSat@MEO6,oSGL,oISL 1.MediumSat@MEO5,VIS,SAR,oSGL,oISL 1.LargeSat@MEO4,VIS,SAR,DAT,oSGL,oISL 2.SmallSat@MEO3,oSGL,oISL 2.MediumSat@MEO2,VIS,SAR,oSGL,oISL 2.LargeSat@MEO1,VIS,SAR,DAT,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        # "1.MediumSat@MEO6,VIS,oSGL,oISL 1.MediumSat@MEO5,VIS,oSGL,oISL 1.LargeSat@MEO4,VIS,SAR,DAT,oSGL,oISL 2.MediumSat@MEO3,VIS,oSGL,oISL 2.MediumSat@MEO2,VIS,oSGL,oISL 2.LargeSat@MEO1,VIS,SAR,DAT,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        # "1.MediumSat@MEO6,VIS,oSGL,oISL 1.MediumSat@MEO5,VIS,DAT,oSGL,oISL 1.LargeSat@MEO4,VIS,SAR,DAT,oSGL,oISL 2.MediumSat@MEO3,VIS,oSGL,oISL 2.MediumSat@MEO2,VIS,DAT,oSGL,oISL 2.LargeSat@MEO1,VIS,SAR,DAT,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        # "1.MediumSat@MEO6,VIS,SAR,oSGL,oISL 1.MediumSat@MEO5,VIS,SAR,oSGL,oISL 1.LargeSat@MEO4,VIS,SAR,DAT,oSGL,oISL 2.MediumSat@MEO3,VIS,SAR,oSGL,oISL 2.MediumSat@MEO2,VIS,SAR,oSGL,oISL 2.LargeSat@MEO1,VIS,SAR,DAT,oSGL,oISL 1.GroundSta@SUR1,oSGL 2.GroundSta@SUR4,oSGL",
        #
        # "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.SmallSat@MEO%d,oSGL,oISL 1.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 2.SmallSat@LEO%d,oSGL,oISL 2.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 3.SmallSat@LEO%d,oSGL,oISL 3.MediumSat@MEO%d,VIS,SAR,oSGL,oISL"%(1,4,5,1,3,6,4,5,2),
        # "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.SmallSat@MEO%d,oSGL,oISL 1.SmallSat@MEO%d,oSGL,oISL 1.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 2.SmallSat@MEO%d,oSGL,oISL 2.SmallSat@MEO%d,oSGL,oISL 2.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 3.SmallSat@MEO%d,oSGL,oISL 3.SmallSat@MEO%d,oSGL,oISL 3.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL"%(1,3,5,1,3,6,3,5,2,5,1,4),
        # "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.SmallSat@MEO%d,oSGL,oISL 1.MediumSat@MEO%d,DAT,oSGL,oISL 1.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 2.SmallSat@MEO%d,oSGL,oISL 2.MediumSat@MEO%d,DAT,oSGL,oISL 2.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 3.SmallSat@MEO%d,oSGL,oISL 3.MediumSat@MEO%d,DAT,oSGL,oISL 3.MediumSat@MEO%d,VIS,SAR,oSGL,oISL"%(1,3,5,1,3,6,3,5,2,5,1,4),
        # "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.SmallSat@MEO%d,oSGL,oISL 1.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 1.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 2.SmallSat@MEO%d,oSGL,oISL 2.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 2.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 3.SmallSat@MEO%d,oSGL,oISL 3.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 3.MediumSat@MEO%d,VIS,SAR,oSGL,oISL"%(1,3,5,1,3,6,3,5,2,5,1,4),
        # "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.SmallSat@MEO%d,oSGL,oISL 1.MediumSat@MEO%d,DAT,oSGL,oISL 1.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 2.SmallSat@MEO%d,oSGL,oISL 2.MediumSat@MEO%d,DAT,oSGL,oISL 2.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 3.SmallSat@MEO%d,oSGL,oISL 3.MediumSat@MEO%d,DAT,oSGL,oISL 3.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL"%(1,3,5,1,3,6,3,5,2,5,1,4),
        #  "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.SmallSat@MEO%d,oSGL,oISL 1.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 1.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 2.SmallSat@MEO%d,oSGL,oISL 2.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 2.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 3.SmallSat@MEO%d,oSGL,oISL 3.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 3.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL"%(1,3,5,1,3,6,3,5,2,5,1,4),
        # "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.MediumSat@MEO%d,VIS,oSGL,oISL 1.MediumSat@MEO%d,VIS,oSGL,oISL 1.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 2.MediumSat@MEO%d,VIS,oSGL,oISL 2.MediumSat@MEO%d,VIS,oSGL,oISL 2.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 3.MediumSat@MEO%d,VIS,oSGL,oISL 3.MediumSat@MEO%d,VIS,oSGL,oISL 3.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL"%(1,3,5,1,3,6,3,5,2,5,1,4),
        # "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.MediumSat@MEO%d,VIS,oSGL,oISL 1.MediumSat@MEO%d,VIS,DAT,oSGL,oISL 1.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 2.MediumSat@MEO%d,VIS,oSGL,oISL 2.MediumSat@MEO%d,VIS,DAT,oSGL,oISL 2.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 3.MediumSat@MEO%d,VIS,oSGL,oISL 3.MediumSat@MEO%d,VIS,DAT,oSGL,oISL 3.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL"%(1,3,5,1,3,6,3,5,2,5,1,4),
        # "1.GroundSta@SUR%d,oSGL 2.GroundSta@SUR%d,oSGL 3.GroundSta@SUR%d,oSGL 1.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 1.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 1.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 2.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 2.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 2.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL 3.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 3.MediumSat@MEO%d,VIS,SAR,oSGL,oISL 3.LargeSat@MEO%d,VIS,SAR,DAT,oSGL,oISL"%(1,3,5,1,3,6,3,5,2,5,1,4),
    )
    experiment = 'auctioneer'
    for design in hardcoded_designs:
        # print design
        if '4.' in design:
            numPlayers = 4
        elif '3.' in design:
            numPlayers = 3
        else:
            numPlayers = 2

        stop = args.start + 1
        execute(args.dbHost, args.dbPort, None, args.start, stop,
                [design],
                numPlayers, args.initialCash, args.numTurns,
                None, None)

        # for ops, fops in [('d6,a,1', 'x')]:#[('n', 'd6,a,1'), ('d6,a,1', 'n'), ('d6,a,1', 'x')]:#[('d6,a,1', 'x')]:#
        #     if 'x' in fops:
        #         stop = args.start + 1
        #         # costsgl = costisl = 'v'
        #         for costsgl in [a for a in range(500, 601, 200)]:# if a not in range(0, 1501,100)]:
        #             # print "cost SGL:", costsgl
        #             costisl = costsgl//2
        #             fops = "x%s,%s,6,a,1"%(str(costsgl),str(costisl))
        #             # print "fops:", fops
        #             # print "ofs-exp-vs Design:",
        #             execute(args.dbHost, args.dbPort, None, args.start, stop,
        #                 [design],
        #                 numPlayers, args.initialCash, args.numTurns,
        #                 ops, fops, experiment)
        #     else:
        #         stop = args.start + 1
        #         # print "fops:", fops
        #         execute(args.dbHost, args.dbPort, None, args.start, stop,
        #                 [design],
        #                     numPlayers, args.initialCash, args.numTurns,
        #                     ops, fops, experiment)
        # else:
        #     execute(args.dbHost, args.dbPort, None, args.start, args.stop,
        #             [' '.join(args.experiment)],
        #             numPlayers, args.initialCash, args.numTurns,
        #             args.ops, args.fops, 0, 0)
