#!/usr/bin/env bash
set -e
set -o pipefail

for i in {1..4}
do
  cols=$(python shuff-6x6.py)
  echo Iteration $i: $cols
  sed "s/::COLS::/$cols/" Makefile.template > Makefile.wt.$i
  rm -f amel-ce-summed.tsv
  make -f Makefile.wt.$i > devnull 2>&1
  perl -ne '@v = split(/\t/); print if($v[15] < 0.01)' < amel-final.tsv | tail -n +2 | cut -f 1-5 | tr '\t' ',' | sort > sig.pt.$i
  wc -l sig.pt.$i
done
comm -12 <(comm -12 sig.pt.1 sig.pt.2) <(comm -12 sig.pt.3 sig.pt.4) | wc -l

for i in {1..4}
do
  cols=$(python shuff-3x3.py)
  echo Iteration $i: $cols
  sed "s/::COLS::/$cols/" Makefile.template > Makefile.wt.$i
  rm -f amel-ce-summed.tsv
  make -f Makefile.wt.$i > devnull 2>&1
  perl -ne '@v = split(/\t/); print if($v[15] < 0.01)' < amel-final.tsv | tail -n +2 | cut -f 1-5 | tr '\t' ',' | sort > sig.wt.$i
  wc -l sig.wt.$i
done
comm -12 <(comm -12 sig.wt.1 sig.wt.2) <(comm -12 sig.wt.3 sig.wt.4) | wc -l

for i in {1..4}
do
  cols=$(python shuff-3x3.py treatment)
  echo Iteration $i: $cols
  sed "s/::COLS::/$cols/" Makefile.template > Makefile.kd.$i
  rm -f amel-ce-summed.tsv
  make -f Makefile.kd.$i > devnull 2>&1
  perl -ne '@v = split(/\t/); print if($v[15] < 0.01)' < amel-final.tsv  | tail -n +2 | cut -f 1-5 | tr '\t' ',' | sort > sig.kd.$i
  wc -l sig.kd.$i
done
comm -12 <(comm -12 sig.kd.1 sig.kd.2) <(comm -12 sig.kd.3 sig.kd.4) | wc -l

for i in {1..4}
do
  colswt=$(python shuff-3x3.py | perl -ne '@v = split(/,/); printf "%s,%s,%s\n", $v[0], $v[1], $v[2]')
  colskd=$(python shuff-3x3.py treatment | perl -ne '@v = split(/,/); printf "%s,%s,%s\n", $v[0], $v[1], $v[2]')
  cols=${colswt},${colskd}
  echo Iteration $i: $cols
  sed "s/::COLS::/$cols/" Makefile.template > Makefile.wt-vs-kd.$i
  rm -f amel-ce-summed.tsv
  make -f Makefile.wt-vs-kd.$i > devnull 2>&1
  perl -ne '@v = split(/\t/); print if($v[15] < 0.01)' < amel-final.tsv  | tail -n +2 | cut -f 1-5 | tr '\t' ',' | sort > sig.wt-vs-kd.$i
  wc -l sig.wt-vs-kd.$i
done
comm -12 <(comm -12 sig.wt-vs-kd.1 sig.wt-vs-kd.2) <(comm -12 sig.wt-vs-kd.3 sig.wt-vs-kd.4) | wc -l
