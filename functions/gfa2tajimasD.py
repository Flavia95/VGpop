from itertools import combinations
from collections import Counter
import csv
import math
counter = Counter()

combinpath = []

#1. All possible combination of pairwise paths
#2. Obtain num_sequences (n.row-->numpath) and num_segregating_sites(n.column-->numvariationsites)  
with open('matrix.tsv', 'r') as f:
    paths = [l.strip() for l in f.readlines()]

    num_sequences = len(paths)
    num_segregating_sites = len(paths[0].split(','))
    for p in combinations(paths, 2):
        combinpath.append(p)

print("num_sequences:",num_sequences)
print("num_segregating_sites",num_segregating_sites)
print(combinpath)

#x,y
#x,z
#y,z

#3. Check differences between pairwise paths. 
#Continue if it finds a ","(because would be compared with another and would give true)

count = 0

for i in range(0, len(combinpath)):
    for j in range(0, len(combinpath[i][0])):
        if ',' in combinpath[i][1][j]:
            continue

#4.If values of combinationpaths are not the same, count the differences.

        if combinpath[i][0][j] == combinpath[i][1][j]:
            #print(combinpath[i][0][j], combinpath[i][1][j])
            print(True)
        else:
            count +=1
            print(False)

print("num_differences:",count)

#5.Define avg_num_pairwise_differences

avg_num_pairwise_differences = count/num_sequences
print("avg_num_pairwise_differences:",avg_num_pairwise_differences)

# 5.TajmasD

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
