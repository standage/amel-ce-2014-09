#!/usr/bin/env bash
set -e
which bowtie
which truesight_pair.pl
RNA=rnaseq
IDX=genome/amel
for cond in c t
do
  for rep in {1..6}
  do
    sample=${cond}${rep}
    mkdir -p alignments/${sample}
    cd alignments/${sample}
    truesight_pair.pl \
        -f ${RNA}/${sample}.1.fq ${RNA}/${sample}.2.fq \
        --bowtie-index ${IDX} \
        --thread 32 \
        --mismatch 2
    cd -
  done
done
