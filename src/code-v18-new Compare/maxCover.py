# from pseudeo_clique_caller.py import enumPseudoClique_1st_level
import util
import copy
# import numpy as np
import sys
import time
import pickle
import profile
from collections import defaultdict

# def f_cover(SS):
# 	# print "SS", SS
# 	if len(SS) == 0:
# 		return 0
# 	covered_v = set()
# 	for S in SS:
# 		covered_v |= S

# 	return len(covered_v)

def MaxCover(V, S, k):
	D = []
	S1 = S
	V1 = set(V)
	for i in range(k):
		C = S1[0]
		for C_elem in S1:
			# print C_elem
			if(len(C_elem & V1) > len(C & V1)):
				C = C_elem
		# print C
		V1 = V1 - C
		S1.remove(C)
		# print S1
		D.append(C)
	# print D
	covers = set()
	for c in D:
		covers |= c
	print "coverage: " + str(len(covers))
	return D

def N(S, E, V): # N(x)={y in V(G)| (x,y) in E(G)}, N(S)=U x in S N(x);
	# print "S,V",S,V
	N_S = set()
	for u in S:
		for v in set(V):
			if(frozenset([u, v]) in E): # neighbors
				N_S.add(v)
	return N_S

def comp_Potential(K, V_remain, E, theta, x, N_r, Union, AdjList):
	# return 1.0
	# N_r_S = compute_N_r(S, theta)
	# print "x", x, "K",K
	# N_x = set()
	# for v in Union:
	# 	if(frozenset([x, v]) in E): # neighbors
	# 		N_x.add(v)

	# print "Old",time.time()

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
	# potential = len(N_r_x) + len(N_r)*(deg_x_S - theta*(len( K) +1.0 ))
	# return potential

	#  degx|Nr(S) + degx|S - r(|S|+ |Nr(S)\{x}| )
	newPotential = len(N_r_x) + deg_x_S - theta*(len(K) +1.0 )
	# print "New potential", "Nr", len(N_r)
	return newPotential

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
	# print N_r

	# if (len(K) == 1):
	# 	u = K.pop()
	# 	for v in V_remain:
	# 		if(frozenset([u, v]) in E and E[frozenset([u, v])] >= theta):
	# 			N_r.add(v)

	# 	return N_r

	if (len(K) == 1):
		u = K.pop()
		for edge_weight in AdjList[u]:
			if edge_weight[1] >= theta:
				N_r.add(edge_weight[0])
		return N_r


	base_density = util.computeDensity(K, E, isWeight)
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

	t0 = time.time()
	N_r = compute_N_r_New(K, V_remain, E, theta, AdjList)

	# print "time of gamma neighbors new", time.time() - t0, len(N_r)

	
	t0 = time.time()

	# print "N_R here!!!!!!", len(N_r)
	N_r_sorted = sort_N_r(K, V_remain, E, theta, N_r, AdjList) #''' bottleneck! '''
	# print "time of N_r sort", time.time() - t0

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
	# print str(K) +"\t" + str(dense)
	# print "first_branch", first_branch
	# print "V_remain:", len(V_remain)
	if 0 == len(V_remain):
		# print "===========reach base case ==========="
		first_branch = False
		CoveredV |= set(K)
		if len(set(K)) > 2:
			should_add = True
			for each_set in max_dense:
				if set(each_set[0]).issuperset(set(K)):
					print "subset", set(K)
					should_add = False
					break
			if should_add:
				max_dense.append((K, dense))		
	 	return


	if len(K) != 0: # 1st level
		# print "grasp_sort start"
		time_start = time.time()
		V_remain_in_seq = grasp_sort(set(K), set(V_remain), E, theta, AdjList)
		# print "grasp_sort end", time.time() - time_start
	
	# print "V_remain_in_seq", len(V_remain_in_seq)
	if len(K) == 1 and len(V_remain_in_seq) == 0:
		# print "0 size return"
		return
	for i in range(len(V_remain_in_seq)):
		# print "i", i
		v = V_remain_in_seq[i]

		K_new = copy.copy(K)
		# V_new = V_remain_in_seq[i+1:]
		# Ancestors = set(K_new) | set(V_remain_in_seq[:i])
		# print K,"sibling here ",V_remain_in_seq[:i]
		# print "V_remain_in_seq",V_remain_in_seq, " i",i
		
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
		new_dense = util.computeDensity(set(K_new), E, isWeight = True)
		# print "dense compute time", time.time() - start_time, new_dense

		# start_time = time.time()
		# new_dense = util.computeDensityNew(set(K_new), AdjList)
		# print "new dense compute time", time.time() - start_time, new_dense

		if new_dense >= theta:
			# print "Old Ancestors:", Ancestors
			# if(not first_branch):
			# 	print "tracing back... "
			# 	# continue
			# 	return
			# print "v is", v
 			# print "Ancestors:", Ancestors_new
	 		if v in Ancestors:
	 			# print "In Ancestors......."
 				continue

 			# if (first_branch or sieve_nonleaf(set(K_new), K_new)):
				# print "not first_branch and not sieve_nonleaf"
				# continue

			V_new = list(N(set(K_new), E, V)  - set(K_new) - Ancestors)
			Ancestors_new =  Ancestors | set(V_remain_in_seq[:i])

			leaf_node = 0
			# print "Next level"
			enumPseudoClique(K_new, V_new, E, V, AdjList, theta, max_dense, new_dense, Ancestors_new, CoveredV)

		else:
				print "stop enumerate due to dense"


	# print "leaf_node", leaf_node, set(K)
	if leaf_node:
		# print "leaf len", len(set(K)), set(K)
		CoveredV |= set(K)
		if len(set(K)) > 2:
			should_add = True
			for each_set in max_dense:
				if set(each_set[0]).issuperset(set(K)):
					# print "Here"
					should_add = False
					break
			if should_add:
				max_dense.append((K, dense))
	
	first_branch = False			
	# print "Reset Ancestors......"
	Ancestors = set()


