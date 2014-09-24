#!/usr/bin/env python
import sys

mapping = {}
for line in open(sys.argv[1], "r"):
  fields = line.split("\t")
  beebaseid = fields[1]
  ncbiid = fields[2]
  mapping[ncbiid] = beebaseid

for line in open(sys.argv[2], "r"):
  fields = line.rstrip().split("\t")
  if len(fields) < 9 or fields[2] != "exon":
    continue
  fields[0] = mapping[fields[0]]
  print "\t".join(fields) 
