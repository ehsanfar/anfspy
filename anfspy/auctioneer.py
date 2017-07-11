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
            if federate not in federatebundledict:
                federatebundledict[federate.name] = []

            federatebundledict[federate.name].append((edge))
            # print("Auctioneer: Find path fed dict:", federate.name, edge)

        federatebundledict = {k: EdgeBundle(v, path) for (k, v) in federatebundledict.items()}
        # print("Auctioneer: federate and bundles:", [(a, b.edgelist) for (a,b) in federatebundledict.items()])

        path.updateBundles(federatebundledict)
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
        # print("uniquePermulations:", [[p.nodelist for p in pathlist] for pathlist in indexlist])
        ntasks = len(indexlist)
        permutations = []
        combinations =  []
        for n in range(1,ntasks+1):
            tempcombinations = itertools.combinations(range(ntasks), n)
            combinations += list(tempcombinations)

        for c in combinations:
            newlist = [indexlist[i] for i in c]
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

    def updateCompatibleBundles(self):
        if not self.compatibleBundles:
            all_paths = list(self.pathdict.values())
            # print("All paths:", self.pathdict)
            probable_products = self.uniquePermutations(all_paths)
            possible_bundles = [PathBundle(plist) for plist in probable_products if self.checkPathCombinations(plist)]

            # print("Auctioneer: possible path combinations:", [p.pathlist for p in possible_bundles])
            # print([t.length for t in possible_bundles])
            self.compatibleBundles = possible_bundles
            # return possible_bundles

        for pathbundle in self.compatibleBundles:
            pathbundle.updateCost()

    def updateBundleCost(self):
        for edgebundle in self.edgebundlelist:
            edgebundle.updateCost(self.bundleCostDict[edgebundle])

        for path in self.pathlist:
            path.updateCost()

        self.updateCompatibleBundles()
        self.findBestBundle()


    def inquirePrice(self):
        federateBundleDict = {}
        for path in self.pathlist:
            tempdict = self.updatePathFederateBundleDict(path)
            # print("Auctioneer: path edge dict:", [(a, bundle.edgelist) for (a,bundle) in tempdict.items()])
            federateBundleDict = self.setDict2Dict(federateBundleDict, tempdict)

        # print("auctioneer: federateBundleDict:", federateBundleDict)
        # print("Auctioneer: federate and bundles:", [(f, [b.edgelist for b in bundles]) for (f,bundles) in federateBundleDict.items()])
        self.bundleCostDict = {}
        for fed, bundleset in federateBundleDict.items():
            bundlelist = list(bundleset)
            # print("Federate:", fed)
            # print("bundle list:", edgebundlelist)
            # print("Inquireprice: bundle list federates:", [[(self.nodeFederateDict[x].name, self.nodeFederateDict[y].name) for (x,y) in bundle.edgelist] for bundle in edgebundlelist])
            # print("Auctioneer: fed and bundleset", fed, [b.edgelist for b in edgebundlelist])
            tempdict = self.namefederatedict[fed].getBundleListCost(bundlelist, self.nodeElementDict)
            # print("Auctioneer: asker federate protocol cost:", [(b.parentFederate.name, fed, c) for (b,c) in tempdict.items()])

            for b in tempdict:
                assert b not in self.bundleCostDict
                self.bundleCostDict[b] = tempdict[b]

            # bundleCostDict = {x: y for x,y in zip(edgebundlelist, costlist)}
        self.updateBundleCost()
        self.updateCompatibleBundles()

    def findBestBundle(self):
        possible_bundles = self.compatibleBundles if self.compatibleBundles else self.updateCompatibleBundles()
        path_bundle_cost = [b.bundlecost for b in possible_bundles]
        path_bundle_revenue = [b.bundlerevenue for b in possible_bundles]
        path_bundle_profit = [x-y for (x,y) in zip(path_bundle_revenue, path_bundle_cost)]
        # path_bundle_length = [b.length for b in possible_bundles]
        # print("pathbundle cost:", path_bundle_cost)
        # sortedcost = sorted(list(zip(path_bundle_cost, path_bundle_length)))
        # print("sorted cost:", sortedcost)
        sorted_revenue = sorted(list(zip(path_bundle_profit, possible_bundles)), reverse = True)
        # print("sorted revenue:", [(x, [p.nodelist for p in y.pathlist]) for x,y in sorted_revenue[:1]])
        self.currentBestPathBundle = sorted_revenue[0][1]

    def updateOpportunityCost(self):
        previousprofit = self.currentBestPathBundle.getBundleProfit()
        print("Default profit is: ", previousprofit)
        for b in self.edgebundlelist:
            print("bundle:", b.edgelist)
            tempcost = self.bundleCostDict[b]
            self.bundleCostDict[b] = 0
            self.updateBundleCost()
            profit_0 = self.currentBestPathBundle.getBundleProfit()
            self.bundleCostDict[b] = 1000
            self.updateBundleCost()
            profit_1 = self.currentBestPathBundle.getBundleProfit()
            self.bundleCostDict[b] = tempcost
            assert profit_1<= previousprofit, profit_0>= previousprofit
            print("Opportunity max, min, actual:", profit_1, previousprofit, profit_0, profit_0 - profit_1)
            b.updateOpportunityCost(profit_1 - profit_0)

















