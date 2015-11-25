import random as r
# import argparse  # TODO !

inpath = "../data/test.csv"     # TODO use args
outpath = inpath + ".sampled"   # TODO use args
ratioToKeep = 0.2       # TODO use args
labelsToKeep = ['1']    # TODO optional arg (in case of imbalanced data...)
seed = 26               # TODO optional arg
sep = ','               # TODO optional arg
# TODO : now assuming class label is the last column; arg 


f = open(inpath, 'r')
out = open(outpath, 'w')
r.seed(seed)

# TODO : now I always keep the first line, it could be a header... add an arg!
line = f.readline()
out.write(line)

discardedCnt = 0
allLines = 1

for line in f:
	fields = line.strip().split(sep)
	allLines = allLines + 1
	# checking class label
	if fields[-1] in labelsToKeep:
		out.write(line)
	else:  
		randnumber = r.random()
		if randnumber < ratioToKeep:
			out.write(line)
		else:
			discardedCnt = discardedCnt + 1
		if allLines % 100000 == 0:
			print("At line " + str(allLines) + " ...")

f.close()
out.close()
print(str(discardedCnt) + " lines were discarded from " + str(allLines))
