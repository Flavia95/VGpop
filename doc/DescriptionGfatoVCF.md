1) odgi build -g graph.gfa -o graph.og

DFS: I'm starting to the graph and with this algorithm I explore it; I'm obtained a tree.
Depth first traversal or Depth first Search is a recursive algorithm for searching all the vertices of a graph or tree data structure. The purpose of the algorithm is to mark each vertex as visited.

The DFS algorithm works as follows:
- Start by placing one of the vertices of the graph in a stack.\\
- Take the item on top of the stack and add it to the list visited.\\
- Create a list of the adjacent nodes of that vertex. Add node that is not in the visited list at the top of the stack



BFS:Breadth first Search is a recursive algorithm for searching all the vertices of a graph or tree data structure.
This algorithm works as follows:

-Start by putting any one of the graph's vertices at the back of a queue.\\
-Take the front item of the queue and add it to the visited list.\\
-Create a list of that vertex's adjacent nodes. Add the ones which aren't in the visited list to the back of the queue

I implement this algorithm for obtained distance from source from each node. 

Bubbles Calling: If distance is unique, I'm obtained start and end of bubbles. I'm interesting of the bubble, because it is the variable region of the sequence.
Variant Calling
Possible path: considering all the possible paths that connect the initial node and the final node of each bubble.
SNV, INDEL,DEL: considering all the possible paths, the variants have been called, that is the nodes supported by at least one path, whose sequence is different from the sequence of the corresponding node in the reference considered.

odgi build -g lil.gfa -o lil.odgi
PYTHONPATH=~/odgi/lib python3
import odgi
g = odgi.graph() 
g.load('file.odgi')


For convert GFA format in VCF the code is availabe on the git repository of the project 

I use vg tools for working with genome variation graphs for validate VCF obtained from GFA. 
Dal vcf ottenuto mediante l'algoritmo scritto ottengo lo stesso grafo usato come punto di partenza.
