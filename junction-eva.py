#!/usr/bin/env python
#
# Input:  TrueSight SAM file
# Output: splice junctions in tab-delimited format, with the following fields:
#           - sequence ID
#           - start position
#           - end position
#           - read count (number of mapped reads spanning the junction)

import re, sys

junction_read_counts = {}
for line in sys.stdin:
  bam_fields = line.rstrip().split("\t")
  cigar = bam_fields[5]
  align_parts = re.split("M|N", cigar)
  assert align_parts.pop() == '', "expected empty string"
  if len(align_parts) == 1:
    continue # Ungapped alignments do not inform junctions, ignore

  cumulative_start = int(bam_fields[3])
  for i in range(1, len(align_parts), 2):
    start = cumulative_start + int(align_parts[i-1])
    end = start + int(align_parts[i])
    junction = "%s:%d:%d" % (bam_fields[2], start, end)
    if junction not in junction_read_counts:
      junction_read_counts[junction] = 0
    junction_read_counts[junction] += 1
    cumulative_start = end

for junction in junction_read_counts:
  seqid, start, end = junction.split(":")
  print "%s\t%s\t%s\t%d" % (seqid, start, end, junction_read_counts[junction])

