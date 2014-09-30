#!/usr/bin/env python
from scipy import stats
from math import log

# Pcount calculation
cont_table = [[208, 546], [218, 801]]
oddsratio, pcount = stats.fisher_exact(cont_table)
print "Pcount: %.5f" % pcount

# Pcov calculation
control = [-0.08388, -0.08664, -0.12015, -0.15473, -0.05790, -0.05036]
treatment = [-0.22015, -0.14484, 0.02633, -0.05601, -0.02995, -0.05089]
tstat, pcov = stats.ttest_ind(control, treatment)
print "Pcov: %.5f" % pcov

# Fisher's combined probability
df = 4 # k=2 probabilities, 2k=4
chi2 = -2 * ( log(pcount) + log(pcov) )
pvalue = stats.chisqprob(chi2, df)
print "Chi2 value: %.3f" % chi2
print "Combined Pvalue: %.5f" % pvalue
