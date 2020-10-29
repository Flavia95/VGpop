The first step before run the script [GfatoVcf.py](/GfatoVcf.py) is convert GFA format in ODGI format.

[Odgi](https://pangenome.github.io/odgi/index.html) is a tool that manipulate variation graphs, large graph without memory problem.

```
odgi build -g graph.gfa -o graph.odgi
```
By example:

odgi build -g [samplePath3.gfa](/data/samplePath3.gfa) -o samplePath3.odgi

Obtained the odgi format, give it as _input to the script_. 

#### Description of the script

The main challenge  was to extract the information about variable sites (i.e. regions where more that one type of sequence is present) from the graphs. Any population genetic analysis is indeed based on the information contained in the variable segments of the sequence and their occurrence in the population under investigation. Because of their appearance in the pangenome graph, variable sites are referred to as bubbles.
The core of VGPOP is the bubblepop function, which takes as input a pangenome, detects bubbles, and outputs the sequences of the variants contained in the bubbles.

### Dectection Bubbles

**Depth first Search (DFS)**

[Depth first Search](https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/) is a recursive algorithm for searching all the vertices of a graph or tree data structure. DFS select an arbitrary node as root node and explores as far as possible along each branch. The exploration process runs until some depth cutoff is reached, and then DFS backtracks to the next most recently expanded node. Therefore, only the path of nodes from the initial node to the current node must be stored in order to execute the
algorithm. In bubblepop I use the DFS algorithm to explore the graph starting from a random node of the pangenome and as result I'm obtained a tree.

**Breadth first Search (BFS)**

[Breadth first Search](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/?ref=lbp) for traversing or searching tree or graph data structures. I used BFS on the tree obtained applying DFS. In bubblepop , I used BFS on the tree obtained by DFS. Starting from the tree root DFS explores the tree until it finds a bubble. When this happens it calculates the distance from the root of all the nodes in the bubbles and stores this information in a dictionary, i.e. a table of correspondence.  

**Bubbles Calling**

A [bubble](https://www.sciencedirect.com/science/article/pii/S0304397515009147#br0100) consists of multiple directed unipaths from a vertex **v** to a vertex **u** and is commonly caused by a small number of errors in the centre of reads. It is format from a start and a end.

Once the pangenome has been decomposed with bubblepop in a tree whose information on the node distance from the root is stored in dictionary.
Within the dictionary, the beginning and the end nodes of a bubbles are identified by the fact that their distance from the root is unique, i.e. they are the only nodes with specific distance from the root. All other nodes are inner nodes of bubbles and correspond to variable regions of the sequence. Furthermore nodes with the same distance from the root are in the same bubble.


![](/figures/bubblepop.png)

**Matrix**

As output we have a matrix, where the columns are the variants and the rows are the paths.

Paths           | bubble1       | bubble2
-------------- | ------------- | -------------- 
pathx         | A           | -
pathy         | A            | A
pathz         | T            | A

Number of the sequences: are the number of the paths (rows)

Number of the segregating sites: are the number of variants (columns)



