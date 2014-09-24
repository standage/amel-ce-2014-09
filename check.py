#!/usr/bin/env python
import sys

exons_endmatch = {}
exons_startmatch = {}
for line in open(sys.argv[1], "r"):
  fields = line.split("\t")
  seqid, start, end = fields[0], fields[3], fields[4]
  coord = "%s_%s-%s" % (seqid, start, end)

  if seqid not in exons_endmatch:
    exons_endmatch[seqid] = {}
  if end not in exons_endmatch[seqid]:
    exons_endmatch[seqid][end] = {}
  exons_endmatch[seqid][end][coord] = 1

  if seqid not in exons_startmatch:
    exons_startmatch[seqid] = {}
  if start not in exons_startmatch[seqid]:
    exons_startmatch[seqid][start] = {}
  exons_startmatch[seqid][start][coord] = 1


for line in open(sys.argv[2], "r"):
  fields = line.rstrip().split("\t")
  seqid, exona_end, exonc_start = fields[0], str(int(fields[1])-1), fields[4]

  endmatches = 0
  if seqid in exons_endmatch and exona_end in exons_endmatch[seqid]:
    endmatches = len(exons_endmatch[seqid][exona_end])
  print "%d" % endmatches

  startmatches = 0
  if seqid in exons_startmatch and exonc_start in exons_startmatch[seqid]:
    startmatches = len(exons_startmatch[seqid][exonc_start])
  print >> sys.stderr, "%d" % startmatches

  
