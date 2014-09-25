#!/usr/bin/env python
import sys
from scipy import stats
from math import isnan, log

header = sys.stdin.readline()
header = header.rstrip() + "\tPcount\tCombinedChi2"
print header
for line in sys.stdin:
  fields = line.rstrip().split("\t")
  #fields[1] = str(int(fields[1]) - 1)
  #fields[3] = str(int(fields[3]) - 1)
  pcov = float(fields[-1])
  control_ic = (int(fields[5]) + int(fields[6])) / 2
  control_is = int(fields[7])
  treatment_ic = (int(fields[8]) + int(fields[9])) / 2
  treatment_is = int(fields[10])
  pcount_str = "nan"
  if control_ic + control_is + treatment_ic + treatment_is > 0:
    oddsratio, pcount = stats.fisher_exact([[control_ic, control_is], [treatment_ic, treatment_is]])
    pcount_str = "%.5f" % pcount
  fields.append(pcount_str)

  if isnan(pcount) or isnan(pcov):
    fields.append("nan")
  else:
    assert pcount > 0.0 and pcov > 0.0, "weird p-values: %.5f and %.5f" % (pcov, pcount)
    chi2 = -2 * ( log(pcount) + log(pcov) )
    fields.append("%.5f" % chi2)
  print "\t".join(fields)
