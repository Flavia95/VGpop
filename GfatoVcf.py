import sys
sys.path.append('/home/flavia/Lab/odgi/lib')  
import odgi
g = odgi.graph()
g.load("/home/flavia/Desktop/GfaToVcf/samplePath3.odgi")

def process_step(s):
    h = g.get_handle_of_step(s) # gets the handle (both node and orientation) of the step
    is_rev = g.get_is_reverse(h)
    id = g.get_id(h)
    return str(id) + ("+" if not is_rev else "-")

path_to_steps_dict = {}

def create_into_dict(path, step):       #dizionario nodo id come chiave e come valore un altro dizionario che ha come chiave il nome del path
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
        
        
        pos += len(seq)  #per ogni posizione aggiungimi la lunghezza della sequenza



for node_id in sorted(node_id_to_path_and_pos_dict.keys()):
    path_and_pos_dict = node_id_to_path_and_pos_dict[node_id]
    print('node_id:', node_id)
    
    for path, pos in path_and_pos_dict.items():
        print('path:', path,'- pos:', pos)

start_node = g.get_handle(1)   #radice
g.get_id(start_node), g.get_sequence(start_node)  #id:seq

g_dfs = odgi.graph() # Array to keep track of visited nodes

def create_edge_and_so_on(handle1, handle2, so_on_function, *args):   #albero con DFS
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
            create_edge_and_so_on(                       #partendo da un nodo vado ad esplorare il resto
                current_node, neighbour, dfs, g.get_id(neighbour)
            )
    )

import queue

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
    visited_node_id_set.add(starting_node_id) #parte dal nodo di start
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

def display_node_edges(h):
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

dist_to_num_nodes = dict()    #dizionario che ha distanza dalla radice ordinata, se distanza unique già è nel dizionario
for node_id, distance in distances_dict.items():
    if distance not in dist_to_num_nodes.keys():    #se la distanza non è tra le chiavi, metti 0, se già inizializzata aggiungi 1
        dist_to_num_nodes[distance] = 0
    dist_to_num_nodes[distance] += 1

print('\nDistance from root --> Num. nodes')   #conto distanze 
for k, v in dist_to_num_nodes.items():
    print(k, '-->', v)

print('\nBubbles')
possible_bubbles_list = []
first_bubble = True
for node_id in ordered_node_id_list:        #per ogni distanza nella lista di nodi ordinati, entra usando la chiave distanza
    key = distances_dict[node_id]
    if dist_to_num_nodes[key] == 1:  #se la distanza è univoca printa start altrimenti no
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


path_to_sequence_dict = {}
for path_name, steps_list in path_to_steps_dict.items():
    path_to_sequence_dict[path_name] = ''

    for node_id_rev in steps_list:
        path_to_sequence_dict[path_name] += g.get_sequence(g.get_handle(int(node_id_rev[:-1])))

