#!/usr/local/env python
import sys

exons = {}
for line in open(sys.argv[1], "r"):
  fields = line.split("\t")
  if len(fields) < 9 or fields[2] != "exon":
    continue
  print line.rstrip()
  exon = "%s_%s-%s" % (fields[0], fields[3], fields[4])
  exons[exon] = 1

for line in open(sys.argv[2], "r"):
  fields = line.split("\t")
  fields[3] = str(int(fields[3]) - 1)
  intrnlexon = "%s_%s-%s" % (fields[0], fields[2], fields[3])
  if intrnlexon in exon:
    continue
  print >> sys.stderr, "DEBUG"
  exongff3 = [fields[0], ".", "exon", fields[2], fields[3], ".", ".", ".", "."]
  print "\t".join(exongff3)
  
