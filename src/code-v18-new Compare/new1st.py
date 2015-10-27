# from pseudeo_clique_caller.py import enumPseudoClique_1st_level
import util
import copy
# import numpy as np
import sys
import time
import pickle
import profile
import Queue

from collections import defaultdict


def N(S, E, V): # N(x)={y in V(G)| (x,y) in E(G)}, N(S)=U x in S N(x);
	# print "S,V",S,V
	N_S = set()
	for u in S:
		for v in set(V):
			# print u,v
			if(frozenset([u, v]) in E): # neighbors
				N_S.add(v)
	# print "N:",len(N_S)
	return N_S

def comp_Potential(K, V_remain, E, theta, x, N_r, Union, AdjList):
	N_x = set()
	for edge_weight in AdjList[x]:
		if(edge_weight[0] in Union): # neighbors
			N_x.add(edge_weight[0])
	N_r_x = N_x & N_r

	deg_x_S = len(N_x & K)

	
	# print "N_r_S",N_r, "N_x",N_x, N_r_x
	potential = len(N_r_x) + len(N_r)*(deg_x_S - theta*(len(K) +1.0 ))
	return potential


def sort_N_r(K, V_remain, E, theta, N_r, AdjList):
	potential_D = {}
	global D
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
	

	if (len(K) == 1):
		u = K.pop()
		for edge_weight in AdjList[u]:
			if edge_weight[1] >= theta:
				N_r.add(edge_weight[0])
		return N_r


	# base_density = util.computeDensity(K, E, isWeight)
	base_density = util.computeDensityNew(set(K), AdjList)
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

def grasp_sort(K, V_remain, E, theta, AdjList): #''' bottleneck! '''

	# t0 = time.time()
	N_r = compute_N_r_New(K, V_remain, E, theta, AdjList)

	N_r_sorted = sort_N_r(K, V_remain, E, theta, N_r, AdjList) #''' bottleneck! '''
	# print N_r_sorted
	return N_r_sorted


def enumPseudoClique(K, V_remain, E, V, AdjList, theta, max_dense, dense, Ancestors, CoveredV):
	''' --------------@para: no of elem in K-------------- '''
	global max_gain
	global first_branch
	leaf_node = 1
	
	for elem in K:
		print str(elem) + "\t",
	print float(dense)
	# print
	# if len(K) > min_elem_output:
	# print dense,
	# print "\t" + str(K)
	# print "first_branch", first_branch
	# print "V_remain:", len(V_remain)
	if 0 == len(V_remain):
		# print "===========reach base case ==========="
		# print float(dense), K

		first_branch = False
		K_set = set(K)
		CoveredV |= K_set
		# all_first_branch.append(K_set)

		should_add = True
		for each_set in max_dense:
			if set(each_set[0]).issuperset(set(K)):
				# print "Here"
				should_add = False
				break
		if should_add:
			# print "leaf node", K, "dense", dense 
			max_dense.append((K, dense))
		 	return


	if len(K) != 0: # 1st level
		# print "grasp_sort start"
		# time_start = time.time()
		V_remain_in_seq = grasp_sort(set(K), set(V_remain), E, theta, AdjList)
		# print "grasp_sort end", time.time() - time_start
	
	# print "V_remain_in_seq", len(V_remain_in_seq)
	if len(K) == 1 and len(V_remain_in_seq) == 0:
		# print "returned"
		return
	
	for i in range(len(V_remain_in_seq)):
		# print "i", i
		v = V_remain_in_seq[i]

		K_new = copy.copy(K)
		
		# check connectivity, if v is not connect to K_new, pick another v
		v_deg = 0
		for u in K_new:
			# if v in AdjList[u]:
			if frozenset((u,v)) in E:
				# break
				v_deg+=1
		if K_new != [] and v_deg == 0:
			# print "pick another v"
			continue # pick another v
		# end	

		# D = util.computeDegree(list(K_new), E)
		# print "D",D,"K_new",K_new
		# min_deg = util.min_degree(D)

		K_new.append(v)

 		# print "K_new",K_new
 		start_time = time.time()
		# new_dense = util.computeDensity(set(K_new), E, isWeight)
		# print "dense compute time", time.time() - start_time, new_dense

		# start_time = time.time()
		new_dense = util.computeDensityNew(set(K_new), AdjList)
		# print "new d", new_dense
		# print "new dense compute time", time.time() - start_time, new_dense

		if new_dense >= theta:
			# print "Old Ancestors:", Ancestors
			
			if(not first_branch):
				# print "tracing back... "
				# continue
				return
			# print "v is", v
 			# print "Ancestors:", Ancestors_new
	 		if v in Ancestors:
	 			# print "In Ancestors.......", v
 				continue

 			# remove those in ancestors
			V_new = list(N(set(K_new), E, V)  - set(K_new) - Ancestors)

			# V_new = list(N(set(K_new), E, V)  - set(K_new))

			Ancestors_new =  Ancestors | set(V_remain_in_seq[:i])

			# if (first_branch or sieve_nonleaf(set(K_new), K_new)):
			# if(first_branch):
			# if(True):

			leaf_node = 0
			# print "Next level"
			enumPseudoClique(K_new, V_new, E, V, AdjList, theta, max_dense, new_dense, Ancestors_new, CoveredV)

		# else:
		# 		print "stop enumerate due to dense"


	print "leaf_node", leaf_node, set(K)
	if leaf_node:
		# print "leaf_node"
		# print float(dense), K

		K_set = set(K)
		CoveredV |= K_set
		# all_first_branch.append(K_set)
		should_add = True
		for each_set in max_dense:
			if set(each_set[0]).issuperset(set(K)):
				# print "Here"
				should_add = False
				break
		if should_add:
			# print "leaf node", K, "dense", dense 
			max_dense.append((K, dense))
		# print "In leaf_node"
	
		first_branch = False			
	print "Reset Ancestors......"
	Ancestors = set()
	# print "S len:"
	# for i in range(k, k*m + 1, 1):
	# 	print len(S[i]),
	# print
	



