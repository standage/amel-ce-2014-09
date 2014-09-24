#!/usr/bin/env python
import sys
from math import log, isnan

header = sys.stdin.readline().rstrip()
header += "\tFinalP"
print header

for line in sys.stdin:
  line = line.rstrip()
  fields = line.split("\t")
  pcount, pcov = map(float, fields[-2:])
  if isnan(pcount) or isnan(pcov):
    print line + "\tnan"
    continue
  assert pcount >= 0.0 and pcov >= 0.0, "weird p-values: %s" % line
  print >> sys.stderr, line
  chi2 = -2 * ( log(pcount) + log(pcov) )
  print line + "\t%.5f" % chi2
