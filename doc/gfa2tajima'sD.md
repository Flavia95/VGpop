[Tajima's-D](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1203831/pdf/ge1233585.pdf) is a population genetic test statistic, 
it is calculated as the difference between two measures of genetic diversity: the ***average number of pairwise differences*** and the ***number of segregation sites***, each scaled so that they are expected to be the same in an evolving neutral population of constant size. 

![D=\frac{d}{\sqrt{V(d)}](https://latex.codecogs.com/svg.latex?\Large&space;D=\frac{d}{\sqrt{V(d)})
![=\frac{K-\frac{S}{a_1)}}{\sqrt{a_1 S+e_2S(S-1)}}](https://latex.codecogs.com/svg.latex?\Large&space;=\frac{K-\frac{S}{a_1}}{\sqrt{e_1S+e_2S(S-1)}}) 

where: 

![](/figures/tajmad.png)

The first estimate is the average number of SNPs found in (n choose 2) pairwise comparisons of sequences (i,j) in the sample.

![](/figures/avgpairwisenumber.png)

The second estimate is derived from the expected value of S, the total number of polymorphisms in the sample

![E(S)={a_1}{{M}](https://latex.codecogs.com/svg.latex?\Large&space;E(S)={a_1}{{M})

where M could be calculate in two mode:

![M=\frac{S}{{(a_1)}](https://latex.codecogs.com/svg.latex?\Large&space;M=\frac{S}{{(a_1)})              

![M={4}{{Nu}](https://latex.codecogs.com/svg.latex?\Large&space;M={4}{{Nu})

#### Tajima's D on Variation Graph:

There are three essential element for calculate it:

*K*: average number pairwise differences.

*S*: number segregating sites.

*n*: number of sequences.

I'm starting from the output that derived from ***bubblepop***:

Paths         | bubble1        | bubble2        | bubble3
--------------| -------------  | -------------- |---------
pathx         | 0              | 1              | 0
pathy         | 0              | 1              | 1
pathz         | 1              | 0              | 0

Where:

1. [Number of sequences](/functions/utils.py#L9) is number of rows in a matrix i.e number of the paths in the VG.

2. [Number of segregation sites](/functions/utils.py#L15) number of the columns in a matrix i.e number of the variable sites in the VG.

3. [Count differences](doc/count_differences.md) on VG.

3. [Average number pairwise differences](/functions/utils.py#63): 

![\frac{count_differences}{{(num_sequences)}](https://latex.codecogs.com/svg.latex?\Large&space;\frac{count_differences}{{(num_sequences)})

  
 4. [Calculate Tajma's D](/function/statistics.py#14). 

![D=\frac{avepairwisediff-\frac{numsegrsites}{a_1)}}{\sqrt{a_1 S+e_2S(S-1)}}](https://latex.codecogs.com/svg.latex?\Large&space;D=\frac{avepairwisedif-\frac{numsegrsites}{a_1}}{\sqrt{e_1numsegrsites+e_2numsegrsites(numsegrsites-1)}})  
 


