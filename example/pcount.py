#!/usr/bin/env python
from scipy import stats

cont_table = [[208, 546], [218, 801]]
oddsratio, pcount = stats.fisher_exact(cont_table)
print "%.5f" % pcount
