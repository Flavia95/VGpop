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

*K*: avgerage number pairwise differences.

*S*: number segregating sites.

*n*: number of sequences.

I'm starting from the output that derived from ***bubblepop***:

Paths         | bubble1        | bubble2        | bubble3
--------------| -------------  | -------------- |---------
pathx         | 0              | 1              | 0
pathy         | 0              | 1              | 1
pathz         | 1              | 0              | 0

1. Number of sequences: number of the paths in a graph, i.e number of rows in a matrix.
2. Number of segregation sites: number of the variable sites in a graph, i.e number of the columns in a matrix.

3.  Number of average number pairwise differences
     
   * With itertools I get all possible combination of paths as pairwise.
    
Combinations  | Value                  
--------------| -------------   
x,y           | ('0,1,0', '0,1,1')                            
x,z           | ('0,1,0', '1,0,0')                           
y,z           |  ('0,1,1', '1,0,0')

    
   * I check each tuple value with each next tuple value.If the value is the same I put True otherwise I put False. I count how many False there are, this is the number of differences as pairwise. For example--> x, y = (True, True, False)
   
   * Calculate average number pairwise differences (K): 

![\frac{numberofdifferences}{{(numberofsequences)}](https://latex.codecogs.com/svg.latex?\Large&space;\frac{numberofdifferences}{{(numberofsequences)})


    
 4. Calculate Tajma's D. 

![D=\frac{avepairwisediff-\frac{numsegrsites}{a_1)}}{\sqrt{a_1 S+e_2S(S-1)}}](https://latex.codecogs.com/svg.latex?\Large&space;D=\frac{avepairwisedif-\frac{numsegrsites}{a_1}}{\sqrt{e_1numsegrsites+e_2numsegrsites(numsegrsites-1)}})  
 


