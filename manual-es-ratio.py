#!/usr/bin/env python
import sys

exoncov = {}
for line in sys.stdin:
  exon, cov = line.rstrip().split("\t")
  exoncov[exon] = float(cov)

left_exon_cov    = exoncov[sys.argv[1]]
skipped_exon_cov = exoncov[sys.argv[2]]
right_exon_cov   = exoncov[sys.argv[3]]

es_skip_ratio = (left_exon_cov + right_exon_cov - (2 * skipped_exon_cov)) / (left_exon_cov + right_exon_cov)
print "%.5f" % es_skip_ratio
