from snap import *
import time
def construct_Dict():
	authorID = TIntStrH()
	# fin = codecs.open("./authorsLabel.txt", 'r','utf-8')
	fin = open("./authorsLabel.txt")
	for line in fin:
		line = line.strip("\n").split('\t')
		# print line[1]
		authorID[int(line[0])] = line[1]
	return authorID


# labels = TIntStrH()
s = time.time()
authorIdDict = construct_Dict()
# print authorIdDict
G = LoadEdgeList(PUNGraph, "aaNew10.txt", 0, 1)
# for EI in G.Edges():
# 	print "edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
DrawGViz(G, gvlSfdp, "graphNew10.png", "Co-author related to Jiawei Han", authorIdDict)
print "Time used:", time.time() - s
# import snap
# UGraph = snap.GenRndGnm(snap.PUNGraph, 10, 40)
# snap.DrawGViz(UGraph, snap.gvlNeato, "graph_undirected.png", "graph 2", True)