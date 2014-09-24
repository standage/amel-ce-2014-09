#!/usr/bin/env python
import sys
from scipy import stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

statsmod = importr("stats")
df = 4

pvalues = []
adj_pvalues = []
infile = open(sys.argv[1], "r")
infile.readline()
for line in infile:
  fields = line.rstrip().split("\t")
  chi2 = float(fields[-1])
  pvalue = stats.chisqprob(chi2, df)
  pvalues.append(pvalue)

adj_pvalues = statsmod.p_adjust(FloatVector(pvalues), method="BH")
pvalues = list(reversed(pvalues))
adj_pvalues = list(reversed(adj_pvalues))

infile = open(sys.argv[1], "r")
header = infile.readline().rstrip()
header += "\tPvalue\tAdjPvalue"
print header
for line in infile:
  p = pvalues.pop()
  ap = adj_pvalues.pop()
  line = line.rstrip() + "\t%.5f\t%.5f" % (p, ap)
  print line
