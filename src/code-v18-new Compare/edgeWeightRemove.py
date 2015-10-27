import util
import numpy as np
import sys
import os
from fnmatch import fnmatch

# def computeEdgeWeight(fname, E):
# 	fin = open("result-nonskip-uw/" + fname)
# 	for line in fin:
# 		vs = line.strip("\n").split("\t")[:-1]
# 		print vs
# 		for i in range(len(vs) - 1):
# 			for j in range(i,len(vs),1):



def main(bioname, gamma, inFilename):
	# input_file = "/Users/DavidZhou/Google Drive/15sp/research/ma/code/human/link_scores.txt"

	(V, E, AdjList, D) = util.readinputNumpy('../../data/datasets/' + bioname + '.txt', mytype = "str", myDelimiter = "\t")
	
	outFilename = "result-edgeWeight/" + inFilename + "-w" + str(gamma) +".txt"

	
			
	
	fout = open(outFilename, "w+")
	# fout = open("../../data/data_bio/reproducibility/cur/" + bioname + "-d" + str(gamma) + "-t" + str(thre) +".txt", "w+")

	fin = open("result-nonskip-uw/" + inFilename)
	cntOri = 0
	cntReal= 0

	for line in fin:
		cntOri +=1
		avgEdgeWeight = 0.0

		numEdges = 0
		vs = line.strip("\n").split("\t")[:-1]
		# print vs
		for i in range(len(vs) - 1):
			for j in range(i+1,len(vs),1):
				# print frozenset((vs[i], vs[j])), E[frozenset((vs[i], vs[j]))]
				if frozenset((vs[i], vs[j])) in E:
					avgEdgeWeight+=E[frozenset((vs[i], vs[j]))]
					numEdges+=1
					# print E[frozenset((vs[i], vs[j]))]
		# print avgEdgeWeight/numEdges
		if avgEdgeWeight/numEdges> float(gamma):
			cntReal+=1
			# print line
			# print avgEdgeWeight*1.0/len(vs), gamma

			fout.write(line)
	# avgEdgeWeight = computeEdgeWeight(inFilename, E)
	print cntOri, cntReal

gamma = sys.argv[1]
print "min weight", gamma
for bioname in [ "gavin2006_socioaffinities_rescaled", "collins2007", "krogan2006_core", "krogan2006_extended"]:
	print bioname
	for file in os.listdir("result-nonskip-uw/"):
		# print file
		if fnmatch(file, bioname + "*.txt"):
			print "file:", file
			main(bioname, gamma, file)
			# break
	# break




