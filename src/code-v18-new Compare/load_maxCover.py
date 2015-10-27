import util
import numpy as np
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


def load_maxCover():
	# input_file = "/Users/DavidZhou/Google Drive/15sp/research/ma/code/human/link_scores.txt"
	# (V, E, AdjList, D) = util.readinputNumpy(input_file, mytype = "str", myDelimiter = "\t")
	max_dense, V = loadMDSFile("/Users/DavidZhou/Google Drive/15sp/research/ma/code/git/MDSMine/result/partition/biogrid-0.8-extend2.txt")

	S = []
	for elem in max_dense:
		# print "Adding...",set(elem)
		S.append(set(elem))
	
	print "len(S)", len(S)
	k = 200
	print "Max cover, k=" + str(k)
	covers = MaxCover(set(V), S, k)
	print len(covers)


	# print "Density:"
	for each_set in max_dense:
		# print each_set[0], covers
		if(set(each_set) in covers):
			for elem in each_set:
				print elem,
			print

def countCov():
	max_dense, V = loadMDSFile("./firstBranch-nonsieve-result/krogan2006_extended-d0.5.txt")
	coverSet = set()
	for elem in max_dense:
		# print "Adding...",set(elem)
		for node in elem:
			coverSet.add(node)
	print len(coverSet)

# load_maxCover()
countCov()
