#!/usr/local/env python
#
# Input:  Gene annotation in GFF3 format and a list of cassette exons
# Output: A GFF3 file containing all exons from either input file
import sys

usage = "python exon-gff3.py annot.gff3 CE > exons.gff3"
assert len(sys.argv) == 3, "error: expected 2 arguments; usage: %s" % usage

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
  exongff3 = [fields[0], ".", "exon", fields[2], fields[3], ".", ".", ".", "."]
  print "\t".join(exongff3)
  
