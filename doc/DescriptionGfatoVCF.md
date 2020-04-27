# Graphical Fragment Assembly (GFA) to Variant Call Format (VCF)

![](/figures/recapscript.png)

#### GFA to ODGI
The first step before run the script [GfatoVcf.py](/VGpop/GfatoVCF.py) is convert GFA format in ODGI format.

[Odgi](https://pangenome.github.io/odgi/index.html) is a tool that manipulate variation graphs, large graph without memory problem.

```
odgi build -g graph.gfa -o graph.odgi
```
By example:

odgi build -g [samplePath3.gfa](/data/SamplePath3.gfa) -o samplePath3.odgi

Obtained the odgi format, give it as _input to the script_. 

Description of script:

### 1. Dectection Bubbles

**Depth first Search (DFS)**

Depth first Search is a recursive algorithm for searching all the vertices of a graph or tree data structure.
This algorithm  mark each vertex as visited.

This works as follows:
- Start by placing one of the vertices of the graph in a stack.
- Take the item on top of the stack and add it to the list visited.
- Create a list of the adjacent nodes of that vertex. Add node that is not in the visited list.

_I'm starting to the graph and with this algorithm I explore it; as result I'm obtained a tree_.

**Breadth first Search (BFS)**

Breadth first Search is another recursive algorithm.

This works as follows:
- Start by putting any one of the graph's vertices at the back of a queue.
- Take the front item of the queue and add it to the visited list.
- Create a list of that vertex's adjacent nodes. Add the ones which aren't in the visited list to the back of the queue.

_I implemented this algorithm because to identify a bubble I need of distance from source from each node_. 

**Bubbles Calling**

A [bubble](https://www.sciencedirect.com/science/article/pii/S0304397515009147#br0100) consists of multiple directed unipaths from a vertex **v** to a vertex **u** and is commonly caused by a small number of errors in the centre of reads. It is format from a start and a end.

_From my script if distance is unique, I'm obtained start and end of bubbles. The center of the bubble is our ALT_. 

### 2. Variant Calling

**Possible paths**

Considering all the possible paths that connect the initial node and the final node of each bubble.                   
For each path chosen as REF, I check the alternates for that REF.

**SNV and INDEL**

Considering all the possible paths, the variants have been called, that is the nodes supported by at least one path, whose sequence is different from the sequence of the corresponding node in the reference considered.

For _Deletion_ if the considerate node in the REF is the current node in the current path, it means that in the current path a node is missing, so there is a deletion respect to the REF.

For _Insertion_ if the considerate node in the current path is the current node in the ref, it means that in the current path there is a node that is missing in the REF, that is an insertion. 

For _SNV_ if the sequence are different in the current path respect to the REF.

From samplepath3.odgi I get [sampleOutputpath3.vcf](/result/sampleOutputpath3.vcf).

From time to time, the path x is chosen as the REF and the other two are ALT, then y and z as the ref.

### 3. Validation VCF

I use [vg](https://github.com/vgteam/vg) tool for working with genome variation graphs for validate VCF obtained from GFA. 

For now to be able to validate VCF, the first path is the REF. In the next updates it will be possible to choose the reference path.
In the line 346 of the script, there is a **break**, uncommenting this, I chose as reference the first path and I obtained
[sampleOutputpath1.vcf](/result/sampleOutputpath1.vcf) for validation. 

From this I obtained the same graph that I use from start. 

```
./vg construct -v SampleOutputPath1.vcf.gz -r ref.fa > VcftoGraph.vg
./vg view -dp VcftoGraph.vg | dot -Tpdf -o ValidationGraph.pdf

```

![](/figures/Validation.png)

GFA | VCF
------------ | -------------
Path_name                   | CHROM
Lenght of sequence in a node| POS
Chose a path (or paths) from the beginning by recording sequences | REF
Sequence not present in REF, the center of bubble | ALT
SNV, INS, DEL | Type
 
*POS*, for example (NODE1 ATG) POS is 3 (lenght of sequence);
for (NODE2 AT) POS is 5 because is the sum of the length of the previous node sequence plus the current node lenght sequence.

Stay tuned for the add of script for calculate Allele Frequency and Fst on graph and for the implementation of this algorithm https://arxiv.org/pdf/1307.7925.pdf! :smile:
