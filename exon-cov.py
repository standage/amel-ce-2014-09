#!/usr/bin/env python
import sys

exon_coverage = {}
exon_length = {}
for line in sys.stdin:
  fields = line.split("\t")
  exon = "%s_%s-%s" % (fields[0], fields[3], fields[4])
  if exon not in exon_coverage:
    exon_coverage[exon] = 0
    exon_length[exon] = int(fields[4]) - int(fields[3]) + 1
  exon_coverage[exon] += int(fields[10])

for exon in exon_coverage:
  length = exon_length[exon]
  cov = exon_coverage[exon]
  print "%s\t%.2f" % (exon, float(cov) / float(length))
