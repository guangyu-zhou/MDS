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

def load(fname):
	r = []
	fin = open(fname)
	for l in fin:
		r.append(frozenset(l.split()))
	return r

# path = './firstBranch-nonsieve-result/'
path = './result-unweight/'

# fLst = ['gavin2006_socioaffinities_rescaled-d0.3', 
# 'collins2007-d0.6',
# 'krogan2006_core-d0.6',
# 'krogan2006_extended-d0.5'
# ]
fLst = ['gavin2006_socioaffinities_rescaled-d0.3']
mergeScore = 0.9
for fname in fLst:
	aggregated_max_dense = load(path + fname +'.txt')
	# break
	aggregated_max_dense_merged = doMerge(aggregated_max_dense, fname, mergeScore)
	print len(aggregated_max_dense), len(aggregated_max_dense_merged)

	# break



