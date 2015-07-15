import util
import Queue
import copy
import time
import random
from collections import defaultdict

class partionSet:
	def __init__(self, v, AdjList,D):
		self.vs = set([v])
		self.inDeg = 0.0
		self.outDeg = D[v]
		self.outN = set()
		self.es = {}
		self.adjs = defaultdict(lambda: set())
		self.ds = defaultdict(lambda: 0.0)
		

	def add(self, u, AdjList):
		for elem in AdjList[u]:
			if elem[0] in self.vs:
				self.inDeg += elem[1]
				self.outDeg -= elem[1]
				self.es[frozenset([u, elem[0]])] = elem[1]
				self.adjs[u].add((elem[0], elem[1]))
				self.adjs[elem[0]].add((u, elem[1]))
				self.ds[u]+= elem[1]
				self.ds[elem[0]]+= elem[1]
			else:
				self.outDeg += elem[1]

		self.vs.add(u)


def cohesiveness(K):
	if len(K.vs) == 1:
		# print  "COH", "0.0", K.vs
		return 0.0
	# print "COH",K.inDeg, K.outDeg, K.inDeg/(K.inDeg+K.outDeg), K.vs
	return K.inDeg/(K.inDeg+K.outDeg)

def cohesiveness2(K, u, AdjList):
	inDeg = K.inDeg
	outDeg = K.outDeg
	vs = K.vs
	for elem in AdjList[u]:
			if elem[0] in vs:
				inDeg += elem[1]
				outDeg -= elem[1]
			else:
				outDeg += elem[1]

	return inDeg/(inDeg+outDeg)



def doPartition(q, K, V, E, AdjList, D):
	global CoveredV
	CoveredVCur = set()
	# start = time.time()
	flag = False

	while(not q.empty()):

		curV = q.get()
		for elem in AdjList[curV]:
			if elem[0] not in CoveredVCur:
				# print "CoveredV",CoveredV
				# print 
				# print "K is ", K.vs, "elem", elem[0], "coh:", cohesiveness(K_new)
				# print cohesiveness(K_new), cohesiveness(K)
				if cohesiveness2(K, elem[0], AdjList) >= cohesiveness(K):
					K.add(elem[0], AdjList)
					flag = True
					CoveredVCur.add(elem[0])
					CoveredV.add(elem[0])
					q.put(elem[0])
		if flag:
			CoveredVCur.add(curV)
			CoveredV.add(curV)

	# print time.time() - start

	return K

def mainPartition(input_file, partitionTimes = 10, threSize = 400):
	# input_file = "../data_tweet/input_enum.txt"
	# input_file = "../data_tweet/input_whole_enum.txt"
	# input_file = "../data_tweet/tweet_complete_processed.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/collins2007.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/krogan2006_core.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/krogan2006_extended.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/gavin2006_socioaffinities_rescaled.txt"
	# input_file = "../data_tweet/corenlp_news/result10k.txt"
	# input_file = "../data_snap/dblp_.25.txt"
	# input_file = "../data_snap/dblp_whole.txt"
	start_time = time.time()
	(V, E, AdjList, D) = util.readinput(input_file, mytype = "str", myDelimiter = "\t", isWeight = False)
	# print "Reading time", time.time() - start_time
	# print "# V", len(V), "# E", len(E)
	global CoveredV
	PartitionList = []
	seeds = copy.copy(V)
	seeds.reverse()
	# print V
	
	while partitionTimes >0 and len(seeds) > 0:
		print "@@@@@@@@@@@ Remaining partition times", partitionTimes, len(seeds) ," @@@@@@@@@@@"
		curV = seeds.pop()
		# print "CoveredV", (curV in CoveredV), curV
		if (curV in CoveredV):
			print "***********Skip seed ***********: ", curV
			continue

		q = Queue.Queue()
		q.put(curV)
		
		K = partionSet(curV, AdjList, D)
		# print "K created: ", K.vs, K.inDeg, K.outDeg, AdjList[curV]
		print "start partition"
		retPart = doPartition(q, K, V, E, AdjList,D)
		if len(retPart.vs) > threSize:
			print curV, len(retPart.vs)
			PartitionList.append(retPart)
			partitionTimes-=1
		else:
			print len(retPart.vs), "too small"

	sum0 = 0
	# for K in PartitionList:
	# 	# print len(K.vs)
	# 	print K.vs
	# 	print K.es
	# 	sum0+=len(K.vs)
	# 	print
	# print "# of partitions", len(PartitionList)
	return PartitionList

CoveredV = set()
# input_file = "../data_snap/dblp_whole.txt"
# input_file = "../data_tweet/input_whole_enum.txt"
# input_file = "../data_tweet/tweet_complete_processed.txt"


# mainPartition(input_file, partitionTimes = 100, threSize = 1)
# main()
# if __name__ == "__main__":
# 	start_time = time.time()
# 	main()
# 	print "Runing time", time.time() - start_time
