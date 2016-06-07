
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
		# print "start sorting"
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
	avgWeight = 0.0
	# AdjList [vertice] = set of (v, weight)
	for row in input_file:
		# print row
		if len(row) == 3:
			weight = float(row[2])
		else:
			weight = 1.0

		# if frozenset([row[0], row[1]]) in E and E[frozenset([row[0], row[1]])]!= weight:
			# print "Dup", E[frozenset([row[0], row[1]])], "New", weight
		


		E[frozenset([row[0], row[1]])] = weight
		V.add(row[0])
		edge_weight = (row[1], weight)
		AdjList[row[0]].add(edge_weight)
		
		V.add(row[1])
		edge_weight = (row[0], weight)
		AdjList[row[1]].add(edge_weight)


	D = {}
	for v in AdjList.keys():
		sum_deg = 0.0
		for edge_weight in AdjList[v]:
			sum_deg+=edge_weight[1]
		D[v] = sum_deg
		# break

	V = list(V)

	# print "D is", D
	# print "start sorting"
	st = time.time()
	V.sort(key = lambda k: (D[k], k), reverse=True)
	# print "end sorting", time.time() - st
	# print "Vertex in degree and alpha order", V 
	# V.sort(reverse=True)
	# print "Vertex in decreasing alpha order only", V
	# print(AdjList)
	# print(E)
	# return (V, E, AdjList)
	for e in E:
		avgWeight+=E[e]
	# print "V input length ", len(V)
	# print "E input length ", len(E)
	# print "avgWeight:",avgWeight/len(E)
	return V, E, AdjList, D

def readinputNumpyNonweight(fileN, mytype, myDelimiter):
	input_file = np.genfromtxt(fileN, dtype = str(mytype), skiprows = 0, delimiter = myDelimiter)
	# with open(fileN) as input_file:
		# print input_file
	V = set()
	E = {}
	AdjList = defaultdict(lambda: set())
	avgWeight = 0.0
	# AdjList [vertice] = set of (v, weight)
	for row in input_file:
		# print row
		weight = 1.0

		# if frozenset([row[0], row[1]]) in E and E[frozenset([row[0], row[1]])]!= weight:
			# print "Dup", E[frozenset([row[0], row[1]])], "New", weight
		

		E[frozenset([row[0], row[1]])] = weight
		V.add(row[0])
		edge_weight = (row[1], weight)
		AdjList[row[0]].add(edge_weight)
		
		V.add(row[1])
		edge_weight = (row[0], weight)
		AdjList[row[1]].add(edge_weight)


	D = {}
	for v in AdjList.keys():
		sum_deg = 0.0
		for edge_weight in AdjList[v]:
			sum_deg+=edge_weight[1]
		D[v] = sum_deg
		# break

	V = list(V)

	# print "D is", D
	# print "start sorting"
	st = time.time()
	V.sort(key = lambda k: (D[k], k), reverse=True)
	# print "end sorting", time.time() - st
	# print "Vertex in degree and alpha order", V 
	# V.sort(reverse=True)
	# print "Vertex in decreasing alpha order only", V
	# print(AdjList)
	# print(E)
	# return (V, E, AdjList)
	for e in E:
		avgWeight+=E[e]
	# print "V input length ", len(V)
	# print "E input length ", len(E)
	# print "avgWeight:",avgWeight/len(E)
	return V, E, AdjList, D	

def readinputNumpyHighOrder(fileN, mytype, myDelimiter):
	input_file = np.genfromtxt(fileN, dtype = str(mytype), skiprows = 0, delimiter = myDelimiter)
	# with open(fileN) as input_file:
		# print input_file
	V = set()
	E = {}
	AdjList = defaultdict(lambda: set())
	# AdjList [vertice] = set of (v, weight)
	for row in input_file:
		weight = float(row[-1])
		# print weight
		v1 = row[0] + ',' + row[1]
		v2 = row[2] + ',' + row[3]
		E[frozenset([v1,v2])] = weight
		V.add(v1)
		edge_weight = (v2, weight)
		AdjList[v1].add(edge_weight)
		
		V.add(v2)
		edge_weight = (v1, weight)
		AdjList[v2].add(edge_weight)

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
	# print "n is ", n
	if(n <= 1):  # Problem!!!!!!!!!!!!!! Compute 1 node density
		return -1
	else:
		density = 2.0*weight/((n-1)*n)
		return density