# main
def main():
	# input_file = "../data/input_enum.txt"
	# input_file = "../data_tweet/input_whole_enum.txt"
	# input_file = "../data_tweet/tweet_complete_processed.txt"
	# input_file = "../../data/data_bio/cl1_datasets/datasets/collins2007.txt"
	# input_file = "../../data/data_bio/cl1_datasets/datasets/krogan2006_core.txt"
	# input_file = "../../data/data_bio/cl1_datasets/datasets/krogan2006_extended.txt"
	input_file = "../../data/data_bio/cl1_datasets/datasets/gavin2006_socioaffinities_rescaled.txt"
	# input_file = "../data_tweet/corenlp_news/result10k.txt"

	# input_file = "../data_bio/cl1_datasets/datasets/biogrid_yeast_physical_unweighted.txt"

	# input_file = "../data_snap/dblp_.1.txt"
	global max_gain
	global D
	print "Reading from:", input_file
	start_time = time.time()
	# (V, E, AdjList, D) = util.readinput(input_file, mytype = "str", myDelimiter = " ", isWeight = True)
	(V, E, AdjList, D) = util.readinputNumpy(input_file, mytype = "str", myDelimiter = "\t")
	print len(D.keys())
	# pickle.dump( V, open( "save-V.p", "wb" ) )
	# pickle.dump( E, open( "save-E.p", "wb" ) )

	# V = pickle.load(open( "save-V.p", "rb" ))
	# E = pickle.load(open( "save-E.p", "rb" ))
	print "time in reading", time.time() - start_time

	
	max_dense = []

	# time.sleep(0.5)
	print "V input length ", len(V)
	print "E input length ", len(E)

	global first_branch
	# D = util.computeDegree_dict(list(V),E)
	# print "D computed"

	CoveredV = set()
	Ancestors = set()
	print "start looping... "
	for i in range(len(V)):
		# print "V[i]",V[i]
		curV = V[i]

		first_branch = True

		# if all_full:
			# continue

		# print "CoveredV", (curV in CoveredV), curV

		if (curV in CoveredV):
			# print "***********Skip seed ***********: ", i
			continue

		K = [V[i]]
		V_new = copy.copy(V)
		V_new.pop(i)
		print "========= progress =========: ", i, len(V)
		# print "Ancestors:", set(V[:i])
		max_gain  = 0
		# print "S keys",len(S.keys())
		enumPseudoClique(K, V_new, E, V, AdjList, theta, max_dense, 1.0, Ancestors, CoveredV)
		Ancestors.add(curV)


	print "========================="
	print "threshold", theta, "All Enum, naive maximal"
	print "========================="

	S = []
	print "max_dense len:", len(max_dense)
	for elem in max_dense:
		print "Adding...",set(elem[0])
		S.append(set(elem[0]))
	
	k = 105
	print "Max cover, k=" + str(k)
	covers = MaxCover(set(V), S, k)


	print "Density:"
	for each_set in max_dense:
		# print each_set[0], covers
		if(set(each_set[0]) in covers):
			# print str(each_set[0]) + '\t' + str(each_set[1])
			for elem in each_set[0]:
				print elem,
			print
	
	# coverage_set = set()
	# for each_set in max_dense:
	# 	# if(len(each_set[0]) > 2 and len(each_set[0]) <=10 ):
	# 	for elem in each_set[0]:
	# 		if elem not in coverage_set:
	# 			coverage_set.add(elem)
	# 		# print str(each_set[0]) + '\t' + str(each_set[1])
	# 		print elem,
	# 	print


# k = 0
theta = 0.0
if(len(sys.argv) != 5):
	print "Usage: **.py <inputfile> <k> <threshold> <min_elem_output>"
	# input_line  = raw_input("Exit? Y or N: ")
	# if(input_line in ['Y','y','Yes','YES','yes']):
	# 	sys.exit()

	
	# k = 50
	theta = 0.6
	print "Running default... theta=",theta


else:
	# input_file = sys.argv[1]
	k = int(sys.argv[2])
	theta = float(sys.argv[3])
	min_elem_output = int(sys.argv[4])

# m = 10

isWeight = True
# S = defaultdict(list)
D = {}
# covers = set()
all_full = False
first_branch = True
max_gain = 0
real_max_gain = 0
# all_enum = []

start_time = time.time()
# profile.run('main(input_file)')
main()
# print "v chosen: ", len(O)*1/100,len(O)
# print "all_full", all_full
print("--- %s seconds ---" % (time.time() - start_time))








