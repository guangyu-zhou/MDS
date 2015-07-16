import codecs
def construct_Dict():
	authorID = {}
	# fin = codecs.open("./authorsLabel.txt", 'r','utf-8')
	fin = open("./authorsLabel.txt")
	for line in fin:
		line = line.strip("\n").split('\t')
		# print line[1]
		authorID[line[0]] = line[1]
	return authorID

def parseMDS(authorID, showSize = True):
	# fin = open("./agm/agm-package/bigclam/test1000.txt")
	fin = open("/Users/DavidZhou/Google Drive/15sp/research/ma/code/code-compare/dblp0.7-New-p0.3-Name.txt")
	fout = codecs.open('data1000.txt','w','utf-8')

	for line in fin:
		line = line.strip("\n").split('\t')
		line = line[:-1]
		if showSize:
			fout.write(str(len(line)) + '\t')
			print str(len(line))+ '\t',

		for eachId in line:
			print authorID[eachId]+ '\t',
			fout.write(authorID[eachId].decode("utf8") + '\t')
		fout.write('\n')
		print
		# break
		# print

def parseAA(authorID):
	fin = open("./aa.txt")
	fout = codecs.open('result.txt','w','utf-8')

	for line in fin:
		line = line.strip("\n").split('\t')
			
		for eachId in line[:-1]:
			print authorID[eachId]+ '\t',
			fout.write(authorID[eachId].decode("utf8") + '\t')
		fout.write(line[-1] + '\n')
		print
		# break
		# print

def main():
	authorID = construct_Dict()
	# print authorID['2']
	parseMDS(authorID, showSize = True)
	# parseAA(authorID)
	

main()