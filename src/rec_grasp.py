# from pseudeo_clique_caller.py import enumPseudoClique_1st_level
import util
import copy
import numpy as np
import sys
import time
import pickle
# from pseudo_clique_enum import enumPseudoClique, my_sort_V

# def my_sort_V(K, V_remain, E):
# 	D = {}
# 	for u in V_remain:
# 		deg = 0rec_grasp.py
# 		for v in K:
# 			if(frozenset([u, v]) in E):
# 				deg += E[frozenset([u, v])]
# 		D[u] = deg
# 	V_remain = list(V_remain)
# 	V_remain.sort(key = lambda d: (D[d], d), reverse=True)
# 	# print "V_remain",V_remain
# 	return V_remain
def f_cover(SS):
	# print "SS", SS
	if len(SS) == 0:
		return 0
	covered_v = set()
	for S in SS:
		covered_v |= S

	return len(covered_v)

def sieve(input_set):
	global all_full 
	all_full = True
	num_no_full = 0
	for v in O:
		# print "====v====", v
		S_temp = S[v] + [input_set]
		marg_gain = f_cover( S_temp) - f_cover(S[v])
		# print "marg_gain", marg_gain
		# print v,"len:", len(S[v])
		
		if len(S[v]) < k:
			num_no_full +=1
			all_full = False
			if marg_gain >= (v/2.0 - f_cover(S[v]))/(k - len(S[v])):
				# print "threshold",(v/2.0 - f_cover(S[v]))/(k - len(S[v]))
				# print "Adding", input_set, "to", v, S[v]
				S[v].append(input_set)
	if float(num_no_full)/len(S) < 0.05:
		print "terminate"
		print "S len:"
		all_full = True
		for i in range(k, k*m + 1, 1):
			print len(S[i]),
		print


def N(S, E, V): # N(x)={y in V(G)| (x,y) in E(G)}, N(S)=U x in S N(x);
	# print "S,V",S,V
	N_S = set()
	for u in S:
		for v in set(V):
			if(frozenset([u, v]) in E): # neighbors
				N_S.add(v)
	return N_S

def comp_Potential(K, V_remain, E, theta, x, N_r):
	# N_r_S = compute_N_r(S, theta)
	# print "x", x, "K",K
	
	N_x = set()
	for v in set(K | V_remain):
		if(frozenset([x, v]) in E): # neighbors
			N_x.add(v)
	N_r_x = N_x & set(N_r)

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

def compute_N_r(K, V_remain, E, theta): # find all gamma neighbors on set S from V_remain
	N_r = set()
	# print N_r
	for u in K:
		# print 'u',u
		for v in V_remain:
			if(frozenset([u, v]) in E): # neighbors
				
				S_temp = K.copy()
				S_temp.add(v)
				# r neighbor or not!!!!!!!! Change here
				# if(util.computeDensity(S_temp, E) >= theta):
				N_r.add(v)	
					# print "v",v
	return N_r	

def sort_N_r(K, V_remain, E, theta, N_r):
	potential_D = {}
	for x in N_r:
		potential_D[x] = comp_Potential(K, V_remain, E, theta, x, N_r)
		# print "potential:",x,potential_D[x]
	return sorted(N_r, key = lambda k: potential_D[k], reverse = True)


def grasp_sort(K, V_remain, E, theta):
	N_r = compute_N_r(K, V_remain, E, theta)
	# print "N_R here!!!!!!", N_r
	N_r_sorted = sort_N_r(K, V_remain, E, theta, N_r)
	return N_r_sorted

