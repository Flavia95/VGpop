
I'm starting from the output that derived from ***bubblepop***:

Paths         | pos1        | pos2        | pos3
--------------| -------------  | -------------- |---------
pathx         | A              | T              | A
pathy         | A              | T              | T
pathz         | -              | -              | A

Where [number of sequences](/functions/utils.py#L9) is number of rows in a matrix and [number of segregation sites](/functions/utils.py#L15) number of the columns in a matrix.
The next step is calculate the total number of pairwise differences observed between all sequences.

***Total number of paiwise differences on VG***:

1. With itertools I get all possible combination of paths as pairwise.
    
Combinations  | Value                  
--------------| -------------   
x,y           | ('A,T,A', 'A,T,T')                            
x,z           | ('A,T,A', '-,-,A')                           
y,z           | ('A,T,T', '-,-,A')

2. I check each tuple value with each next tuple value. If the value is the same I put True otherwise I put *False*. 

3. [Count_differences](/functions/utils.py#L39) is: count how many False there are, there is the number of differences as pairwise.
For example--> x, y = (True, True, False), count of false is 1.
