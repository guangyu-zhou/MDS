import util
import numpy as np
import sys
import os
from fnmatch import fnmatch

def computeEdgeWeight(path,fname):
	fin = open(path+ fname + '.txt')
	fout = open('../../data/datasets_pseudo/' + fname + '-d'  + str(d) + '.txt', 'w+')
	cnt = 0
	cnt2 = 0
	for line in fin:
		cnt+=1
		vs = line.strip("\n").split("\t")
		print vs[-1]
		if float(vs[-1]) > d:
			cnt2+=1
			# fout.write(vs[0] + '\t' + vs[1] + '\t' + vs[2] + '\n')
			fout.write(vs[0] + '\t' + vs[1] + '\t' + str(1) + '\n')

		# for i in range(len(vs) - 1):
	print cnt, cnt2

path = "../../data/datasets/"

inFile = ["gavin2006_socioaffinities_rescaled",
"collins2007",
"krogan2006_core",
"krogan2006_extended"]

d = 0.5
# for f in inFile:
f = inFile[1]
computeEdgeWeight(path, f)