#!/usr/bin/env python
#
# Input:  TrueSight SAM file (standard input), list of annotated cassette exons
#         (positional argument), and sample/rep label (positional argument)
# Output: skipped exon events, along with the number of mapped reads spanning
#         each associated splice junction
import re, sys

# Look at gapped alignments, determine # of mapped reads spanning each junction
junction_read_counts = {}
for line in sys.stdin:
  bam_fields = line.rstrip().split("\t")
  cigar = bam_fields[5]
  align_parts = re.split("M|N", cigar)
  assert align_parts.pop() == '', "expected empty string"
  if len(align_parts) == 1:
    continue # Ignore ungapped alignments
  cumulative_start = int(bam_fields[3])
  for i in range(1, len(align_parts), 2):
    start = cumulative_start + int(align_parts[i-1])
    end = start + int(align_parts[i])
    junction = "%s:%d:%d" % (bam_fields[2], start, end)
    if junction not in junction_read_counts:
      junction_read_counts[junction] = 0
    junction_read_counts[junction] += 1
    cumulative_start = end

# Look at each cassette exon, report # of mapped reads for each junction
label = sys.argv[2]
print ("seqid\texon1_e\texon2_b\texon2_e\texon3_b\t"+
       "%s:exon1-exon2\t%s:exon2-exon3\t%s:exon1-exon3" % (label, label, label))
for line in open(sys.argv[1], "r"):
  line = line.rstrip()
  seqid, exon1_e, exon2_b, exon2_e, exon3_b = line.split("\t")
  junc_1_2 = "%s:%s:%s" % (seqid, exon1_e, exon2_b)
  junc_2_3 = "%s:%s:%s" % (seqid, exon2_e, exon3_b)
  junc_1_3 = "%s:%s:%s" % (seqid, exon1_e, exon3_b)
  junc_1_2c = 0
  junc_2_3c = 0
  junc_1_3c = 0
  if junc_1_2 in junction_read_counts:
    junc_1_2c = junction_read_counts[junc_1_2]
  if junc_2_3 in junction_read_counts:
    junc_2_3c = junction_read_counts[junc_2_3]
  if junc_1_3 in junction_read_counts:
    junc_1_3c = junction_read_counts[junc_1_3]
  print "%s\t%d\t%d\t%d" % (line, junc_1_2c, junc_2_3c, junc_1_3c)
