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
gene to test whether I had implemented to workflow correctly. A minimal Python
script ``example.py`` performs the calculations.

### Pcount
  The Pcount value is calculated using junction-spanning read counts from the
  ``amel-ce.tsv`` file. While the counts calculated by workflow agree perfectly
  with the workflow provided by Yang (i.e. the ``BEE_CE_LIST`` file), neither of
  these agree with the numbers reported for this CE event in the paper.

  The contingency table for this CE event's Fisher's Exact Test is shown below.
  This test produces a p value of 0.00287.

|             |  Exon contained  |  Exon skipped  |
|:-----------:|:----------------:|:--------------:|
|   Control   |       208        |      546       |
|  Treatment  |       218        |      801       |

  **Update**: Yang has confirmed that the numbers reported in the paper
  correspond to a single control and a single treatment. The Fisher's Exact Test
  for the numbers reported in the paper produces a p value of 0.09288.

### Pcov
  The ES skipping ratios for this example are calculated using the
  ``es-ratio.py`` script, and these ratios are then used to calculate Pcov.

  The unpaired t test on control versus treatment skipping ratios produces a p
  value of 0.74836. No Pcov calculations are provided for the example in the
  paper, so no comparison with the published data is possible.

### Combined probability
  Pcov and Pcount were combined using Fisher's combined probability, as
  described in the supplement.

  Fisher's method yields a chi square value of 12.287, which at 2k=4 degrees of
  freedom produces a p value of 0.01534. Again, these values are not provided
  for the example in the paper, so no comparison with the published result is
  possible.

## Results

The ``amel-final.tsv`` file contains a table with all of the read counts (summed
across replicates), Pcov values, Pcount values, combined probabilities, and
probabilities adjusted for multiple testing (see the table headers). Simple
shell commands can determine how many events are significant (at a particular
threshold) and which events those are.

```bash
# How many skipped exon events are significant?
perl -ne '@v = split(/\t/); print if($v[14] < 0.01)' < amel-final.tsv | wc -l

# Store significant events in a separate table
perl -ne '@v = split(/\t/); print if($v[14] < 0.01)' < amel-final.tsv \
    > amel-final-sig-01.tsv
```

Using the methods described herein, we determine 35 skipped/cassette exon events
to be significant at a FDR of < 0.01, many fewer than the 192 events reported in
the dmnt3 knockdown paper.

## Discussion

- The ``CE`` file provided by Yang annotates CE events by listing the start and
  end coordinates of the skipped exon, as well as the closest nucleotide of each
  flanking exon. Using the OGS 3.2, this describes a single unambiguous set of 3
  exons, the middle of which is alternatively skipped. However, in some cases
  the description matches multiple potential flanking exons, and in some cases
  the description fails to provide a match for one or both of the flanking
  exons. These missing exons were probably found using the method described in
  the TrueSight supplement (improving the GLEAN annotation), but neither the
  improved annotation nor the code used to generate it has been made available.
  Regarding CE events with multiple potential combinations of flanking exons,
  handling of this case was not described in the dmnt3 knockdown paper or its
  supplement, so for now I have ignored these cases. This may explain some of
  the discrepancy between the results I describe here and those reported in the
  published paper.
- I have a concern about normalization for library size (or the lack thereof)
  for some of these calculations. It seems reasonable that library size need not
  be taken into account for Pcov calculations, since these are based on coverage
  ratios of adjacent exons within a replicate. However, the Pcount values are
  calculated from raw read counts aggregated over all replicates. Without
  normalizing for library size, it seems impossible to discriminate whether
  higher read counts are the result of higher expression or higher sequencing
  depth.
