import re, argparse

def main(): 

    parser = argparse.ArgumentParser()
    parser.add_argument('-fasta',type=str, help='path to the fasta file', required=True)
    parser.add_argument('-start',type=str, help ='coordinate of the starting position ', required=True)
    parser.add_argument('-vcf',type=str, help ='path to the vcf ', required=True)
    args = parser.parse_args()

    seq=[]
    with open(args.fasta) as f:
        next(f)
        for line in f:
            seq.append(line.rstrip()) 

    with open(args.vcf) as g: 
        for vline in g: 
            if not re.match('#', vline): 
                x=vline.rstrip().split()
                pos=int(x[1]); newpos=pos-int(args.start)
                #uncomment to check correspondence between reference allele in vcf and fasta sequence 
                #print(x[:5],newpos, seq[0][newpos]) 
                x[1]=newpos
                print('\t'.join(map(str, x) ))
            else: print(vline.rstrip())

if __name__ == "__main__":
        main()
