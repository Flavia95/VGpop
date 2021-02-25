### Description
[**vcflift.py**](VGpop/functions/vcflift.py) takes as input a chunk of a vcf file, a chunk of the reference sequence in fasta that covers the region in the vcf and adjust the chromosome positions to match the positions in the fasta. The vcf should have been generated from the same reference sequence from which the fasta is extracted. 

#### Usage 
vcflift.py -fasta pathToFastaFile -start startingPositionIntheReference -vcf vcfFile 

#### Example Usage 
testdata in enzac@penguin2:/home/enzac/data/vcfliftTestData

1. Decide which region you want to select. In the example I use chr19:3117753-3336924
2. Extract the fasta chunks from the reference sequence. I use: 

`bedtools getfasta -fi /home/davida/UCSC_mm10.fa -bed test.region.zerobased.bed  >  test.UCSC_mm10.zerobased.fa`  

Rememeber that bedtools 
 - is zerobased therefore the region in test.region.zerobased.bed is chr19:3117752-3336924 
 - requires a newline at the end of the single line in the bed file 

3. Extract the vcf chunks. I use: 

`tabix -h /data/DBA_2J_consensus_site_copy_hom_only_chr19_only.vcf.gz chr19:3117753-3336924 > test.vcf` 

4. Run vcflift.py: 

`vcflift.py -fasta test.UCSC_mm10.zerobased.fa -start 3117753 -vcf test.vcf  > lifted.test.vcf` 


 
