from itertools import combinations
from collections import Counter
import collections

with open('matrix.tsv', 'r') as f:
    matrix = [l.strip() for l in f.readlines()]

#1. Return the rows of the matrix (paths=sequences of the VG).
def num_sequences(matrix):
	num_sequences = len(matrix)

	return num_sequences

#2. Return the columns of matrix (polymorphic sites of the VG).
def num_segregating_sites(matrix):
    num_segregating_sites = len(matrix[0].split(','))

    return num_segregating_sites

#3. Return allele frequencies.
def freqalle(matrix,collections):
    allelfreq = []
    for line in matrix:
        no_comma = []
        for c in line:
            if c == ',':
                continue
            no_comma.append(c)
        
        occurrences = collections.Counter(no_comma)
        numerotot = (sum(occurrences.values()))

        for key, value in occurrences.items():
            allelfreq.append(value/numerotot)
    return allelfreq


#4. Returns total number of pairwise differences observed between all sequences.
def count_differences(matrix):
    counter = Counter()
    combinpath = []

    for p in combinations(matrix, 2):
        combinpath.append(p)

    count = 0

    for i in range(0, len(combinpath)):
        for j in range(0, len(combinpath[i][0])):
            if ',' in combinpath[i][1][j]:
                continue

            if combinpath[i][0][j] == combinpath[i][1][j]:
                #print(combinpath[i][0][j], combinpath[i][1][j])
                print(True)
            else:
                count +=1
                #print(False)    

    return count


#5. Return the number of pairwise differences between the sequences and the number of DNA sequences sampled.
def avg_num_pairwise_differences(matrix):
    avg_num_pairwise_differences = count_differences(matrix)/num_sequences(matrix)
    return avg_num_pairwise_differences