def enumPseudoClique(K, V_remain, E, V, theta, max_dense, dense, Ancestors):
	''' --------------@para: no of elem in K-------------- '''
	if all_full:
		# print "========= all_full ========="
		return
	# for elem in K:
	# 	print str(elem) + "\t",
	# print float(dense)
	# print
	if len(K) > min_elem_output:
		print str(K) +"\t" + str(dense)
	if 0 == len(V_remain):
		# # print "===========reach base case ==========="
		# # print "leaf node", K
		# should_add = True
		# for each_set in max_dense:
		# 	if set(each_set[0]).issuperset(set(K)):
		# 		should_add = False
		# 		break
		# if should_add:
		# 	max_dense.append((K, dense))
		sieve(set(K))
	 	return


	if len(K) != 0: # 1st level
		# print "000000"
		V_remain_in_seq = grasp_sort(set(K), set(V_remain), E, theta)
		# print "V_remain_in_seq", V_remain_in_seq
	# else:
	# 	print "===========@@@@@@@@@@@@@@@==========="
	# 	V_remain_in_seq = list(V_remain)
	# 	print "1st level V_remain_in_seq", V_remain_in_seq
		# V_remain_in_seq = grasp_sort(set(K), set(V_remain), E, theta)

	
	# print "V_not_K: ",V_not_K
	# V_remain_in_seq = my_sort_V(K, V_remain, E)
	for i in range(len(V_remain_in_seq)):
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

		D = util.computeDegree(list(K_new), E)
		# print "D",D,"K_new",K_new
		min_deg = util.min_degree(D)

		K_new.append(v)

 		# print "K_new",K_new

		new_dense = util.computeDensity(set(K_new), E)
		# print "dense",new_dense

		if new_dense >= theta:
			# print "Old Ancestors:", Ancestors
			Ancestors_new =  Ancestors | set(V_remain_in_seq[:i])
			# print "v is", v
 			# print "Ancestors:", Ancestors_new
	 		if v in Ancestors:
	 			# print "In Ancestors......."
 				continue
			V_new = list(N(set(K_new), E, V)  - set(K_new) - Ancestors)
 			# print "Ancestors:", Ancestors_new
			# print "v_deg",v_deg,"min_deg",min_deg
			# if min_deg+1 < v_deg:
			# 	print "@@@@@@@@@  min_deg is small @@@@@@@@@"
			# 	print "v_deg",v_deg,"min_deg",min_deg
			# 	print K
			enumPseudoClique(K_new, V_new, E, V, theta, max_dense, new_dense, Ancestors_new)

			# else:
			# 	enumPseudoClique(K_new, V_new, E, V, theta, max_dense, new_dense, Ancestors_new)
			# else:
				# if min_deg+1 >= v_deg:
					# enumPseudoClique(K_new, V_new, E, V, theta, max_dense, new_dense)

		sieve(set(K))			
	# print "Reset Ancestors......"
	Ancestors = set()
	# print "S len:"
	# for i in range(k, k*m + 1, 1):
	# 	print len(S[i]),
	# print
	# should_add = True
	# for each_set in max_dense:
	# 	if set(each_set[0]).issuperset(set(K)):
	# 		# print "Here"
	# 		should_add = False
	# 		break
	# if should_add:
	# 	# print "leaf node", K, "dense", dense 
	# 	max_dense.append((K, dense))


# main
def main(input_file):
	print "Reading from:", input_file
	(V, E, AdjList) = util.readinput(input_file, mytype = "str", myDelimiter = "\t")
	
	max_dense = []

	# time.sleep(0.5)
	print "V input length ", len(V)
	print "E input length ", len(E)
	for i in range(len(V)):
		# print "V[i]",V[i]
		if all_full:
			continue
		K = [V[i]]
		V_new = copy.copy(V)
		V_new.pop(i)
		print "========= progress =========: ",round(float(i)/len(V),2)
		# print "Ancestors:", set(V[:i])

		enumPseudoClique(K, V_new, E, V, theta, max_dense, 1.0, set(V[:i]))
	# pickle.dump( max_dense, open( "save-0.5.p", "wb" ) )
	# max_dense = pickle.load( open( "save-0.5.p", "rb" ) )
	# print "max_dense_graph:"

	# coverage_set = set()
	# for each_set in max_dense:
	# 	if(len(each_set[0]) > 2 and len(each_set[0]) <=10 ):
	# 		for elem in each_set[0]:
	# 			if elem not in coverage_set:
	# 				# print elem
	# 				coverage_set.add(elem)
	# 		print str(each_set[0]) + '\t' + str(each_set[1])

	# print "coverage: ",len(coverage_set)
	(maxV, maxF) = (0,0)
	for i in S.keys():
		# print 'v=',i, 'len=',len(S[i]),'cover=',f_cover(S[i])
		if maxF < f_cover(S[i]):
			(maxV, maxF) = (i, f_cover(S[i]))
			
	# print "====="
	# print "Best v",maxV, "with coverage",maxF


	print "========================="
	print "top-k",k,"threshold", theta
	print "========================="
	coverage_set = set()
	max_dense =  S[maxV]
	for elem in max_dense:
		if(len(elem) >= min_elem_output):
			# density = util.computeDensity(elem, E)
			# print elem, density
			for node in elem:
				print node + " ",
			print

	print "coverage",maxF
		# if(len(elem[0]) >= 3 and len(elem[0]) <=8 ):




if(len(sys.argv) != 5):
	print "Usage: **.py <inputfile> <k> <threshold> <min_elem_output>"
	# input_line  = raw_input("Exit? Y or N: ")
	# if(input_line in ['Y','y','Yes','YES','yes']):
	# 	sys.exit()
	print "Running default... k=20, theta=0.97, min_elem_output=3"

	# input_file = "../data/input_enum.txt"
	# input_file = "../data/input_whole_enum.txt"
	# input_file = "../data_tweet/tweet_complete_processed.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/collins2007.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/krogan2006_core.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/gavin2006_socioaffinities_rescaled.txt"
	input_file = "../data_tweet/corenlp_news/result.txt"
	k = 20
	theta = 0.7
	min_elem_output = 3

else:
	input_file = sys.argv[1]
	k = int(sys.argv[2])
	theta = float(sys.argv[3])
	min_elem_output = int(sys.argv[4])

m = 10
O = []
S = {}
all_full = False
for i in range(k, k*m + 1, 1):
	O.append(i)
	S[i] = []
start_time = time.time()
main(input_file)
# print "all_full", all_full
print("--- %s seconds ---" % (time.time() - start_time))