# main
def main(input_file):
	
	global D
	start_time = time.time()
	(V, E, AdjList, D) = util.readinputNumpy(input_file, mytype = "str", myDelimiter = "\t")
	# print "time in reading", time.time() - start_time
	max_dense = []

	CoveredV = set()
	Ancestors = set()
	# print "start looping... "
	for i in range(len(V)):
		# print "V[i]",V[i]
		print "========= progress =========: ", i, len(V), V[i]

		curV = V[i]

		# if (curV in CoveredV):
			# print "***********Skip seed ***********: ", i
			# continue
		K = set([curV])
		# print "K1", K
		V_remain = N(K, E, V)
		while(True):
			# print V_remain

			K_copy = copy.copy(K)
			V_remain_in_seq = grasp_sort(K_copy, set(V_remain), E, theta, AdjList)

			if len(V_remain_in_seq) == 0:
				# print "V_remain_in_seq = 0!"
				break
			else:
				# print "V_remain_in_seq[0]",V_remain_in_seq[0]
				K.add(V_remain_in_seq[0])
				# print 'd', util.computeDensityNew(K, AdjList)
				if util.computeDensityNew(K, AdjList) < theta:
					break
				else:
					V_remain = N(K, E, V) - K
		print "K2", len(K)
		should_add = True
		for each_set in max_dense:
			if each_set.issuperset(K) :
				print "Here"
				should_add = False
				break
		if should_add and len(K) > 2:
			# print "leaf node", K, "dense", dense 
			print "adding", K
			max_dense.append(K)

	foutName = input_file.split("/")[-1].split(".")[0]

	fout = open('./NonEnum/'+foutName + '-d' + str(theta) + '.txt', 'w+')
	print "# MDS", len(max_dense)
	for mds in max_dense:
		for v in mds:
			fout.write(v + '\t')
		fout.write('\n')
	
		



theta = 0.0

D = {}
# covers = set()
first_branch = True
all_first_branch = []


# profile.run('main(input_file)')

input_file_list = [
"../../data/datasets/gavin2006_socioaffinities_rescaled.txt",
# "../../data/datasets/gavin2006_socioaffinities_rescaled.txt",

"../../data/datasets/collins2007.txt",
"../../data/datasets/krogan2006_core.txt",
"../../data/datasets/krogan2006_extended.txt",
"../../data/data_tweet/input_whole_enum.txt",
"../../data/demo.txt"

]


input_file = input_file_list[1]

# for theta in [0.5, 0.6, 0.7, 0.8, 0.9, 0.4, 0.3]:
for theta in [0.6]:

# for i in [3]:

# input_file = input_file_list[i]
# theta = 0.6
# for theta in [0.6, 0.5, 0.4, 0.3]:
# for input_file in input_file_list:
	start_time = time.time()
	
	# print fout
	print "Reading from:", input_file
	print "theta",theta

	main(input_file)
	print("%s seconds" % round((time.time() - start_time), 2))








