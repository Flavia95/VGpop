library(tidyverse) 
library(grid)
library(gridExtra )
library(optparse)


#myd.table('chr19.info', header=F )
#bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%QUAL\t%AC\t%AF\n' -r chr19 -o chr19.info [relevantvcf] 
#usage Rscript af.R -i chr19.info


option_list = list(make_option(c("-i", "--input"), type="character", default=NULL, help="path to the input files", metavar="character"), 
		   make_option(c("-e", "--experiment"),  type="character", default="my experiment" , help = "name of the experiment", metavar="character" )  )
opt_parser=OptionParser(option_list=option_list)
opt=parse_args(opt_parser)

myd=read.table(opt$input, header=F, sep='\t' , comment.char='')
colnames(myd)=c('CHROM','POS','REF','ALT','QUAL','AC','AF')

p<- myd %>% select (CHROM, POS , AC) %>% separate_rows(AC , convert=T ) %>% group_by(CHROM, POS  )%>% summarise (ALTsum=sum(AC)) 
p1<- ggplot(p, aes(ALTsum ) )+geom_bar(aes(y=..prop..)) + theme_minimal()  + ggtitle(paste('counts ', opt$experiment , sep='-'))
p2<-  ggplot(p, aes(ALTsum ) )+geom_bar() + theme_minimal()   +xlim (0,20) + ggtitle(paste('counts ', opt$experiment , sep='-'))
p3<-  ggplot(p, aes(ALTsum ) )+geom_bar() + theme_minimal()   +xlim(50,300 ) +ggtitle (paste('counts ', opt$experiment , sep='-'))
p4<- ggplot(p, aes(ALTsum ) )+geom_bar() + theme_minimal()  + ggtitle(paste('counts ', opt$experiment , sep='-'))
g<-grid.arrange(p4, p1, p2, p3, nrow=4 )
ggsave('sfscounts.pdf', g  ) 


q<- myd %>% select (CHROM, POS , AF) %>% separate_rows(AF , convert=T ) %>% group_by(CHROM, POS  )%>% summarise (ALT_AF=sum(AF)) 
q1<- ggplot(q,  aes(ALT_AF) )+geom_histogram(bins=100) +theme_minimal() + ggtitle(paste( 'allele frequencies ' , opt$experiment, sep='-') ) 
ggsave('sfsfreq.pdf') 

