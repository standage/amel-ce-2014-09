#!/usr/bin/env python
import sys

cov = {}
exons = {}
for infile in sys.argv[1:]:
  cov[infile] = {}
  for line in open(infile, "r"):
    exon, coverage = line.rstrip().split("\t")
    exons[exon] = 1
    cov[infile][exon] = coverage

for exon in exons:
  sys.stdout.write(exon)
  for infile in sys.argv[1:]:
    sys.stdout.write("\t"+ cov[infile][exon])
  sys.stdout.write("\n")
