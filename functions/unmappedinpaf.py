import os 
import argparse
#import matplotlib.pyplot as plt
"""
check for unmapped supernova contigs in a paf file. take as input a paf file and a folder with the stats obtained by Flavia  
"""

parser = argparse.ArgumentParser()
parser.add_argument('-pafPath',type=str, help= 'path to the paf file  where is lib odgi', required=True)
parser.add_argument('-contigsDirPath',type=str, help ='path to the folder with contig stats ', required=True)
args = parser.parse_args()

#pafpath='/home/flaviav/git/pggb/133strains/chr19.pan+ref.fa.pggb-W-s10000-l50000-p95-n20-a0-K16.paf'  #path to the  paf file 
#contigsDirPath='/home/enzac/data/contigsAndPaf/teststat'  #folder with stats from contings 

#paf 
contigsinpaf=[]
for line in open (args.pafPath ): 
    x=line.split() 
    contigsinpaf.append(x[0])
    contigsinpaf.append(x[5])

d_allcontigs={}
for contigsfile in os.listdir(args.contigsDirPath):
    with open('%s/%s' %(args.contigsDirPath, contigsfile)) as f:
        allcontigs = f.readlines()[2:]
        f.close() 
        #print (allcontigs)
        for a in allcontigs: 
            contig=a.rstrip().split(',')[0].split('\t')[0]
            lenseq=a.rstrip().split(',')[-1].split(':')[1]
            ns=a.rstrip().split(',')[-2].split('=')[1]
            d_allcontigs[contig]=[lenseq, ns]
#print (d_allcontigs) 
#print (d_allcontigs.keys())
#df_allcontigs = pd.DataFrame (d_allcontigs)

unmapped=set(d_allcontigs.keys()).difference(set(contigsinpaf))
mapped=set(d_allcontigs.keys()) & set(contigsinpaf)
for i in unmapped: print( '\t'.join(map (str, ['unmapped',i]+ d_allcontigs[i])))  
for i in mapped: print( '\t'.join(map (str, ['mapped',i]+ d_allcontigs[i])))  

#fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
    

