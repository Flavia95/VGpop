import math
import sys 

##on VG
num_sequences=int(sys.argv[1])   ## number of diploid sequences~number of sequences in the number of paths
avg_num_pairwise_differences=float(sys.argv[2]) ## rows--> paths, column--> bubble, differences between pairwise of rows
num_segregating_sites=float(sys.argv[3])  ## number of bubbles where there are different alleles(there will be many bubble without differences in any paths, for instance any pair of nodes with only one edge between them) 

def _tajimas_d(num_sequences, avg_num_pairwise_differences, num_segregating_sites):

    a1 = sum([1.0/i for i in range(1, num_sequences)])
    a2 = sum([1.0/(i**2) for i in range(1, num_sequences)])
    b1 = float(num_sequences+1)/(3*(num_sequences-1))
    b2 = float(2 * ( (num_sequences**2) + num_sequences + 3 )) / (9*num_sequences*(num_sequences-1))
    c1 = b1 - 1.0/a1
    c2 = b2 - float(num_sequences+2)/(a1 * num_sequences) + float(a2)/(a1 ** 2)
    e1 = float(c1) / a1
    e2 = float(c2) / ((a1**2) + a2)

    D = (
        float(avg_num_pairwise_differences - (float(num_segregating_sites)/a1))
        / math.sqrt(
            (e1 * num_segregating_sites )
          + ((e2 * num_segregating_sites) * (num_segregating_sites-1) ))
        )
    return D

def main(): 

    print(_tajimas_d(num_sequences, avg_num_pairwise_differences, num_segregating_sites)) 

if __name__ == "__main__":
    main()
                   
