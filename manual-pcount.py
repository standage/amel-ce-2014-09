#!/usr/bin/env python
from scipy import stats

cont_table = [[207, 546], [142, 541]]
oddsratio, pcount = stats.fisher_exact(cont_table)
print "%.5f" % pcount
