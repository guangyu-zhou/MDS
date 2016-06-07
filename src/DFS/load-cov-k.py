import util
import numpy as np
import sys
def loadMDSFile(fname):
	V = set()
	max_dense = []
	fin = open(fname)
	for line in fin:
		line = line.strip("\n").split("\t")
		for v in line[:-1]:
			if v not in V:
				V.add(v)
		max_dense.append(line[:-1])
		# for elem in 
		# print line[:-1]
		# print "elem" + str(line),
	# print
	return max_dense, V

def cov_k(V, S, thre):
	D = []
	S1 = S
	V1 = set(V)
	covers = set()
	k = 0
	while True and len(S1) > 0:
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
		covers |= C
		k += 1.0
		# print k == len(D)
		# print "len(covers)/k", len(covers)/k
		if len(covers)/k < thre:
			break
	# print D
	# for c in D:
	# 	covers |= c
	# print len(D)
	# print "coverage: " + str(len(covers))
	return D


def main(bioname, theta):
	# input_file = "/Users/DavidZhou/Google Drive/15sp/research/ma/code/human/link_scores.txt"
	# (V, E, AdjList, D) = util.readinputNumpy(input_file, mytype = "str", myDelimiter = "\t")
# 	gavin2006_socioaffinities_rescaled.txt
# collins2007.txt
# krogan2006_core.txt
# krogan2006_extended.txt
	thre = 5.0
	print "Cov/k =", thre
	filename = "result-nonskip-w/" + bioname + "-d" + str(theta) +"-nonskip.txt"
	# fout = open("../temp_result.txt", "w+")
	fout = open("../../data/data_bio/reproducibility/cur/" + bioname + "-d" + str(theta) + "-t" + str(thre) +".txt", "w+")

	max_dense, V = loadMDSFile(filename)

	S = []
	for elem in max_dense:
		# print "Adding...",set(elem)
		S.append(set(elem))
	
	# print "len(S)", len(S)
	# thre = float(sys.argv[2])
	
	covers = cov_k(set(V), S, thre)


	# print "Density:"
	coverage = set()
	for each_set in covers:
		# print each_set[0], covers
		# if(set(each_set) in covers):
		for elem in each_set:
			coverage.add(elem)
			fout.write(elem + "\t")
		fout.write("\n")
	print len(coverage)
	print len(covers)

theta = sys.argv[1]
print "d", theta
# for bioname in [ "gavin2006_socioaffinities_rescaled", "collins2007", "krogan2006_core", "krogan2006_extended"]:
for bioname in [  "collins2007"]:
	main(bioname, theta)




