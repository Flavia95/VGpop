from collections import Counter
path_node_id = {}
step_node_id = {}
path_id_ref = ''
pops_to_haplotypes_dict = {}

#Calcolo Frequenze Genotipiche

#1.Load metadata for calculate info of tree leaves and dict (key:num_pop and value:num_haplo)
with open('metadata280pop.tsv', 'r') as f:
    f.readline()

    for line in f:
        num_pop, num_haplo = line.strip('\n').split('\t')
        if num_pop not in pops_to_haplotypes_dict.keys():
            pops_to_haplotypes_dict[num_pop] = []
        pops_to_haplotypes_dict[num_pop].append(num_haplo)
    #print(pops_to_haplotypes_dict)

#2.Load rep {range of rep} from SeqgeneToGfa and mantain info of pathid and stepid (from line that start with Path) and id and seq (from line that start with Seq)

for num_rep in range(3,4):
    print('Num.replicate:', num_rep)

with open("rep3.seq.gfa","r") as f:
    for line in f:
        line_list = line.strip('\t').split('\t') 
        if line.startswith('P'):
            path_node_id[line_list[1]] = [x.strip('+') for x in line_list[2].strip('\n').split(',')]   #pathid and stepid
            
            if 'ref' in line_list[1].lower():
                path_id_ref = line_list[1]
        elif line.startswith('S'):
            step_node_id[line_list[1]] = line_list[2].strip('\n')    #id and seq  

#3.Info for number of populations
for num_pop, individual_haplotypes_list in pops_to_haplotypes_dict.items():
    print('Population num.', num_pop)

    triall_dict = {}

#Diploid_individuals

    num_diploid_individuals = len(individual_haplotypes_list) / 2

    for pos in range(len(path_node_id[path_id_ref])):
        tmp_seq_in_pos_list = []
        
        it = iter(individual_haplotypes_list)
        for path_id_haplo_1 in it:
            path_id_haplo_2 = next(it)

            seq_current_step = ''.join(
                sorted([step_node_id[path_node_id[path_id_haplo_1][pos]], step_node_id[path_node_id[path_id_haplo_2][pos]]])
            )
            #print('\t' + path_id_haplo_1, path_id_haplo_2, seq_current_step)
            tmp_seq_in_pos_list.append(seq_current_step)

        #print('\tPos', pos, '- sequences in this pos', tmp_seq_in_pos_list)
        ATCG_counts_dict = Counter(tmp_seq_in_pos_list)
        #print('\tPos', pos, '- ', ATCG_counts_dict)   #I put delete it, is not necessary

        for nt_nt, count in ATCG_counts_dict.items():
            if count/num_diploid_individuals != 1:        #print AlleleFrequency if different of 1
                if pos not in triall_dict.keys():
                    triall_dict[pos] = {}
                triall_dict[pos][nt_nt] = count/num_diploid_individuals                       

#5. Write file tsv that contains genotype frequencies for each population and write two file, one for population
    with open('genofreq_rep{}.pop{}.tsv'.format(num_rep,num_pop),'w') as fw:
        for pos, nt_nt_freq_dict in triall_dict.items():
            for nt_nt, freq in nt_nt_freq_dict.items():
                fw.write(str(pos) + '\t' + nt_nt + '\t' + str(freq) + '\n')
