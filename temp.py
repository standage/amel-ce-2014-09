#!/usr/bin/env python
from scipy import stats

cont_table = [[36,90], [51,197]]
oddsratio, pcount = stats.fisher_exact(cont_table)
print "%.5f" % pcount
