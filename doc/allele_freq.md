**Allele frequency** is the relative frequency of an allele at a particular locus in a population.

![](/figures/allelefrequencies.png)

Allele        | A              | a
--------------| -------------  | -------------- 
Allele counts   |![n_A={7}](https://latex.codecogs.com/svg.latex?\Large&space;n_A={7)  |![n_a={13}](https://latex.codecogs.com/svg.latex?\Large&space;n_a={13)             
Allele Frequencies |![f_A=\frac{n_A}{{(2N)}](https://latex.codecogs.com/svg.latex?\Large&space;f_A=\frac{n_A}{{(2N)}) |![f_a=\frac{n_a}{{(2N)}](https://latex.codecogs.com/svg.latex?\Large&space;f_a=\frac{n_a}{{(2N)})            

![f_A={0.35}](https://latex.codecogs.com/svg.latex?\Large&space;f_A={0.35)

![f_a={0.65}](https://latex.codecogs.com/svg.latex?\Large&space;f_a={0.65) 

The allele frequency is the fraction of all the occurrences i of that allele and the total number of chromosome copies across the population.

**Allele frequencies on Variation Graph**:

I'm starting from the output that derived from ***bubblepop***:

Paths         | pos1        | pos2        | pos3
--------------| -------------  | -------------- |---------
pathx         | A              | T              | A
pathy         | A              | T              | T
pathz         | -              | -              | A

Where [number of sequences](/functions/utils.py#L9) is number of rows in a matrix and [number of segregation sites](/functions/utils.py#L15) number of the columns in a matrix.

1. For each row (sequence) I calculate number of occurences of allele, number of times an allele is found. 

2. For each row I calculate the sum of number of occurences.

3. Return [allele_freq](/functions/utils.py#L21)

![f_A=\frac{n_occurencesallele}{{(totalnumber)}](https://latex.codecogs.com/svg.latex?\Large&space;f_A=\frac{n_occurencesallele}{{(totalnumber)})
