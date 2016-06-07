import util
import Queue
import copy
import time
import random
from collections import defaultdict
class MdsClass:
	def __init__(self, V_curSet, AdjList):
		self.vs = V_curSet
		weight = 0.0
		for v in V_curSet:
			for edge_weight in AdjList[v]:
				if(edge_weight[0] in V_curSet):
					weight+=edge_weight[1]
		
		self.inDeg = weight

	def add(self, nb, AdjList):

		weight = self.inDeg
		for edge_weight in AdjList[nb]:
				if(edge_weight[0] in self.vs):
					weight+=2*edge_weight[1]

		self.vs.add(nb)
		self.inDeg = weight

	def computeDenseNew(self, nb, AdjList):
		weight = self.inDeg
		for edge_weight in AdjList[nb]:
				if(edge_weight[0] in self.vs):
					weight+=2*edge_weight[1]

		n = len(self.vs) + 1
		return weight/((n-1)*n)


def extend_merge(V, E, AdjList, D, MdsList, overlapScore):
	'''
	for each mds in list of original MDS:
	check if it has overlap with any extended_MDS > threshold
	if yes, ignore
	if no, proceed to extend this one and put it inside extended_MDS
	'''
	newMdsHashSet = set()
	newMdsList = []
	global theta
	# fout = open("./result/extendOptMerge0.5Overlap.txt",'w+')
	fout = open("result_extMerge/"+input_file.split("/")[-1].split(".")[0] + "-d" + str(theta)+ "extendMERGE-o"+ str(overlapScore)+".txt",'w+')
	print "density", theta
	print "In extend. Total Mds", len(MdsList)
	print "overlapScore",overlapScore
	cnt = 0
	for mds in MdsList:  # each mds contains frozen set of vs
		cnt +=1
		# print "In ", cnt, "mds"
		passflag = False
		for extendedMds in newMdsHashSet:
			overlap = frozenset(mds) & extendedMds
			# if len(overlap) > 0:
			# 	print overlap
			if len(overlap)/(1.0*len(mds)) > overlapScore:
			# if extendedMds.issuperset(frozenset(mds)):
				# print "Pass mds"
				passflag = True
				break
		if passflag:
			continue
		mdsObj = MdsClass(set(mds), AdjList) 
		# print mds
		st = time.time()
		q = Queue.Queue()

		for node in mdsObj.vs:
			q.put(node)
		# print "before len of mds", len(mdsObj.vs)
		oldLen = len(mdsObj.vs)
		while(not q.empty()):
			# print q.qsize()
			curV = q.get()
			for nb in AdjList[curV]:
				nb = nb[0]
				if nb not in mdsObj.vs:
					# newMds = copy.copy(mds)
					# newMds.add(nb)
					# print "mds:",mds
					n = len(mdsObj.vs)
					# print "Old density", len(mdsObj.vs), mdsObj.inDeg/((n-1)*n)
					# print "New density", mdsObj.computeDenseNew(nb, AdjList)
					# print 
					if mdsObj.computeDenseNew(nb, AdjList) >= theta:
						# print "Adding", nb
						mdsObj.add(nb, AdjList)
		# print cnt, "Len of mds", oldLen, "=>", len(mdsObj.vs)
		# print "Time in this mds extending", time.time() - st

		newMdsHashSet.add(frozenset(mdsObj.vs))
		newMdsList.append(mdsObj)
		# break

	coverSet = set()
	print "newMdsList size ( >=1 included)",len(newMdsList)
	for mdsObj in newMdsList:
		if len(mdsObj.vs) < 3:
			# print "Too small",mdsObj.vs
			continue
		for v in mdsObj.vs:
			coverSet.add(v)				
			fout.write(v + '\t')
		fout.write('\n')
	print "Extend Cover:",len(coverSet)
	# check_overlap(newMdsList)
	# for elem in newMdsHashSet:
	# 	print elem


def bfs_grasp_new(K, V, E, AdjList, D):
	
	# Q.add(nbs_sorted)
	nbs = util.N(K, V, E) - K
	# print "Start bfs_grasp_new"
	# print K,"nbs", nbs
	nonLeaf= True
	# CoveredVLocal = set()


	while(len(nbs) > 0 and nonLeaf):
		nonLeaf=False


		# for nb in nbs:
		# 	print nb, E[frozenset((nb, curV))]
		# nbs_sorted = util.grasp_sort(nbs, set(V) - set(nbs), E, theta, AdjList)
		# print len(K)
		nbs_sorted = util.grasp_sort(K, nbs, E, theta, AdjList, D)
		# print "nbs_sorted", nbs_sorted
		# nbs_sorted2 = grasp_sort(K, set(V) - set(K) , E, theta, AdjList)


		# print nbs_sorted2
		# for nb in nbs_sorted:
		# 	print nb, E[frozenset((nb, curV))]
		for elem in nbs_sorted:
			# if elem not in CoveredVLocal:
				# print K
				# K.add(elem)
				# print K
				# print "D",util.computeDensityNew(K , AdjList), 
				K.add(elem)
				# print "D new", util.computeDensityNew(K , AdjList)
				if util.computeDensityNew(K , AdjList) > theta:
					# print "adding", elem ,"density", util.computeDensityNew(K , AdjList)

					nonLeaf = True
					# print "K new",K
					# CoveredVCur.add(elem[0])
					# CoveredVLocal.add(elem)
					CoveredV.add(elem)
				else:
					K.remove(elem)
					# print "removing", elem
					# print "******************************"
					break
		# if flag:
			# CoveredVCur.add(curV)
			# CoveredV.add(curV)
		# print "Q size", q.qsize(), "CoveredV", len(CoveredV)
		# break
		nbs = util.N(K, V, E) - K
		# print K,"nbs new", nbs
		# print
	# print time.time() - start

	return K

theta = 0.8
overlapScore = 1.0
# load G: (V,E, AdjList, D)
input_file_list = [
# "../../data/data_tweet/input_whole_enum.txt"
# "../../data/datasets/gavin2006_socioaffinities_rescaled.txt",
# "../../data/datasets/collins2007.txt",
# "../../data/datasets/krogan2006_core.txt",
"../../data/datasets/krogan2006_extended.txt",
# "../../data/datasets/biogrid_yeast_physical_unweighted.txt"
]
for input_file in input_file_list:
	st = time.time()
	print input_file
	# input_file = input_file_list[1]
	(V, E, AdjList, D) = util.readinputNumpy(input_file, mytype = "str", myDelimiter = "\t")
	print len(V), len(E)
	# sort(V)
	# q = Queue.Queue()
	CoveredV = set()
	MDS = []
	cnt = 0
	for v in V:
		cnt+=1
		# check covered or not
		# print "v",v
		if v in CoveredV:
			continue
		K = set()
		K.add(v)
		# print "*****K****", cnt
		CoveredV.add(v)

		K_new = bfs_grasp_new(K, V, E, AdjList, D)
		if len(K_new) >0:
			MDS.append(K_new)

		# break
	print len(MDS)

	fname = input_file.split('/')[-1].split('.')[0]
	# print fname
	fout= open("./result/" + fname + '_' + str(theta) + '-w.txt', 'w+')
	for mds in MDS:
		if len(mds) < 3:
			continue
		for elem in mds:
			fout.write(elem + '\t')
		fout.write('\n')

	print "time:", time.time()- st

	extend_merge(V, E, AdjList, D, MDS, overlapScore)

	print "time:", time.time()- st
