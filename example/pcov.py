#!/usr/local/bin env
from scipy import stats

control = [-0.08388, -0.08664, -0.12015, -0.15473, -0.05790, -0.05036]
treatment = [-0.22015, -0.14484, 0.02633, -0.05601, -0.02995, -0.05089]
tstat, pvalue = stats.ttest_ind(control, treatment)
print "%.5f" % pvalue
