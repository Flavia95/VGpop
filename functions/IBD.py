#0. Windows: tutti i paths e tipo lunghezza 100, (o/e righe intere ma tot path ala volta?)
#1. minlenseed: definisce l'operatore la lunghezza del segmento, tipo 2 cM (ossia 2 milioni di paia di basi)
#2. seedIBS: segmento che supera la lunghezza del minseed (> 2 cM)

#3. IBS si estende se ci sono due segmenti IBS separati da un gap per una coppia di aplotipi
#4. Estensione può avvenire più volte, fin quando la lunghezza in cM è maggiore di un valore di default presente nel file di output. 

import itertools
#1. Define len windows(N nucleotides) and lenminimumsegment (ex 2cM)
first_nt = 0
last_nt = 3

lenmin = 2
pairwise = []

with open('matrix.tsv', 'r') as f:
    f.readline()
    
    list_of_2tuples = [(line[2:].strip(), ','.join(f.readline().strip().split(',')[1:])) for line in f]
 
#2.Window   
    c = 0
    for i, (x, y) in enumerate(list_of_2tuples):
        if i >= first_nt and i <= last_nt:
            if x == y:
                c = c + 1
            print(x,y)

#3. Work with paths in pairs, if lenofseedIBS is major of lenmin it is an IBS segment
for (line1,line2) in list_of_2tuples: 
    if len (line1) and len(line2) > lenmin:
        IBS = (line1,line2)
        print('seedIBS(> of lenmin):',IBS)
    else:
        print('noseedIBS:', IBS)

    pairwise.append(IBS)

#3. I compare each nucleotide of each pair of path, if are equal T else F
ls = []

for i in range(0, len(pairwise)):
        for j in range(0, len(pairwise[i][0])):
            if ',' in pairwise[i][1][j]:
                continue

            if pairwise[i][0][j] == pairwise[i][1][j]:
                ls.append(True)
               
            else:
                ls.append(False)
        
print('T if nucleotides are equal else F:',ls)

#4. Define IBD: nucleotides equal for two paths as pair, if the number of true is equal to the len of paths or IBD and corrispondente nucleotide

c = (list(zip(*([iter(ls)] * 3))))
for i in c:
  print(i)

  s = 0
  for x in i:
    if x:
      s = s + 1
    else:
      s = 0

  if s >= (len(pairwise)+1):
    print('Segment IBD, where there are', s, 'True:', line2)