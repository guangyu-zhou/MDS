import util
import Queue
import copy
import time

class partionSet:
	def __init__(self, v, AdjList,D):
		self.vs = set([v])
		self.inDeg = 0.0
		self.outDeg = D[v]
		self.outN = set()
		

	def add(self, u, AdjList):
		for elem in AdjList[u]:
			if elem[0] in self.vs:
				self.inDeg += elem[1]
				self.outDeg -= elem[1]
			else:
				self.outDeg += elem[1]

		self.vs.add(u)


def cohesiveness(K):
	if len(K.vs) == 1:
		# print  "COH", "0.0", K.vs
		return 0.0
	# print "COH",K.inDeg, K.outDeg, K.inDeg/(K.inDeg+K.outDeg), K.vs
	return K.inDeg/(K.inDeg+K.outDeg)


def doPartition(q, K, V, E, AdjList, D):
	while(not q.empty()):
		curV = q.get()
		for elem in AdjList[curV]:
			if elem[0] not in CoveredV:
				# print "CoveredV",CoveredV
				# print 
				K_new = copy.deepcopy(K)
				K_new.add(elem[0], AdjList)
				print "K is ", K.vs, "elem", elem[0], "coh:", cohesiveness(K_new)
				# print cohesiveness(K_new), cohesiveness(K)
				if cohesiveness(K_new) >= cohesiveness(K):
					# print "!!!!! good, adding ", elem[0]
					K.add(elem[0], AdjList)
					CoveredV.add(elem[0])
					CoveredV.add(curV)
					q.put(elem[0])
					# print K.vs
					# print 

		# print
	return K

def main():
	# input_file = "../data/input_enum.txt"
	# input_file = "../data_tweet/input_whole_enum.txt"
	# input_file = "../data_tweet/tweet_complete_processed.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/collins2007.txt"
	input_file = "../data_bio/cl1_datasets/datasets/krogan2006_core.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/krogan2006_extended.txt"
	# input_file = "../data_bio/cl1_datasets/datasets/gavin2006_socioaffinities_rescaled.txt"
	# input_file = "../data_tweet/corenlp_news/result10k.txt"
	# input_file = "../data_snap/dblp_whole.txt"
	start_time = time.time()
	(V, E, AdjList, D) = util.readinput(input_file, mytype = "str", myDelimiter = "\t", isWeight = False)
	print "Reading time", time.time() - start_time
	print "# V", len(V), "# E", len(E)
	PartitionV = []
	# print V
	for i in range(len(V)):
		print "======== in ", i ,len(V), " ========"
		curV = V[i]

		# print "CoveredV", (curV in CoveredV), curV
		if (curV in CoveredV):
			print "***********Skip seed ***********: ", V[i]
			continue

		q = Queue.Queue()
		q.put(curV)
		
		K = partionSet(curV, AdjList, D)
		# print "K created: ", K.vs, K.inDeg, K.outDeg, AdjList[curV]
		retPart = doPartition(q, K, V, E, AdjList,D)
		# print retPart.vs
		PartitionV.append(retPart)

	sum0 = 0
	for K in PartitionV:
		print len(K.vs)
		sum0+=len(K.vs)
	print "# of partitions", len(PartitionV)

CoveredV = set()
if __name__ == "__main__":
	start_time = time.time()
	main()
	print "Runing time", time.time() - start_time
