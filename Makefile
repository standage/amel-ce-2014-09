#!/usr/bin/make -f
SHELL=bash

# TrueSight alignments in BAM format
controlbam=c1.bam c2.bam c3.bam c4.bam c5.bam c6.bam
treatmentbam=t1.bam t2.bam t3.bam t4.bam # t5.bam t6.bam
allbam=$(controlbam) $(treatmentbam)

# CE (cassette exon) events
#  - counts (# aligned reads spanning splice junctions)
#  - exon coverage
allce=$(patsubst %.bam,%.ce,$(allbam))
allce_cut=$(patsubst %.bam,%.ce.temp,$(allbam))
allcov=$(patsubst %.bam,%.exoncov,$(allbam))

.SECONDARY:				$(allce) $(allce_cut)


#--------------------------
# Calculating Pcount, Pcov,
# and combined probability
#--------------------------
amel-final.tsv:				amel-pcount.tsv padj_bh.py
					python padj_bh.py amel-pcount.tsv > amel-final.tsv

amel-pcount.tsv:			amel-pcov.tsv pcount.py
					python pcount.py < amel-pcov.tsv > amel-pcount.tsv

amel-pcov.tsv:				amel-ce-summed.tsv amel-exoncov.tsv pcov.py
					python pcov.py amel-exoncov.tsv < amel-ce-summed.tsv > amel-pcov.tsv


#----------------------------
# Reads aligning to junctions
#----------------------------
amel-ce-summed.tsv:			amel-ce.tsv
					echo $$'exon1-exon2:control\texon2-exon3:control\texon1-exon3:control\texon1-exon2:treatment\texon2-exon3:treatment\texon1-exon3:treatment' > junc-span-counts.tsv 
					#cut -f 6-  amel-ce.tsv | tail -n +2 | awk -v OFS=$$'\t' '{ print $$1+$$4+$$7+$$10+$$13+$$16,$$2+$$5+$$8+$$11+$$14+$$17,$$3+$$6+$$9+$$12+$$15+$$18,$$19+$$22+$$25+$$28+$$31+$$34,$$20+$$23+$$26+$$29+$$32+$$35,$$21+$$24+$$27+$$30+$$33+$$36 }' >> junc-span-counts.tsv
					cut -f 6-  amel-ce.tsv | tail -n +2 | awk -v OFS=$$'\t' '{ print $$1+$$4+$$7+$$10+$$13+$$16,$$2+$$5+$$8+$$11+$$14+$$17,$$3+$$6+$$9+$$12+$$15+$$18,$$19+$$22+$$25+$$28,$$20+$$23+$$26+$$29,$$21+$$24+$$27+$$30 }' >> junc-span-counts.tsv
					cut -f 1-5 amel-ce.tsv | head -n 1 | perl -ne 's/[ \t]+/\t/g; print' > amel-dmnt3-kd-ce.temp
					cut -f 1-5 amel-ce.tsv | tail -n +2 | awk -v OFS=$$'\t' '{ print $$1,$$2-1,$$3,$$4-1,$$5 }' >> amel-dmnt3-kd-ce.temp
					paste amel-dmnt3-kd-ce.temp junc-span-counts.tsv > amel-ce-summed.tsv
					rm junc-span-counts.tsv amel-dmnt3-kd-ce.temp

amel-ce.tsv:				$(allce_cut)
					paste <(echo -e "seqid\texon1_e\texon2_b\texon2_e\texon3_b" && cut -f 1-5 CE | perl -ne 's/[ \t]+/\t/g; print') $(allce_cut) >> amel-ce.tsv

%.ce.temp:				%.ce
					echo $$'$*:exon1-exon2\t$*:exon2-exon3\t$*:exon1-exon3' > $*.ce.temp
					cut -f 6- $*.ce | tail -n +2 >> $*.ce.temp

%.ce:					%.bam CE ce-counts.py
					which samtools
					samtools view $*.bam | python ce-counts.py CE $* > $*.ce

#--------------
# Exon coverage
#--------------
amel-exoncov.tsv:			$(allcov) cov-merge.py
					python cov-merge.py $(allcov) > amel-exoncov.tsv

%.exoncov:				amel-exons-ogs-plus.gff3 %.bam exon-cov.py
					which bedtools
					bedtools coverage -d -abam $*.bam -b amel-exons-ogs-plus.gff3 | python exon-cov.py > $*.exoncov

#------------
# Input files
#------------
amel-exons-ogs-plus.gff3:		amel_OGSv3.2.gff3 CE
					python exon-gff3.py amel_OGSv3.2.gff3 CE > amel-exons-ogs-plus.gff3

amel_OGSv3.2.gff3:			
					curl -O http://hymenopteragenome.org/beebase/sites/hymenopteragenome.org.beebase/files/data/consortium_data/amel_OGSv3.2.gff3.gz
					gunzip $@.gz

clean:					
					rm -f $(allce) $(allce_cut) $(allcov) amel_OGSv3.2.gff3 amel-exons-ogs-plus.gff3 amel-exoncov.tsv amel-ce.tsv amel-ce-summed.tsv amel-pcov.tsv amel-pcount.tsv
