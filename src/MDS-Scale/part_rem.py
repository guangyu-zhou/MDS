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
		global CoveredV
		for elem in AdjList[u]:
			if elem[0] in CoveredV:
				# print "Add: In removed v", elem[0]
				if elem[0] not in self.vs:
					continue
			# print "Adding", elem[0]
				# if elem[0] in self.vs:
				else:
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

class MDS:
	def __init__(self, V_curSet, AdjList):
		self.vs = V_curSet
		weight = 0.0
		for v in V_curSet:
			for edge_weight in AdjList[v]:
				if(edge_weight[0] in V_curSet):
					weight+=edge_weight[1]
		
		self.inDeg = weight

	def add(self, nb, AdjList):

		weight = self.inDeg
		for edge_weight in AdjList[nb]:
				if(edge_weight[0] in self.vs):
					weight+=2*edge_weight[1]

		self.vs.add(nb)
		self.inDeg = weight

	def computeDenseNew(self, nb, AdjList):
		weight = self.inDeg
		for edge_weight in AdjList[nb]:
				if(edge_weight[0] in self.vs):
					weight+=2*edge_weight[1]

		n = len(self.vs) + 1
		return weight/((n-1)*n)



def cohesiveness(K):
	if len(K.vs) == 1:
		# print  "COH", "0.0", K.vs
		return 0.0
	# print "COH",K.inDeg, K.outDeg, K.inDeg/(K.inDeg+K.outDeg), K.vs
	return K.inDeg/(K.inDeg+K.outDeg)

def cohesiveness2(K, u, AdjList):
	global CoveredV
	inDeg = K.inDeg
	outDeg = K.outDeg
	vs = K.vs
	for elem in AdjList[u]:
		if elem[0] in CoveredV:
			# print "Cohesive: In removed v", elem[0]
			if elem[0] not in vs:
				continue
			# if elem[0] in vs:
			else:
				inDeg += elem[1]
				outDeg -= elem[1]
		# # else:
		# 	# print "Cohesive: ", elem[0]
		# 	if elem[0] in vs:
		# 		inDeg += elem[1]
		# 		outDeg -= elem[1]
		else:
			outDeg += elem[1]

	return inDeg/(inDeg+outDeg)



def doPartition(q, K, V, E, AdjList, D, partitionSize):  # don't consider any potins in coveredV
	global CoveredV
	# CoveredVCur = set()
	# start = time.time()
	flag = False

	while(not q.empty()):

		curV = q.get()
		for elem in AdjList[curV]:
			# if elem[0] not in CoveredVCur:
			if elem[0] not in CoveredV:

				# print "CoveredV",CoveredV
				# print 
				# print "K is ", len(K.vs)#, "elem", elem[0]#, "coh:", cohesiveness(K_new)
				# print cohesiveness(K_new), cohesiveness(K)
				if cohesiveness2(K, elem[0], AdjList) >= 0*cohesiveness(K) and len(K.vs) < partitionSize:
					K.add(elem[0], AdjList)
					flag = True
					# CoveredVCur.add(elem[0])
					CoveredV.add(elem[0])
					q.put(elem[0])
		if flag:
			# CoveredVCur.add(curV)
			CoveredV.add(curV)

	# print time.time() - start

	return K

def mainPartition(input_file, partitionTimes = 1000, threSize = 30, partitionSize = 1000):
	# print "partitionTimes", partitionTimes
	print "threSize",threSize
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
	(V, E, AdjList, D) = util.readinputNumpy(input_file, mytype = "str", myDelimiter = "\t")

	print "Reading time", time.time() - start_time
	print "# V", len(V), "# E", len(E)
	global CoveredV
	PartitionList = []
	outputList = []
	seeds = copy.copy(V)
	seeds.reverse()
	# random.shuffle(seeds)
	# print V
	
	while len(seeds) > 0:
		if len(CoveredV) >= len(V):
			print "End, enough cover"
			break
		# print "*********** Remaining partition times & covered V", partitionTimes , len(CoveredV) 
		curV = seeds.pop()
		# print "CoveredV", (curV in CoveredV), curV
		if (curV in CoveredV):
			# print "***********Skip seed ***********: ", curV
			continue

		q = Queue.Queue()
		q.put(curV)
		
		K = partionSet(curV, AdjList, D)
		# print "K created: ", K.vs, K.inDeg, K.outDeg, AdjList[curV]
		# print "start partition"
		retPart = doPartition(q, K, V, E, AdjList,D, partitionSize)
		if len(retPart.vs) > threSize:
			# print "large for partition",len(retPart.vs)#, retPart.vs
			PartitionList.append(retPart)
			partitionTimes-=1
		elif len(retPart.vs) > 2: 
			# print "small for output", len(retPart.vs)
			outputList.append(retPart)
			# partitionTimes-=1
		else:
			pass
		# 	# print "<3 pruned"
		# 	print ''

	# sum0 = 0
	# for K in PartitionList:
	# 	# print len(K.vs)
	# 	print K.vs
	# 	print K.es
	# 	sum0+=len(K.vs)
	# 	print
	print "# of partitions", len(PartitionList)
	print "CoveredV", len(CoveredV)
	return PartitionList, outputList, V, E, AdjList, D

CoveredV = set()
# input_file = "../../data/data_snap/dblp_whole.txt"
# input_file = "../data_tweet/input_whole_enum.txt"
# input_file = "../data_tweet/tweet_complete_processed.txt"
# input_file = "../../data/data_bio/cl1_datasets/datasets/biogrid_yeast_physical_unweighted.txt"
# input_file = "../../data/data_tweet/input_enum2.txt"
input_file = "/Users/DavidZhou/Google Drive/15sp/research/ma/code/human/link_scores_experimental.txt"


# mainPartition(input_file, partitionTimes = 1000, threSize = 20)
# main()
# if __name__ == "__main__":
# 	start_time = time.time()
# 	main()
# 	print "Runing time", time.time() - start_time
