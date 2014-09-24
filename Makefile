SHELL=bash

amel-final.txt:				amel-fisher.txt padj_bh.py
					python padj_bh.py amel-fisher.txt > amel-final.txt

amel-fisher.txt:			amel-pcov.txt pcount.py
					python pcount.py < amel-pcov.txt > amel-fisher.txt

amel-pcov.txt:				dmnt3-kd-juncspancounts.txt pcov.py
					python pcov.py amel-exoncov.txt < dmnt3-kd-juncspancounts.txt > amel-pcov.txt

coverage:				c1.exoncov c2.exoncov c3.exoncov c4.exoncov c5.exoncov c6.exoncov t1.exoncov t2.exoncov t3.exoncov
					

dmnt3-kd-juncspancounts.txt:		BEE_CE_LIST
					echo $$'exon1-exon2:control\texon2-exon3:control\texon1-exon3:control\texon1-exon2:treatment\texon2-exon3:treatment\texon1-exon3:treatment' > junc-span-counts.txt 
					cut -f 6- BEE_CE_LIST | tail -n +2 | awk -v OFS=$$'\t' '{ print $$1+$$4+$$7+$$10+$$13+$$16,$$2+$$5+$$8+$$11+$$14+$$17,$$3+$$6+$$9+$$12+$$15+$$18,$$19+$$22+$$25,$$20+$$23+$$26,$$21+$$24+$$27 }' >> junc-span-counts.txt
					cut -f 1-5 BEE_CE_LIST | head -n 1 | perl -ne 's/[ \t]+/\t/g; print' > BEE_CE_LIST.info
					cut -f 1-5 BEE_CE_LIST | tail -n +2 | awk -v OFS=$$'\t' '{ print $$1,$$2-1,$$3,$$4-1,$$5 }' >> BEE_CE_LIST.info
					paste BEE_CE_LIST.info junc-span-counts.txt > dmnt3-kd-juncspancounts.txt
					rm junc-span-counts.txt BEE_CE_LIST.info

BEE_CE_LIST:				c1.bam c2.bam c3.bam c4.bam c5.bam c6.bam t1.exoncov t2.exoncov t3.exoncov pre.list CE work.pl
					perl work.pl pre.list

%.exoncov:				amel-exons-ogs-plus.gff3 %.bam exon-cov.py
					which bedtools
					bedtools coverage -d -abam $*.bam -b $< | python exon-cov.py > $@

amel-exons-ogs-plus.gff3:		amel_OGSv3.2.gff3 CE
					python exon-gff3.py $^ > $@

amel_OGSv3.2.gff3:			
					curl -O http://hymenopteragenome.org/beebase/sites/hymenopteragenome.org.beebase/files/data/consortium_data/amel_OGSv3.2.gff3.gz
					gunzip $@.gz
