#!/usr/bin/env python
import numpy, re, sys
from scipy import stats

numpy.seterr(invalid='ignore')

control_cov = {}
treatment_cov = {}
exons_by_start = {}
exons_by_end = {}
for line in open(sys.argv[1], "r"):
  fields = line.rstrip().split("\t")
  exon = fields[0]
  idmatch = re.search("(\S+)_(\d+)-(\d+)", exon)
  assert idmatch, "error parsing exon ID"
  seqid = idmatch.group(1)
  start = idmatch.group(2)
  end   = idmatch.group(3)
  control_cov[exon] = map(float, fields[1:7])
  treatment_cov[exon] = map(float, fields[7:])
  if start not in exons_by_start:
    exons_by_start[start] = []
  exons_by_start[start].append(exon)
  if end not in exons_by_end:
    exons_by_end[end] = []
  exons_by_end[end].append(exon)


header = sys.stdin.readline()
header = header.rstrip()
header += "\tPcov"
print header
for line in sys.stdin:
  line = line.rstrip()
  fields = line.split()
  assert len(fields) == 11, "expected 11 fields, found %d: %s" % (len(fields), line)
  if fields[1] not in exons_by_end:
    continue
  if fields[4] not in exons_by_start:
    continue
  upstream_exons = exons_by_end[fields[1]]
  downstream_exons = exons_by_start[fields[4]]
  if len(upstream_exons) != 1 or len(downstream_exons) != 1:
    continue

  upstream_exon    = upstream_exons[0]
  cov_ab_control   = control_cov[upstream_exon]
  cov_ab_treatment = treatment_cov[upstream_exon]
  downstream_exon  = downstream_exons[0]
  cov_cd_control   = control_cov[downstream_exon]
  cov_cd_treatment = treatment_cov[downstream_exon]
  skipped_exon     = "%s_%s-%s" % (fields[0], fields[2], fields[3])
  assert skipped_exon in control_cov and skipped_exon in treatment_cov, "missing exon %s" % skipped_exon
  cov_pq_control   = control_cov[skipped_exon]
  cov_pq_treatment = treatment_cov[skipped_exon]

  control_es_ratios = []
  for i in range(len(cov_ab_control)):
    cov_ab = cov_ab_control[i]
    cov_cd = cov_cd_control[i]
    cov_pq = cov_pq_control[i]
    ratio = 0
    if cov_ab + cov_cd > 0:
      ratio = (cov_ab + cov_cd - (2 * cov_pq)) / (cov_ab + cov_cd)
    control_es_ratios.append(ratio)

  treatment_es_ratios = []
  for i in range(len(cov_ab_treatment)):
    cov_ab = cov_ab_treatment[i]
    cov_cd = cov_cd_treatment[i]
    cov_pq = cov_pq_treatment[i]
    ratio = 0
    if cov_ab + cov_cd > 0:
      ratio = (cov_ab + cov_cd - (2 * cov_pq)) / (cov_ab + cov_cd)
    treatment_es_ratios.append(ratio)

  tstat, pvalue = stats.ttest_ind(control_es_ratios, treatment_es_ratios)
  line += "\t%.5f" % pvalue
  print line
