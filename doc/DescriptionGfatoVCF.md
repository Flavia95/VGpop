# Graphical Fragment Assembly(GFA) to Variant Call Format(VCF)

![](/figures/RecapScript.png)

#### GFA to ODGI
The first step after run the script [GfatoVcf.py](/VGpop/GfatoVCF.py) is convert GFA format in ODGI format.
Odgi is a tool that manipulate variation graphs,large graph without memory problem.
https://pangenome.github.io/odgi/index.html

```
odgi build -g graph.gfa -o graph.odgi
```
Obtained the odgi format, give it as input to the script. 

Description of script:

### 1. Dectection Bubbles

**Depth first Search (DFS)**

Depth first Search is a recursive algorithm for searching all the vertices of a graph or tree data structure. The purpose of the algorithm is to mark each vertex as visited.

The DFS algorithm works as follows:
- Start by placing one of the vertices of the graph in a stack.
- Take the item on top of the stack and add it to the list visited.
- Create a list of the adjacent nodes of that vertex. Add node that is not in the visited list at the top of the stack.

I'm starting to the graph and with this algorithm I explore it; As result I'm obtained a tree.

**Breadth first Search(BFS)**

Breadth first Search is a recursive algorithm for searching all the vertices of a graph or tree data structure.

This algorithm works as follows:
- Start by putting any one of the graph's vertices at the back of a queue.
- Take the front item of the queue and add it to the visited list.
- Create a list of that vertex's adjacent nodes. Add the ones which aren't in the visited list to the back of the queue.

I implemented this algorithm because to identify a bubble I need of distance from source from each node. 

**Bubbles Calling**

A bubble consists of multiple directed unipaths from a vertex]**v** to a vertex **u** and is commonly caused by a small number of errors in the centre of reads. There have a start and a end.

From my script if distance is unique, I'm obtained start and end of bubbles. The center of the bubble is our ALT. 

### 2. Variant Calling

**Possible path**

Considering all the possible paths that connect the initial node and the final node of each bubble.                   
For each path chosen as REF, I check the alternates for that REF.

**SNV and INDEL**

Considering all the possible paths, the variants have been called, that is the nodes supported by at least one path, whose sequence is different from the sequence of the corresponding node in the reference considered.

For Deletion if the succ node in the ref is the current node in the current path, it means that. In the current path a node is missing, so there is a deletion respect to the REF.

For Insertion if the succ node in the current path is the current node in the ref, it means that. In the current path there is a node that is missing in the ref, that is an insertion. 

### 3. Validation VCF

I use vg tools for working with genome variation graphs for validate VCF obtained from GFA. 
From VCF obtained with script I obtained the same graph that I use from start. 

```
./vg construct -v gfatovcf.vcf.gz -r ref.fa > VcftoGraph.vg
./vg view -dp  VcfToGraph.vg | dot -Tpdf -o ValidationGraph.pdf

```

From [samplepath3.odgi](/data/samplepath3.odgi) I get [sampleOutputpath3.vcf](/result/sampleOutputpath3.vcf). Start from GFA in the VCF, CHROM is the name of path in the gfa, POS is the lenght of sequence (ex. Node1: CAG, NODE2: TA--> POS 3 and POS 3+ 2 = 5. REF: Chose a path present in GFA as ref, one or three,follow the path or paths selected at the beginning as a reference by recording the sequences. ALT: sequence not present in path, but it present in the centre of bubble.  
