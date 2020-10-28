import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-path',type=str, help='specific path where is lib odgi', required=True)
parser.add_argument('-input',type=str, help ='specific input as format gfa.odgi', required=True)
args = parser.parse_args()
sys.path.append(args.path)  

import odgi
g = odgi.graph()
g.load(args.input)

def process_step(s):
    h = g.get_handle_of_step(s)  #gets the handle (both node and orientation) of the step
    is_rev = g.get_is_reverse(h)
    id = g.get_id(h)
    return str(id) + ("+" if not is_rev else "-")

path_to_steps_dict = {}

def create_into_dict(path, step):       #dict with node_id as key and as value another dict that have as key name of path 
    path_name = g.get_path_name(path)
    if path_name not in path_to_steps_dict:
        path_to_steps_dict[path_name] = []
    path_to_steps_dict[path_name].append(process_step(step))

g.for_each_path_handle(
    lambda p:
        g.for_each_step_in_path(p, lambda s: create_into_dict(p, s))
)

node_id_to_path_and_pos_dict = {}
for path_name, steps_list in path_to_steps_dict.items():
    #print(path_name)

    pos = 0
    for nodeId_isRev in steps_list:
        node_id = int(nodeId_isRev[:-1])
        is_rev = nodeId_isRev[-1]
        
        node_handle = g.get_handle(node_id)
        seq = g.get_sequence(node_handle)
        
        if node_id not in node_id_to_path_and_pos_dict:
            node_id_to_path_and_pos_dict[node_id] = {}
        
        if path_name not in node_id_to_path_and_pos_dict[node_id]:
            node_id_to_path_and_pos_dict[node_id][path_name] = pos
        
        
        pos += len(seq)  #for each position add lenght of sequence 



for node_id in sorted(node_id_to_path_and_pos_dict.keys()):
    path_and_pos_dict = node_id_to_path_and_pos_dict[node_id]
    print('node_id:', node_id)
    
    for path, pos in path_and_pos_dict.items():
        print('path:', path,'- pos:', pos)

start_node = g.get_handle(1)   #root
g.get_id(start_node), g.get_sequence(start_node)  #id:seq

g_dfs = odgi.graph() # Array to keep track of visited nodes, DFS

def create_edge_and_so_on(handle1, handle2, so_on_function, *args):   #graph to tree 
    handle1_id = g.get_id(handle1)     
    handle2_id = g.get_id(handle2)
    if not g_dfs.has_node(handle2_id):   
        so_on_function(args[0])

        if not g_dfs.has_node(handle1_id):
            g_dfs.create_handle(
                g.get_sequence(handle1),
                handle1_id
            )

        if not g_dfs.has_node(handle2_id):
            g_dfs.create_handle(
                g.get_sequence(handle2),
                handle2_id
            )
        g_dfs.create_edge(handle1, handle2)
        #print('\tNew edge:', handle1_id, '-->', handle2_id) #create edge 

def dfs(node_id):
    current_node = g.get_handle(node_id)
    sequence_node = g.get_sequence(current_node)
    #print('current node_id:', node_id,'- sequence:', sequence_node)

    g.follow_edges(
        current_node,
        False,

        lambda neighbour:
            create_edge_and_so_on(                       #start from a node and explore 
                current_node, neighbour, dfs, g.get_id(neighbour)
            )
    )

import queue    #calculate distance from root with an implementation of BFS

def calculate_distance(visited_node_id_set, prev_node_id, neighbour_id, Q, distances_dict):
    if neighbour_id not in visited_node_id_set:
        #print('neighbour_id:', neighbour_id)

        # update distance for neighbour
        distances_dict[neighbour_id] = distances_dict[prev_node_id] + 1
        Q.put(neighbour_id)
        visited_node_id_set.add(neighbour_id)
        #print('queue:', list(Q.queue))
        #print('visited_node_id_set:', visited_node_id_set)
        #print()

def bfs_distances(graph, starting_node_id):
    visited_node_id_set = set()
    ordered_node_id_list = []

    # lambdas don't permit assignment
    distances_dict = {}
    node_id_list = []
    graph.for_each_handle(lambda h: node_id_list.append(graph.get_id(h)))
    for node_id in node_id_list:
        distances_dict[node_id] = 0
    node_id_list.clear()

    Q = queue.Queue()

    Q.put(starting_node_id)
    visited_node_id_set.add(starting_node_id) #start visit from starting node
    while not Q.empty():
        current_node_id = Q.get()
        current_node = g.get_handle(current_node_id)

        #print('current_node_id:', current_node_id)
        ordered_node_id_list.append(current_node_id)
        
        graph.follow_edges(
            current_node,
            False,

            lambda neighbour:
                calculate_distance(
                    visited_node_id_set, current_node_id, graph.get_id(neighbour), Q, distances_dict
                )
        )

    return distances_dict, ordered_node_id_list

dfs(1)

def show_edge(a, b):
    print(g_dfs.get_id(a), "-->", g_dfs.get_id(b))

def display_node_edges(h):           #consider only forward strand
    print("node", g_dfs.get_id(h))
    g_dfs.follow_edges(
        h, False,
        lambda n:
        show_edge(h, n))
    #g_dfs.follow_edges(
    #    h, True,
    #    lambda n:
    #    show_edge(n, h))
    
# displays all the edges twice, once for each of their ends
#print('\nDFS graph')
g_dfs.for_each_handle(display_node_edges)
#print()

distances_dict, ordered_node_id_list = bfs_distances(g_dfs, 1)

for node_id, distance in distances_dict.items():
    print(node_id, '- distance from root:', distance)

#print('ordered_node_id_lis:t', ordered_node_id_list)

dist_to_num_nodes = dict()    #if distance is unique it is already in a dict
for node_id, distance in distances_dict.items():
    if distance not in dist_to_num_nodes.keys():    #if distance not in the keys, put 0, if not add 1 
        dist_to_num_nodes[distance] = 0
    dist_to_num_nodes[distance] += 1

print('\nDistance from root --> Num. nodes')   #count distance 
for k, v in dist_to_num_nodes.items():
    print(k, '-->', v)

print('\nBubbles')
possible_bubbles_list = []
first_bubble = True
for node_id in ordered_node_id_list:        #for each distance, I enter using key distance
    key = distances_dict[node_id]
    if dist_to_num_nodes[key] == 1:     #if distance is unique print START
        if not first_bubble:
            print(node_id, 'END', node_id_to_path_and_pos_dict[node_id],g_dfs.get_sequence(g_dfs.get_handle(node_id)))
            possible_bubbles_list[-1][1] = node_id

        first_bubble = False
        print(node_id, 'START', node_id_to_path_and_pos_dict[node_id],g_dfs.get_sequence(g_dfs.get_handle(node_id)))
        possible_bubbles_list.append([node_id, -1])
    else:
        #print(get_sequence(node_id), 'sequence') 
        print(node_id, 'Bolla', node_id_to_path_and_pos_dict[node_id],g_dfs.get_sequence(g_dfs.get_handle(node_id)))

def print_all_paths_util(graph, u_node_id, d_node_id, visited_node_id_set, path_list, all_path_list):
    if u_node_id not in visited_node_id_set:
        visited_node_id_set.add(u_node_id)
        path_list.append(u_node_id)

        #print(u_node_id)
        if u_node_id == d_node_id:
            #print('Path:', path_list)
            all_path_list.append(path_list.copy())
        else:
            graph.follow_edges(
                graph.get_handle(u_node_id),
                False,

                lambda i_node:
                    print_all_paths_util(
                        graph, graph.get_id(i_node), d_node_id, visited_node_id_set, path_list, all_path_list
                    )
            )

        path_list.pop() 
        visited_node_id_set.remove(u_node_id)

def print_all_paths(graph, start_node_id, end_node_id, all_path_list):
    visited_node_id_set = set()

    path_list = []

    print_all_paths_util(graph, start_node_id, end_node_id, visited_node_id_set, path_list, all_path_list)



print('\n------------------')