def computeDensityNew(V_curSet, AdjList, ):

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


def f_cover(SS):
	# print "SS", SS
	if len(SS) == 0:
		return 0
	covered_v = set()
	for S in SS:
		covered_v |= S

	return len(covered_v)

def N(S, V, E): # N(x)={y in V(G)| (x,y) in E(G)}, N(S)=U x in S N(x);
	# print "S,V",S,V
	N_S = set()
	for u in S:
		for v in set(V):
			if(frozenset([u, v]) in E): # neighbors
				N_S.add(v)
	return N_S

def comp_Potential(K, V_remain, E, theta, x, N_r, Union, AdjList):
	N_x = set()
	for edge_weight in AdjList[x]:
		if(edge_weight[0] in Union): # neighbors
			N_x.add(edge_weight[0])
	# print len(N_x), len(N_x_new)

	# print "New",time.time()
	N_r_x = N_x & N_r

	######### possible opt??? Need to go over all vs ###########
	# N_x2 = set()
	# for v in set(N_r):
	# 	if(frozenset([x, v]) in E): # neighbors
	# 		N_x2.add(v)
	# print "N_r_x", N_r_x, "N_x2", N_x2
	deg_x_S = len(N_x & K)

	
	# print "N_r_S",N_r, "N_x",N_x, N_r_x
	potential = len(N_r_x) + len(N_r)*(deg_x_S - theta*(len(K) +1.0 ))
	return potential


def sort_N_r(K, V_remain, E, theta, N_r, AdjList, D):
	potential_D = {}
	# global D
	start_time = time.time()
	Union = K | V_remain
	for x in N_r:
		# potential_D[x] = 1.0
		potential_D[x] = comp_Potential(K, V_remain, E, theta, x, N_r, Union, AdjList)
		# print "potential:",x,potential_D[x]
		# print "g_degree:",x,D[x]
	# print "Done potential", time.time() - start_time
	return sorted(N_r, key = lambda k: (potential_D[k], D[k]), reverse = True)


def compute_N_r_New(K, V_remain, E, theta, AdjList): # find all gamma neighbors on set S from V_remain
	# return set(V_remain)
	N_r = set()
	# print N_r

	# if (len(K) == 1):
	# 	u = K.pop()
	# 	for v in V_remain:
	# 		if(frozenset([u, v]) in E and E[frozenset([u, v])] >= theta):
	# 			N_r.add(v)

	# 	return N_r

	if (len(K) == 1):
		# u = K.pop()
		u = next(iter(K))

		for edge_weight in AdjList[u]:
			if edge_weight[1] >= theta:
				N_r.add(edge_weight[0])
		return N_r


	# base_density = computeDensity(K, E, isWeight)
	base_density = computeDensityNew(set(K), AdjList)
	n = len(K)
	edge_weight = base_density*(n-1)*n/2.0

	for v in V_remain:
		new_edge_weight = edge_weight
		for u in K:
			if(frozenset([u, v]) in E): # neighbors
				new_edge_weight+= E[frozenset([u, v])]
				# new_edge_weight+= 1

		new_density = new_edge_weight*2/((n+1)*n)
		if new_density >= theta:
			N_r.add(v)	

	return N_r	

def grasp_sort(K, V_remain, E, theta, AdjList, D): #''' bottleneck! '''

	# t0 = time.time()
	N_r = compute_N_r_New(K, V_remain, E, theta, AdjList)

	# print "time of gamma neighbors new", time.time() - t0, len(N_r)

	
	# t0 = time.time()

	# print "N_R here!!!!!!", len(N_r)
	# if len(N_r) > 0:
	# 	N_r_sorted = sort_N_r(K, V_remain, E, theta, N_r, AdjList) #''' bottleneck! '''
	# # print "time of N_r sort", time.time() - t0
	# 	return N_r_sorted
	# else:
	# 	return set()
	N_r_sorted = sort_N_r(K, V_remain, E, theta, N_r, AdjList, D) #''' bottleneck! '''
	return N_r_sorted

