import util
# from partition_new import mainPartition
import copy
# import numpy as np
import sys
import time
import pickle
import profile
import Queue

from collections import defaultdict

class MDS:
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



def bfs(overlapG_V, overlapG_Adj):
	covered_v = set()
	connectedGroups = []
	flag=False

	for v in overlapG_V:
		if v in covered_v:
			continue
		q = Queue.Queue()
		q.put(v)
		curGroup = [v]
		while(not q.empty()):
			curV = q.get()
			if curV not in overlapG_Adj:
				continue
			for nb in overlapG_Adj[curV]:
				if nb not in covered_v:
					covered_v.add(nb)
					curGroup.append(nb)
					q.put(nb)
					flag = True
			if flag:
				covered_v.add(curV)
		connectedGroups.append(curGroup)
	
	return connectedGroups

def doMerge(aggregated_max_dense, fname, mergeScore):
	aggregated_max_dense_merged = set()
	MdsList = list(aggregated_max_dense)
	overlapScore = {}
	overlapG_V = range(0,len(MdsList))
	overlapG_Adj = {}
	for i in range(0,len(MdsList)-1):
		for j in range(i+1,len(MdsList)):
			a = MdsList[i]
			b = MdsList[j]
			newSet = a&b
			# print "newSet", newSet
			curScore = float(len(newSet)**2)/(len(a)*len(b))
			overlapScore[frozenset((a, b))] = curScore
			if curScore >= mergeScore:			
				# print i,j,"score",curScore
				if i not in overlapG_Adj:
					overlapG_Adj[i] = []

				overlapG_Adj[i].append(j)

				if j not in overlapG_Adj:
					overlapG_Adj[j] = []
					
				overlapG_Adj[j].append(i)
			# print i,j
	# print len(overlapScore), len(overlapG_Adj)
	# print overlapG_Adj.keys()
	connectedGroups = bfs(overlapG_V, overlapG_Adj)
	print "connectedGroups"
	for elem in connectedGroups:
		# print "New....."
		if len(elem)>1:
			# print "Old"
			newMds = frozenset()
			for i in elem:
				newMds |= MdsList[i]
				# print MdsList[i],
			aggregated_max_dense_merged.add(newMds)
			# print
			# print "New", newMds
		else:
			# print "Old", MdsList[elem[0]]
			aggregated_max_dense_merged.add(MdsList[elem[0]])

	# for i in overlapScore:
		# print i,overlapScore[i]
	fout= open("./new_merge_result/" + fname + '_' + str(mergeScore) + '-nw.txt', 'w+')
	for mds in aggregated_max_dense_merged:
		for elem in mds:
			fout.write(elem + '\t')
		fout.write('\n')
	return aggregated_max_dense_merged

def extend(V, E, AdjList, D, MdsList, theta2):
	newMdsList = []
	global theta
	fout = open("extend_result/"+input_file.split("/")[-1].split(".")[0] + "-d" + str(theta)+ "extend" + str(theta2)+ "-skip-nw.txt",'w+')
	cnt = 0
	for mds in MdsList:  # each mds contains frozen set of vs
		cnt +=1
		mdsObj = MDS(set(mds), AdjList) 
		# print mds
		# print "In ", cnt, "mds"
		st = time.time()
		q = Queue.Queue()

		for node in mdsObj.vs:
			q.put(node)
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
					if mdsObj.computeDenseNew(nb, AdjList) >= theta2:
						# print "Adding", nb
						mdsObj.add(nb, AdjList)
		# print cnt, "Len of mds", oldLen, "=>", len(mdsObj.vs)
		# print "Time in this mds extending", time.time() - st
		newMdsList.append(mdsObj)
		# break

	coverSet = set()
	num_mds = 0
	for mdsObj in newMdsList:
		if len(mdsObj.vs) < 3:
			# print "Too small",mdsObj.vs
			continue
		num_mds+=1
		for v in mdsObj.vs:
			coverSet.add(v)				
			fout.write(v + '\t')
		fout.write('\n')
	print "====================="
	print "theta2", theta2
	print "Extend Coverage:",len(coverSet)
	print "Extend # Mds", num_mds

def load(fname):
	r = []
	fin = open(fname)
	for l in fin:
		r.append(frozenset(l.split()))
	return r

# path = './firstBranch-nonsieve-result/'
path = './result/'

# fLst = ['gavin2006_socioaffinities_rescaled-d0.3', 
# 'collins2007-d0.6',
# 'krogan2006_core-d0.6',
# 'krogan2006_extended-d0.5'
# ]
fLst = ['gavin2006_socioaffinities_rescaled-d0.3']
mergeScore = 0.9
for fname in fLst:
	(V, E, AdjList, D) = util.readinputNumpy('../../data/datasets_uw', mytype = "str", myDelimiter = "\t")

	aggregated_max_dense = load(path + fname +'.txt')
	# break
	aggregated_max_dense_merged = doMerge(aggregated_max_dense, fname, mergeScore)
	print len(aggregated_max_dense), len(aggregated_max_dense_merged)

	# break



