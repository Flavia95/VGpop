ref_seq = ''
                                                                 #for more replicates
path_input = 'T3.seqgen'             #Input:2popwith40seq100rep
time = 'T3'

with open(path_input) as f:
    for num_rep, replicate in enumerate(f.read().split('\n ')):   #with for I read single file and with external loop read and split output in N replicate
        ref_seq = ''

        num_ref, len_seq = replicate.strip(' \n').split('\n')[0].split(' ')
        len_seq = int(len_seq)
        num_ref = int(num_ref) + 1

        num_to_seq_dict = {}
        for num_seq in replicate.strip(' \n').split('\n')[1:]:
            num, seq = num_seq.split('\t')
            num_to_seq_dict[int(num)] = seq

        if num_ref in num_to_seq_dict:
            ref_seq = seq

        #print(num_ref, len_seq, ref_seq)
        #print(num_to_seq_dict)

        if ref_seq == '':
            print('Replicate num. {} - no reference found!'.format(num_rep))
            continue

        ####################################################################################
        # VCF
        pos_to_individual_to_seq_dict = {}

        pos_with_at_least_one_variant_set = set()

        for pos, seq_in_ref in enumerate(ref_seq):
            pos_to_individual_to_seq_dict[pos] = {}

            for num, seq in num_to_seq_dict.items():
                if num != num_ref:
                    num_individual = int((num + 1) / 2)

                    if num_individual not in pos_to_individual_to_seq_dict[pos]:
                        pos_to_individual_to_seq_dict[pos][num_individual] = []

                    is_a_variant = seq[pos] != seq_in_ref
                    pos_to_individual_to_seq_dict[pos][num_individual].append(seq[pos])
                    if is_a_variant:
                        pos_with_at_least_one_variant_set.add(pos)

        if len(pos_with_at_least_one_variant_set) == 0:
            print('Replicate num. {} - no variants found!'.format(num_rep))
        else:
            individual_list = sorted(pos_to_individual_to_seq_dict[0].keys())

            # CREATE REFERENCE
            path_reference = 'seqgen.rep{}.{}.AncestralReference.fa'.format(num_rep, time)
            chrom = 'rep{}.{}.AncestralReference'.format(num_rep, time)
            with open(path_reference, 'w') as fw:
                fw.write('>{}\n{}\n'.format(chrom, ref_seq))
            print(path_reference + ' written')
            #--------

            pos_to_individual_to_seq_dict

            
            path_vcf = 'seqgen.rep{}.{}.vcf'.format(num_rep, time)
            with open(path_vcf, 'w') as fw:
                fw.write('##fileformat=VCFv4.2\n')
                fw.write('##fileDate=20200726\n')
                fw.write('##reference={}\n'.format(path_reference))
                fw.write('##contig=<ID=,length={}>\n'.format(chrom, len(ref_seq)))
                fw.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
                
                
                columns = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t' + '\t'.join(['Ind_{}'.format(ind) for ind in individual_list]) + '\n'

                fw.write(columns)

                for pos in sorted(pos_with_at_least_one_variant_set):
                    variants_set = set()
                    for num_individual in individual_list:
                        num = 2 * num_individual - 1

                        variants_set.update(
                            set([num_to_seq_dict[num][pos], num_to_seq_dict[num + 1][pos]]).difference(set(ref_seq[pos]))
                        )

                    ref_and_variants_list = [ref_seq[pos]] + sorted(variants_set)

                    genotype_list = []
                    for num_individual in individual_list:
                        num = 2 * num_individual - 1

                        genotype = [
                            str(ref_and_variants_list.index(num_to_seq_dict[num][pos])),
                            str(ref_and_variants_list.index(num_to_seq_dict[num+1][pos]))
                        ]
                        genotype_list.append('/'.join(sorted(genotype)))
                
                    fw.write('\t'.join([chrom, str(pos), '.', ref_seq[pos], ','.join(variants_set), '.', '.', '.', 'GT'] + genotype_list) + '\n')
            print(path_vcf + ' written')

        ####################################################################################

        ####################################################################################
        # GFA
        # The first step_id is the reference step id
        pos_to_step_ids_in_that_pos_dict = {}
            
        step_id_to_seq_dict = {}
        path_nodes_dict = {}

        path_nodes_dict['AncestralReference'] = []
        for step_id, nt in enumerate(ref_seq):
            step_id_to_seq_dict[step_id] = nt
            
            path_nodes_dict['AncestralReference'].append(str(step_id))
            
            pos_to_step_ids_in_that_pos_dict[step_id] = [step_id]
           

        last_step_id = step_id + 1

        links_to_write = ''  #for write output, define links, steps and paths
        steps_to_write = ''
        paths_to_write = ''

        stuff_already_seen = set()
        for num, seq in num_to_seq_dict.items():
            # If it is not the reference...
            if int(num) != num_ref:
                # ...find differences
                
                path_nodes_dict[num] = []
                last_chosen_node = -1
                for pos, (x, y) in enumerate(zip(ref_seq, seq)):
                    choosen_step_id = -1
                    if x == y:
                        choosen_step_id = pos_to_step_ids_in_that_pos_dict[pos][0] # The first step id is the reference step id
                    else:
                        for possible_step_id in pos_to_step_ids_in_that_pos_dict[pos]:
                            if step_id_to_seq_dict[possible_step_id] == y:
                                # Already available a node with the same sequence
                                choosen_step_id = possible_step_id
                                break
                        
                        if choosen_step_id == -1:
                            # I need to create a new step_id
                            step_id_to_seq_dict[last_step_id] = y
                            pos_to_step_ids_in_that_pos_dict[pos].append(last_step_id)
                            choosen_step_id = last_step_id
                        
                            last_step_id += 1
                    path_nodes_dict[num].append(str(choosen_step_id))
                    
                    # Links
                    if last_chosen_node != -1:
                        nodo_1 = last_chosen_node
                        nodo_2 = choosen_step_id
                        nodo_12 = str(nodo_1) + '_' + str(nodo_2)
                        if nodo_12 not in stuff_already_seen:
                            stuff_already_seen.add(nodo_12)
                            links_to_write += 'L\t' + str(nodo_1) + '\t+\t' + str(nodo_2) + '\t+\t0M\n'
                            
                    last_chosen_node = choosen_step_id
                    

                        
        for step_id, seq in step_id_to_seq_dict.items():
            #print('\t'.join(['S', str(step_id), seq]))
            steps_to_write += 'S\t'+ str(step_id) + '\t' + seq + '\n'
            

        for path, node_list in path_nodes_dict.items():
            paths_to_write += ('\t'.join(['P', str(path),'+,'.join(node_list) + '+', '\n']))

            
        
        path_gfa = 'seqgen.rep{}.{}.gfa'.format(num_rep, time)
        with open(path_gfa, 'w') as fw:
            fw.write('H\tVN:Z:1.0\n')    #add header
            fw.write(steps_to_write + paths_to_write + links_to_write)
        print(path_gfa + ' written')
        ####################################################################################
