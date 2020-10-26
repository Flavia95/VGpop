import math
import sys
sys.path.append("./functions")
import vgpop 
from vgpop import num_sequences
from vgpop import avg_num_pairwise_differences
from vgpop import num_segregating_sites

# 5.TajmasD

with open('matrix.tsv', 'r') as f:
    matrix = [l.strip() for l in f.readlines()]


def _tajimas_d(num_sequences, avg_num_pairwise_differences, num_segregating_sites):
    a1 = sum([1.0/i for i in range(1, num_sequences)])
    print(a1)
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
    #print(freqgeno(collections)) 
    #print(freqalle(collections))
    print(num_sequences(matrix))
    print(num_segregating_sites(matrix))
    print(avg_num_pairwise_differences(matrix))
    print(_tajimas_d(num_sequences(matrix), num_segregating_sites(matrix), avg_num_pairwise_differences(matrix))) 
   
    
    
if __name__ == "__main__":
    main()

    