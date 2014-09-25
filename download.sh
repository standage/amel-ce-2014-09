#!/usr/bin/env bash
set -e
SRA=ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR893
which fastq-dump

# Download all 12 libraries (serially)
for i in {21..44}
do
  curl -O $SRA/SRR8930${i}/SRR8930${i}.sra
done

# Convert all 12 libraries to Fastq format (in parallel)
for i in {21..44}
do
  fastq-dump --split-files SRR8930${i}.sra &
done
wait

# Rename controls
# 112c=c1, 114c=c2, 115c=c3, 131c=c4, 136c=c5, 138c=c6
for i in {21..32}
do
  j=$(($i - 20))
  k=$(($i % 2))
  l=$((1 - $k))
  rep=$((1 + ($j / 2) - $l))
  sample=c$rep
  cat SRR8930${i}_1.fastq >> ${sample}.1.fq
  cat SRR8930${i}_2.fastq >> ${sample}.2.fq
done

# Rename treatments (dmnt3 knockdowns)
# 187t=t1, 196t=t2, 198t=t3, 205t=t4, 212t=t5, 214t=t6
for i in {33..44}
do
  j=$(($i - 32))
  k=$(($i % 2))
  l=$((1 - $k))
  rep=$((1 + ($j / 2) - $l))
  sample=t$rep
  cat SRR8930${i}_1.fastq >> ${sample}.1.fq
  cat SRR8930${i}_2.fastq >> ${sample}.2.fq
done

