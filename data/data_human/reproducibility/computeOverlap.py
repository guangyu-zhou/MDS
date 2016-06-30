# fin = open("./gold_standard/processed_groundTruth-3.txt")
# fin = open("./bio-gs/merged_gold_standard.txt")
# fin = open("./bio-gs/sgd-3.txt")
# fin = open("./bio-gs/mips_3_100.txt")
fin = open("./bio-gs/yeastProcessed.txt")




ns = set()
complexs = []
for l in fin:
	# print frozenset(l.split())
	complexs.append(frozenset(l.split()))
	for v in l.split():
		ns.add(v)
		# print v
	# break

cnt = 0
for i in range(len(complexs)):
	for j in range(i+1, len(complexs), 1):
		# print i,j
		if len(complexs[i] & complexs[j]) >0:
			cnt+=1
		# break
	# break


numComplex = len(complexs)
print len(ns),numComplex
print cnt,cnt*1.0/(numComplex*numComplex/2)


