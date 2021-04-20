library(grid)
library(gridExtra )                                                                                                                                                                                         
library(tidyverse)
library(optparse)

#myd=read.table('unmapped.133strains.list', header=F, sep='\t' , comment.char='') 
# usage Rscript unmappedinpafplot.R -i  unmapped.133strains.list

option_list = list(make_option(c("-i", "--input"), type="character", default=NULL, help="path to the input files", metavar="character") ) 
opt_parser=OptionParser(option_list=option_list) 
opt=parse_args(opt_parser) 

myd=read.table(opt$input, header=F, sep='\t' , comment.char='') 

colnames(myd)<- c("type", "sequence", "length", "Ns")
a<- tableGrob(myd %>% group_by(type) %>% tally() )
a1<-ggplot(myd , aes( length/1e6, fill=type  ) )  + geom_histogram ()+ facet_wrap(.  ~ type, scales="free_y")  + theme_minimal() +xlab ('length Mbp' )  +ggtitle ('Distribution of lengths')
a2<-ggplot(myd, aes( type, length, color=type  ) )  + geom_boxplot () + scale_y_log10() + theme_minimal() + ggtitle ('Length of the sequence') 
a3<-ggplot(myd, aes( type, Ns,  color=type  ) )  + geom_boxplot ()  + scale_y_log10()  + theme_minimal() + ggtitle('Number of Ns in the sequence' )

g<-grid.arrange(a, a1, a2, a3, nrow=4 )
ggsave(paste (opt$input, '.pdf', sep=''), g) 
