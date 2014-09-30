#!/usr/bin/env bash
set -e

URL=http://gremlin2.soic.indiana.edu/~standage/amel-dmnt3-alignments
for cond in c t
do
  for rep in {1..6}
  do
    sample=${cond}${rep}
    curl -O ${URL}/${sample}.bam
  done
done
