from itertools import permutations
from collections import Counter
import csv
counter = Counter()

combinpath = []
c=0
field={}

#1. All possible combination of pairwise paths
with open('matrix.tsv', 'r') as f:
    paths = (l.strip() for l in f if l.strip())  
    for p in permutations(paths, 2):
        combinpath.append(p)

#2. Obtain num_sequences (n.row) and num_segregating_sites(n.column), edit it   
with open('matrix.tsv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        field[c]=row
        print(field[c])
        c=c+1

row=len (field[0])
column=len(field)

csvFile.close()

print("num_sequences:",row)
print("num_segregating_sites",column)
print(combinpath)
#x,y
#x,z
#y,x
#y,z
#z,x
#z,y

#3. Differences between pairwise path and count it. Index for list, tuple.
count = 0

for i in range(0, len(combinpath)-1): 
    for j, _ in enumerate(combinpath[i][0]):
        #print(combinpath[i][0][j], combinpath[i][1][j])
        if combinpath[i][0][j] == combinpath[i][1][j]:
            print(True)
        else:
            count +=1
            print(False)
            
print("num_differences:",count)

#4. Define avg_num_pairwise_differences

k = count/row
print("avg_num_pairwise_differences:",k)



#def _avg_num_pairwise_differences(num_differences,num_sequences):
    """
    Returns $k$ (Tajima 1983; Wakely 1996), calculated for a set of sequences:

    k = \frac{\right(\sum \sum \k_{ij}\left)}{n \choose 2}

    where $k_{ij}$ is the number of pairwise differences between the
    $i$th and $j$th sequence, and $n$ is the number of DNA sequences
    sampled.
    """
