from .graphdrawfunctions import convertPath2Edge
from .path import Path
from .bundle import EdgeBundle, PathBundle
import itertools


class Auctioneer():
    def __init__(self, nodes, nodefederatedict, nodeelementdict):
        self.federates = nodefederatedict.values()
        self.namefederatedict = {f.name: f for f in self.federates}
        # print("Auctioneer nodes:",nodes)
        # print("Auctioneer federates:", self.namefederatedict)
        self.nodeFederateDict = nodefederatedict
        self.nodeElementDict = nodeelementdict
        self.nodes = nodes

        # print(self.federateDict)
        self.pathdict = {}
        self.pathlist = []
        self.edgebundlelist = []
        self.federateEdgeBundles = {}
        self.tasks = []
        self.compatibleBundles = None
        self.bundleBidDict = {}

    def reset(self):
        self.pathdict = {}

    def addPath(self, task, nodelist):
        taskid = task.taskid
        self.tasks.append(task)
        # obj = None
        # print("Task nodelist:", taskid.taskid, nodelist)
        obj = Path(task, nodelist)
        if taskid in self.pathdict:
            self.pathdict[taskid].append(obj)
        else:
            self.pathdict[taskid] = [obj]

        self.pathlist.append(obj)

    def updatePathFederateBundleDict(self, path):
        nodelist = path.getNodeList()
        # print("auctioneer: nodelist:", nodelist)
        edgelist = convertPath2Edge(nodelist)
        federatebundledict = {}
        for edge in edgelist:
            # print("auctioneer: edge:", edge)
            # print(self.nodes)
            federate = self.nodeFederateDict[edge[1]]
            if federate.name not in federatebundledict:
                federatebundledict[federate.name] = []

            federatebundledict[federate.name].append((edge))
            # print("Auctioneer: Find path fed dict:", federate.name, edge)

        # print("path:", nodelist, edgelist)
        # print("Auctioneer: federate and bundles:", [(a, len(b)) for (a,b) in federatebundledict.items()])
        federatebundledict = {k: EdgeBundle(v, path, self.namefederatedict[k]) for (k, v) in federatebundledict.items()}

        path.updateBundles(federatebundledict)
        # print("Path and federate bundle list:", path.nodelist, [b.edgelist for b in federatebundledict.values()])
        self.edgebundlelist.extend(federatebundledict.values())
        # print("Auctioneer: federatebundledict:", federatebundledict)
        return federatebundledict

    def setDict2Dict(self, dict1, dict2):
        for key in dict2:
            # print("dict key and dict1 and dict2:", key, dict1[key] if key in dict1 else None, dict2[key])
            if key in dict1:
                # print("2 bundles:", dict1[key], dict2[key])
                dict1[key] = dict1[key].union(set([dict2[key]]))
            else:
                # print("bundle edgelist:", dict2[key].edgelist)
                dict1[key] = set([dict2[key]])
        return dict1

    def uniquePermutations(self, indexlist):
        # print("indexlist:", indexlist)
        # print("uniquePermulations:", [[p.nodelist for p in pathlist] for pathlist in indexlist])
        ntasks = len(indexlist)
        permutations = []
        combinations =  []
        for n in range(1,ntasks+1):
            tempcombinations = itertools.combinations(range(ntasks), n)
            combinations += list(tempcombinations)

        for c in combinations:
            newlist = [indexlist[i] for i in c]
            # print("newlist:", newlist)
            tempproducts = itertools.product(*newlist)
            # print("Permutations:", [p.nodelist for p in list(tempproducts)])
            permutations.extend(list(tempproducts))

        # print("Unique products:", )
        return permutations


    def checkPathCombinations(self, pathlist):
        alledges = set([])
        # print("check path combination:", [p.nodelist for p in pathlist])
        for path in pathlist:
            newedges = set(convertPath2Edge(path.nodelist))
            # print("new edges:", newedges)
            intersection = alledges.intersection(newedges)
            # print("intersection:", intersection)

            if intersection:
                # print(False)
                return False

            alledges = alledges.union(newedges)
        # print(True)
        return True

    def updateCompatibleBundles(self, forced = False):
        if not self.compatibleBundles or forced:
            all_paths = list(self.pathdict.values())
            # print("Update compatible bundles: all paths:", all_paths)
            # print("All paths:", self.pathdict)
            probable_products = self.uniquePermutations(all_paths)
            possible_bundles = [PathBundle(plist) for plist in probable_products if self.checkPathCombinations(plist)]

            # print("Auctioneer: possible path combinations:", [p.pathlist for p in possible_bundles])
            # print([t.length for t in possible_bundles])
            self.compatibleBundles = possible_bundles
            # return possible_bundles

        for pathbundle in self.compatibleBundles:
            pathbundle.updateValues()

    def updateBundleBid(self):
        for edgebundle in self.edgebundlelist:
            edgebundle.updateBid(self.bundleBidDict[edgebundle])

    def updateBundles(self):
        for path in self.pathlist:
            path.updateValues()

        self.updateCompatibleBundles()
        return self.findBestBundle()

    def removeBundles(self, bundlelist):
        # print([b.edgelist for b in bundlelist], " are removed")
        self.edgebundlelist = sorted([b for b in self.edgebundlelist if b not in bundlelist])
        bundleset = set(bundlelist)
        # for p in self.pathlist:
        #     print("path and intersection with bundles:", p.nodelist, [b.edgelist for b in set(p.edgebundles).intersection(bundleset)])
        self.pathlist = [p for p in self.pathlist if not set(p.edgebundles).intersection(bundleset)]
        for taskid, paths in self.pathdict.items():
            newpaths = [p for p in paths if p in self.pathlist]
            self.pathdict[taskid] = newpaths

        emptykeys = [k for k in self.pathdict if not self.pathdict[k]]
        for k in emptykeys:
            self.pathdict.pop(taskid, None)

        self.updateCompatibleBundles(forced = True)


    def inquirePrice(self):
        federateBundleDict = {}
        for path in self.pathlist:
            tempdict = self.updatePathFederateBundleDict(path)
            # print("Auctioneer: path edge dict:", [(a, bundle.edgelist) for (a,bundle) in tempdict.items()])
            federateBundleDict = self.setDict2Dict(federateBundleDict, tempdict)

        # print("auctioneer: federateBundleDict:", federateBundleDict)
        # print("Auctioneer: federate and bundles:", [(f, [b.edgelist for b in bundles]) for (f,bundles) in federateBundleDict.items()])
        self.bundleBidDict = {}
        for fed, bundleset in federateBundleDict.items():
            bundlelist = list(bundleset)
            # print("Federate:", fed)
            # print("bundle list:", edgebundlelist)
            # print("Inquireprice: bundle list federates:", [[(self.nodeFederateDict[x].name, self.nodeFederateDict[y].name) for (x,y) in bundle.edgelist] for bundle in edgebundlelist])
            # print("Auctioneer: fed and bundleset", fed, [b.edgelist for b in edgebundlelist])
            tempdict = self.namefederatedict[fed].getBundleBid(bundlelist)
            # print("Auctioneer: asker federate protocol cost:", [(b.federateAsker.name, fed, c) for (b,c) in tempdict.items()])

            for b in tempdict:
                assert b not in self.bundleBidDict
                self.bundleBidDict[b] = tempdict[b]

            # bundleBidDict = {x: y for x,y in zip(edgebundlelist, costlist)}
        self.updateBundleBid()
        self.updateBundles()
        self.updateCompatibleBundles()

    def findBestBundle(self, compatiblebundels = []):
        # print("length of compatible bundles:", len(self.compatibleBundles))
        if compatiblebundels:
            possible_bundles = compatiblebundels
        else:
            possible_bundles = self.compatibleBundles if self.compatibleBundles else self.updateCompatibleBundles()

        if not possible_bundles:
            # self.currentBestPathBundle = None
            return False

        path_bundle_cost = [b.bundleCost for b in possible_bundles]
        path_bundle_revenue = [b.bundleRevenue for b in possible_bundles]
        path_bundle_profit = [x-y for (x,y) in zip(path_bundle_revenue, path_bundle_cost)]
        # path_bundle_length = [b.length for b in possible_bundles]
        # print("pathbundle cost:", path_bundle_cost)
        # sortedcost = sorted(list(zip(path_bundle_cost, path_bundle_length)))
        # print("sorted cost:", sortedcost)
        sorted_revenue = sorted(list(zip(path_bundle_profit, possible_bundles)), reverse = True)
        # print("sorted revenue:", [(x, [p.nodelist for p in y.pathlist]) for x,y in sorted_revenue[:1]])
        self.currentBestPathBundle = sorted_revenue[0][1]
        return True

    def checkBundleinBundle(self, pathbundle, edgebundle):
        all_bundles = []
        for path in pathbundle.pathlist:
            all_bundles.extend(path.edgebundles)

        # print("chekc bundle in bundle:", all_bundles)
        if edgebundle in all_bundles:
            return True
        return False

    def updateOpportunityCost(self):
        previousprofit = self.currentBestPathBundle.getBundleProfit()
        # print("Default profit is: ", previousprofit)
        # print(len(self.edgebundlelist))
        for b in self.edgebundlelist:
            profit_0 = profit_1 = taskProfit_0 = taskProfit_1 = 0
            # print("Update opp cost: length of compatible bbundles:", len(self.compatibleBundles))
            # print("bundle:", b.edgelist)
            tempprice = b.price
            b.updatePrice(0)
            if self.updateBundles():
                b.updatePrice(tempprice)
                profit_0 = self.currentBestPathBundle.getBundleProfit()
                taskProfit_0 = self.currentBestPathBundle.getTaskProfit(b.taskAsker)

            # self.findBestBundle(compatiblebundles)
            compatiblebundles = [pathbundle for pathbundle in self.compatibleBundles if not self.checkBundleinBundle(pathbundle, b)]
            if self.findBestBundle(compatiblebundles):
                profit_1 = self.currentBestPathBundle.getBundleProfit()
                taskProfit_1 = self.currentBestPathBundle.getTaskProfit(b.taskAsker)

            # b.updatePrice(10000)
            # self.updateBundles()
            # if not (profit_1<= previousprofit and profit_0>= previousprofit):
                # print("bundle max, min, OC, task OC:", list(b.edgelist), profit_0, profit_1, profit_0 - profit_1, taskProfit_0, taskProfit_1, taskProfit_0 - taskProfit_1)
            # assert profit_1<= previousprofit, profit_0>= previousprofit
            b.setGenOppCost(profit_0 - profit_1)
            # print("updated opportunity cost:", b.generalOpportunityCost)

        self.updateBundles()

    def evolveBundles(self):
        self.updateOpportunityCost()
        for b in self.edgebundlelist:
            b.updatePrice(max(b.getGeneralOppCost(), b.getBid()))

        # print("edge bundle list:", self.edgebundlelist, len(self.edgebundlelist))
        while True:
            # print("Evolve bundles")
            removelist = sorted([(b.getGeneralOppCost() - b.getBid(), b) for b in self.edgebundlelist if b.getGeneralOppCost() < b.getBid()])
            # print("remove list:", [(c, b.edgelist) for c,b in removelist[:1]])
            if not removelist:
                break
            self.removeBundles([r[1] for r in removelist[:1]])
            # print("length of self.edgebundlelist after remove:", len(self.edgebundlelist))
            self.updateOpportunityCost()

            # for b in self.edgebundlelist:
            #     # print("update price")
            #     b.updatePrice(b.generalOpportunityCost)
            #
            # self.updateBundles()
        self.findBestBundle()

    def deliverTasks(self):
        taskpath = [(p.task, p) for p in self.currentBestPathBundle.pathlist]
        for task, path in taskpath:
            task.updatePath(path)
            element = task.elementOwner
            print("Task final value and pathprice:", task.getValue(task.federateOwner.time) , path.pathPrice)
            if task.getValue(task.federateOwner.time) - path.pathPrice >0:
                element.deliverTask(task)

    # def offerPrice2Federates(self):
    #
    #     for b in self.edgebundlelist:
    #         federate = b.federateOwner
    #
    #         federate.grantBundlePrice(b)






















