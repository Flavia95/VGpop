import math
#import dendropy
#from dendropy.calculate import probability
#from dendropy.calculate import combinatorics
import sys 

num_sequences=int(sys.argv[1])   ## number of diploid sequences  ~  half of the number of paths
avg_num_pairwise_differences=float(sys.argv[2]) ## 
num_segregating_sites=float(sys.argv[3])  ## number of bubbles 

def _tajimas_d(num_sequences, avg_num_pairwise_differences, num_segregating_sites):
    #num_sequences = 10
    #avg_num_pairwise_differences = 3.888889
    #num_segregating_sites = 16
    ###  for validation.: tajimas_d(10, 3.888889, 16) == -1.44617198561
    ###           a1 == 2.82896825397
    ###           a2 == 1.53976773117
    ###           b1 == 0.407407407407
    ###           b2 == 0.279012345679
    ###           c1 == 0.0539216450284
    ###           c2 == 0.0472267720013
    ###           e1 == 0.0190605338016
    ###           e2 == 0.0049489277699
    ###           D ==  -1.44617198561

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
                   