stuff_to_alts_dict = {}
for current_ref in path_to_steps_dict.keys():
    # Remove the sign
    ref_path = [int(x[:-1]) for x in path_to_steps_dict[current_ref]]   

    for start, end in possible_bubbles_list[:-1]: # not the last element
        print('ref_path:', ref_path)
        print('Bubble [', start, ', ', end, ']')
        start_node_index_in_ref_path = ref_path.index(start)
        all_path_list = []
        print_all_paths(g, start, end, all_path_list)

        for path in all_path_list:
            print('\tPath:', path)
            pos_ref = node_id_to_path_and_pos_dict[start][current_ref]+1
            pos_path = pos_ref

            print('Start paths position:', pos_ref)

            max_index = min(len(path), len(ref_path))
            current_index_step_path, current_index_step_ref = (0, 0)
            for i in range(0, max_index):

                current_node_id_path = path[current_index_step_path]
                current_node_id_ref = ref_path[current_index_step_ref + start_node_index_in_ref_path]

                print(pos_ref, pos_path, '--->', current_node_id_ref, current_node_id_path)
                if current_node_id_ref == current_node_id_path:
                    print('REFERENCE')
                    node_seq = g.get_sequence(g.get_handle(current_node_id_ref))
                    pos_ref += len(node_seq)
                    pos_path = pos_ref

                    current_index_step_ref += 1
                    current_index_step_path += 1
                else:
                    succ_node_id_path = path[current_index_step_path + 1]
                    succ_node_id_ref = ref_path[current_index_step_ref + start_node_index_in_ref_path + 1]
                    if succ_node_id_ref == current_node_id_path:
                        print('DEL')
                        node_seq_ref = g.get_sequence(g.get_handle(current_node_id_ref))

                        prec_node_id_ref = ref_path[current_index_step_ref + start_node_index_in_ref_path - 1]
                        prec_nod_seq_ref = g.get_sequence(g.get_handle(prec_node_id_ref))
                        key = '_'.join([current_ref, str(pos_path - 1), prec_nod_seq_ref[-1] + node_seq_ref])
                        if key not in stuff_to_alts_dict:
                            stuff_to_alts_dict[key] = set()
                        stuff_to_alts_dict[key].add(prec_nod_seq_ref[-1] + '_del')

                        pos_ref += len(node_seq_ref)

                        current_index_step_ref += 1
                        current_node_id_ref = ref_path[current_index_step_ref + start_node_index_in_ref_path -1]
                        print('\t', current_node_id_ref)
                        continue
                    elif succ_node_id_path == current_node_id_ref:
                        print('INS')
                        node_seq_path = g.get_sequence(g.get_handle(current_node_id_path))

                        prec_node_id_ref = ref_path[current_index_step_ref + start_node_index_in_ref_path-1]
                        prec_nod_seq_ref = g.get_sequence(g.get_handle(prec_node_id_ref))
                        key = '_'.join([current_ref, str(pos_ref-1), prec_nod_seq_ref[-1]])
                        if key not in stuff_to_alts_dict:
                            stuff_to_alts_dict[key] = set()
                        stuff_to_alts_dict[key].add(prec_nod_seq_ref[-1] + node_seq_path + '_ins')

                        pos_path += len(node_seq_path)

                        current_index_step_path += 1
                        current_node_id_path = path[current_index_step_path]
                        print('\t', current_node_id_path)
                        continue
                    else:
                        node_seq_ref = g.get_sequence(g.get_handle(current_node_id_ref))
                        node_seq_path = g.get_sequence(g.get_handle(current_node_id_path))

                        if node_seq_ref == node_seq_path:
                            print('REFERENCE')
                        else:
                            print('SNV')

                        key = '_'.join([current_ref, str(pos_path), node_seq_ref])
                        if key not in stuff_to_alts_dict:
                            stuff_to_alts_dict[key] = set()
                        stuff_to_alts_dict[key].add(node_seq_path + '_snv')

                        pos_ref += len(node_seq_ref)
                        pos_path += len(node_seq_path)
                        current_index_step_ref += 1
                        current_index_step_path += 1

            print('---')        
        #all_path_list.append(path_name,g.get_sequence(g.get_handle(node_id)))
        #print(u_node_id)
        print('==========================================')
    
        

    break  #per avere solo un path



vcf_list = []
for chrom_pos_ref, alt_type_set in stuff_to_alts_dict.items():
    chrom, pos, ref = chrom_pos_ref.split('_')
    alt_list = [x.split('_')[0] for x in alt_type_set]
    type_ = set([x.split('_')[1] for x in alt_type_set])
    vcf_list.append([chrom, pos, '.', ref, ','.join(alt_list), '.', '.', 'TYPE=' + ';TYPE='.join(type_), 'GT', '0|1'])

vcf_list = sorted(vcf_list, key=lambda x: (x[0], int(x[1])), reverse=False)

import time

with open('sample.vcf', 'w') as fw:
    fw.write('##fileformat=VCFv4.2\n')
    fw.write('##fileDate=' + time.strftime("%Y%m%d") + '\n')   #genera la data di generazione nel vcf automaticamente
    fw.write('##reference=x.fa\n')
    fw.write('##reference=y.fa\n')
    fw.write('##reference=z.fa\n')
    fw.write('##commandline=gfa2vcf.py --input-gfa g.odgi\n')
    fw.write('##INFO=<ID=TYPE,Number=A,Type=String,Description="Type of each allele (snv, ins, del, mnp, complex)">\n')
    fw.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    fw.write('\t'.join(['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SampleName']) + '\n')
    fw.write('\n'.join(['\t'.join(row) for row in vcf_list]) + '\n')
