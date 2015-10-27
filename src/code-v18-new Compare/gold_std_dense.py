# from pseudeo_clique_caller.py import enumPseudoClique_1st_level
import util
import copy
import numpy as np
import sys
import time
import pickle
import profile
from collections import defaultdict
import matplotlib.pyplot as plt

# def _compute_density(nodeList):
# 	for u in nodeList:
# 		for v in AdjList[u]

def eval_mips(fileN, fname, no):
	# fout = open(out_file, 'w+')
	s = 0.0
	cnt = 0
	mips = []
	with open(fileN) as gold_standard:
		for subgraph in gold_standard:
			nodeList = subgraph.strip('\n').split(' ')
			# print nodeList

			d = util.computeDensityNew(set(nodeList), AdjList	)
			mips.append(d)
			if d>=0.3:
				s+=d
				cnt+=1

			# print str(d) + ",",
			# for elem in nodeList:
			# 	print elem,
			# print
			# break
	# print s/cnt
	plt.subplot(2, 1, 1)
	plt.hist(mips, 50)
	# plt.title('mips')
	plt.xlabel(fname+' mips density')


def eval_sgd(fileN, fname, no):
	s = 0.0
	cnt = 0
	sgd = []
	with open(fileN) as gold_standard:
		for subgraph in gold_standard:
			nodeList = subgraph.strip('\n').split('\t')
			# print nodeList

			d = util.computeDensityNew(set(nodeList), AdjList	)
			sgd.append(d)
			
			if d>=0.3:
				s+=d
				cnt+=1
			# print str(d) + "\t",
			
			# for elem in nodeList:
			# 	print elem,
			# print
			# break
	# print s/cnt
	plt.subplot(2, 1, 2)
	plt.hist(sgd, 50)
	# plt.title('sgd')
	plt.xlabel(fname+' sgd density')


input_file1 = "../../data/data_bio/cl1_datasets/datasets/collins2007.txt"
input_file2 = "../../data/data_bio/cl1_datasets/datasets/krogan2006_core.txt"
input_file3 = "../../data/data_bio/cl1_datasets/datasets/krogan2006_extended.txt"
input_file4 = "../../data/data_bio/cl1_datasets/datasets/gavin2006_socioaffinities_rescaled.txt"
inList = [input_file1, input_file2, input_file3, input_file4]
input_file_sgd = "../../data/data_bio/cl1_gold_standard/gold_standard/sgd.txt"
input_file_mips = "../../data/data_bio/cl1_gold_standard/gold_standard/mips_3_100.txt"

# out_file = './gold_std_density/gavin.txt'



# plt.show()
cnt = 0
for input_file in inList:
	# input_file = inList[0]
	cnt+=1
	(V, E, AdjList, D) = util.readinputNumpy(input_file, mytype = "str", myDelimiter = "\t")
	print input_file.split('/')[-1]
	fname = input_file.split('/')[-1]
	fname = fname.split('.')[0]
	# print "V",len(V), "E",len(E)
	# print "Evaluating", input_file_sgd
	# print AdjList
	eval_mips(input_file_mips, fname, cnt)
	# print
	print "============================================================"
	eval_sgd(input_file_sgd, fname, cnt)
	print
	# print "Evaluating", input_file_mips
	plt.show()
	
	# break

