import copy
from itertools import chain, combinations
# import numpy as np
import sys
import time


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

def readinput(fileN, mytype, myDelimiter):
	# input_file = np.genfromtxt(file, dtype = str(mytype), skiprows = 0)
	input_file = open(fileN)
	# print input_file
	V = []
	E = {}
	AdjList = {}
	for row in input_file:
		row = row.strip("\n")
		# if len(row.split(" "))
		row = row.split(myDelimiter)
		# print "row", row
		E[frozenset([row[0], row[1]])] = round(float(row[2]),3)
		if(row[0] not in V):
			V.append(row[0])
			AdjList[row[0]] = [row[1]]
		else:
			AdjList[row[0]].append(row[1])
		if(row[1] not in V):
			V.append(row[1])
			AdjList[row[1]] = [row[0]]
		else:
			AdjList[row[1]].append(row[0])

	# '''
	D = computeDegree_dict(V, E)
	# print "D is", D
	V.sort(key = lambda k: (D[k], k), reverse=True)
	# print "Vertex in degree and alpha order", V 
	# V.sort(reverse=True)
	# print "Vertex in decreasing alpha order only", V
	# print(AdjList)
	# print(E)
	return (V, E, AdjList)

def powerset_generator_2(i):
    for subset in chain.from_iterable(combinations(i, r) for r in range(2,1,-1)):
        yield frozenset(subset)

def computeDensity(V_curSet, E):
	all_pairs = []
	for i in powerset_generator_2(V_curSet):
		# print(i)
		all_pairs.append(i)

	weight = 0;
	for each_pair in all_pairs:
		if(each_pair in E):
			weight+= E[each_pair]
	n = len(V_curSet)
	if(n <= 1):  # Problem!!!!!!!!!!!!!! Compute 1 node density
		return 1
	else:
		density = 2.0*weight/((n-1)*n)
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




