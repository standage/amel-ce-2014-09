# Differential splicing analysis workflow for skipped exons

25 Sept 2014, Daniel Standage <daniel.standage@gmail.com>.
Based on scripts by Yang Li <yangli8@illinois.edu>
and supplementary info at http://dx.doi.org/10.1073/pnas.1310735110

## Overview

Yang Li was kind enough to share some of the scripts he used to collect data for
Pcount calculations as described in the Supporting Information (supplement) of
[this recent PNAS paper](http://dx.doi.org/10.1073/pnas.1310735110). Although
the full Pcount calculation was not automated by these scripts, they provided
me enough of a starting point so that I could write a fully automated workflow
to do the calculation.

Based on the description in the paper supplement and some suggestions from Yang,
I also went on to automate calculation of Pcov, combined probabilities, and
final probabilities corrected for multiple testing. This workflow is implemented
as a Make file, which in turn utilizes a collection of Python scripts.

## Prerequisites

Running the complete workflow requires the following software.

- GNU Make
- Python (tested with Python 2.7)
- SciPy (tested with SciPy 0.12.1)
- rpy2 (tested with rpy2 2.4.3)
- samools (tested with samtools version 0.1.19+)
- bedtools (tested with bedtools version 2.20.1)

The workflow also relies on annotated CE events. Yang was kind enough to provide
this in the materials he sent (specifically the ``CE`` file), although he did
not include the scripts/programs used to produce the file.

## Running the workflow

Assuming all the software prerequisites are satisfied, the workflow can be run
simply by executing ``make``. If you have 32 processors available on your system
you'll probably want to execute the following command.

    make -j 32

It requires about 10 minutes to build the final output table ``amel-final.tsv``.
This does not include the most time-intensive steps, which are downloading the
RNA-seq data (see ``download.sh``) and running the alignments with TrueSight
(see ``truesight.sh``), which requires several days for this data set.

## A simple example
The main text of the dmnt3 knockdown paper listed above provides a single
example of a CE (cassette exon) event: gene GB53079 on scaffold 4.5. I used this
gene to test whether I had implemented to workflow correctly. Minimal Python
scripts in the ``example`` directory perform the calculations.

### Pcount
  The Pcount value for this CE event is calculated using the
  ``example/manual-pcount.py`` script, using junction-spanning read counts from
  the ``amel-ce.tsv`` file. While the counts calculated by workflow agree
  perfectly with the workflow provided by Yang (i.e. the ``BEE_CE_LIST`` file),
  neither of these agree with the numbers reported for this CE event in the
  paper.

  The contingency table for this CE event's Fisher's Exact Test is shown below.
  This test produces a p value of 0.00178.

|             |  Exon contained  |  Exon skipped  |
|:-----------:|:----------------:|:--------------:|
|   Control   |       208        |      546       |
|  Treatment  |       172        |      655       |

### Pcov
  The ES skipping ratio was calculated for each replicate using the
  ``example/manual-es-ratio.py`` script. These values were then used to
  calculate Pcov with the ``example/manual-pcov.py`` script. These values could
  not be confirmed since Yang provided no coverage data.

  The unpaired t test on control versus treatment skipping ratios produces a p
  value of 0.86865.

### Combined probability
  Pcov and Pcount were combined using Fisher's combined probability, as
  described in the PNAS supplement, using the
  ``example/manual-fisher-combined-p.py`` script.

  Fisher's method yields a chi square value of 12.944, which at 2k=4 degrees of
  freedom produces a p value of 0.01155.
