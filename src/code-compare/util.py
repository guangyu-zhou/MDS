import copy
from itertools import chain, combinations
import numpy as np
import sys
import time
from collections import defaultdict



def computeDegree(V_list, E):
	# use list for degree to be ordered
	D = []
	# print V_list
	for u in V_list:
		deg = 0
		for v in V_list:
			if(frozenset([u, v]) in E):
				deg += E[frozenset([u, v])]
		D.append((u, deg))
	# print "V_list", V_list, "D ", D
	return D

def computeDegree_dict(V_list, E):
	# use list for degree to be ordered
	D = {}
	# print V_list
	for u in V_list:
		deg = 0
		for v in V_list:
			if(frozenset([u, v]) in E):
				deg += E[frozenset([u, v])]
		D[u] = deg
	# print "V_list", V_list, "D ", D
	return D

def readinput(fileN, mytype, myDelimiter, isWeight = True):
	# input_file = np.genfromtxt(fileN, dtype = str(mytype), skiprows = 0)
	with open(fileN) as input_file:
		# print input_file
		V = set()
		E = {}
		AdjList = defaultdict(lambda: set())
		# AdjList [vertice] = set of (v, weight)
		for row in input_file:
			row = row.strip("\n").split(myDelimiter)
			# if len(row.split(" "))
			# print "row", row

			# E[frozenset([row[0], row[1]])] = round(float(row[2]),3)
			if isWeight:
				weight = float(row[2])
			else:
				weight = 1.0
			E[frozenset([row[0], row[1]])] = weight
			V.add(row[0])
			edge_weight = (row[1], weight)
			AdjList[row[0]].add(edge_weight)
			
			V.add(row[1])
			edge_weight = (row[0], weight)
			AdjList[row[1]].add(edge_weight)

		# print len(AdjList['Best Buy Theater']), len(AdjList['China'])
		# '''
		D = {}
		for v in AdjList.keys():
			sum_deg = 0.0
			for edge_weight in AdjList[v]:
				sum_deg+=edge_weight[1]
			D[v] = sum_deg
			# break

		V = list(V)

		# print "D is", D
		print "start sorting"
		V.sort(key = lambda k: (D[k], k), reverse=True)
		# print "Vertex in degree and alpha order", V 
		# V.sort(reverse=True)
		# print "Vertex in decreasing alpha order only", V
		# print(AdjList)
		# print(E)
	# return (V, E, AdjList)
	return V, E, AdjList, D


def readinputNumpy(fileN, mytype, myDelimiter):
	input_file = np.genfromtxt(fileN, dtype = str(mytype), skiprows = 0, delimiter = myDelimiter)
	# with open(fileN) as input_file:
		# print input_file
	V = set()
	E = {}
	AdjList = defaultdict(lambda: set())
	# AdjList [vertice] = set of (v, weight)
	for row in input_file:
		if len(row) == 3:
			weight = float(row[2])
		else:
			weight = 1.0
		E[frozenset([row[0], row[1]])] = weight
		V.add(row[0])
		edge_weight = (row[1], weight)
		AdjList[row[0]].add(edge_weight)
		
		V.add(row[1])
		edge_weight = (row[0], weight)
		AdjList[row[1]].add(edge_weight)

		# print len(AdjList['Best Buy Theater']), len(AdjList['China'])
		# '''
	D = {}
	for v in AdjList.keys():
		sum_deg = 0.0
		for edge_weight in AdjList[v]:
			sum_deg+=edge_weight[1]
		D[v] = sum_deg
		# break

	V = list(V)

	# print "D is", D
	print "start sorting"
	V.sort(key = lambda k: (D[k], k), reverse=True)
	# print "Vertex in degree and alpha order", V 
	# V.sort(reverse=True)
	# print "Vertex in decreasing alpha order only", V
	# print(AdjList)
	# print(E)
	# return (V, E, AdjList)
	return V, E, AdjList, D

def powerset_generator_2(i):
    for subset in chain.from_iterable(combinations(i, r) for r in range(2,1,-1)):
        yield frozenset(subset)

def computeDensity(V_curSet, E, isWeight = True):
	all_pairs = []
	for i in powerset_generator_2(V_curSet):
		# print(i)
		all_pairs.append(i)

	weight = 0;
	if isWeight:
		for each_pair in all_pairs:
			if(each_pair in E):
				weight+= E[each_pair]
	else:
		for each_pair in all_pairs:
			if(each_pair in E):
				weight+= 1.0
	n = len(V_curSet)
	if(n <= 1):  # Problem!!!!!!!!!!!!!! Compute 1 node density
		return 1
	else:
		density = 2.0*weight/((n-1)*n)
		return density

def computeDensityNew(V_curSet, AdjList):

	weight = 0
	for v in V_curSet:
		for edge_weight in AdjList[v]:
			if(edge_weight[0] in V_curSet):
				weight+=edge_weight[1]

	n = len(V_curSet)
	if(n <= 1):  # Problem!!!!!!!!!!!!!! Compute 1 node density
		return 1
	else:
		density = weight/((n-1)*n)
		return density

''' 
return a list of pairs (vertex, degree) that are connected.
Can be better optimized
'''
# def computeDegree(V_set, AdjList, E):
# 	# use list for degree to be ordered
# 	D = []
# 	for v in AdjList:
# 		deg = 0
# 		if v not in V_set:
# 			continue
# 		for neighbor in AdjList[v]:
# 			if neighbor in V_set:
# 				deg +=1
# 		D.append((v, deg))
# 	# print "Vset", V_set, "D ", D
# 	return D



def v_star(D):
	sorted_D = sorted(D, key = lambda d: (d[1], d[0]))
	# print "sorted_D", sorted_D
	# minIndex = D.values().index(min(sorted(D.values())))
	# print "v_star is", sorted_D[0][0]
	return sorted_D[0][0]

def min_degree(D):
	if len(D) == 0:
		return 0
	
	sorted_D = sorted(D, key = lambda d: d[1])
	# print "sorted_D", sorted_D
	# minIndex = D.values().index(min(sorted(D.values())))
	# print "v_star is", sorted_D[0][0]
	return sorted_D[0][1]




