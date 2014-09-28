#!/usr/bin/env python
from scipy import stats
from math import log

df     = 4 # k=2 probabilities, 2k=4
pcount = 0.00287
pcov   = 0.74836

chi2 = -2 * ( log(pcount) + log(pcov) )
pvalue = stats.chisqprob(chi2, df)
print "Chi2 value: %.3f" % chi2
print "Combined Pvalue: %.5f" % pvalue
