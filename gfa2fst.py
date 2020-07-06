import statistics
#import matplotlib.pyplot as plt

#1. three different times of separation of two populations 
for T in ['1', '2', '3']:                        
    mean_fst_list = []
    for num_rep in range(0,99):                               
        print('Num. rep: ', num_rep)
        
#2. Open replicates from population1 and from population two
        f1 = open('t{}/allelfr_rep{}.pop1.tsv'.format(T, num_rep))    
        f2 = open('t{}/allelfr_rep{}.pop2.tsv'.format(T, num_rep))

        fst_list = []


        pos_set = set()
        pos_to_freq_pop1 = {}
        for line1 in f1:
            pos_pop1 = int(line1.strip('\n').split('\t')[0])
            lecter1 = line1.strip('\n').split('\t')[1]
            freq_pop1 = line1.strip('\n').split('\t')[-1]  
            
            if lecter1 == 'X' or freq_pop1 == 0 or freq_pop1 == 1:
                print(pos_pop1, lecter1, freq_pop1)
                continue

            if pos_pop1 not in pos_to_freq_pop1:
                pos_to_freq_pop1[pos_pop1] = []
            pos_to_freq_pop1[pos_pop1].append(float(freq_pop1))

            pos_set.add(pos_pop1)

        pos_to_freq_pop2 = {}
        for line2 in f2:
            pos_pop2 = int(line2.strip('\n').split('\t')[0])
            lecter2 = line2.strip('\n').split('\t')[1]
            freq_pop2 = line2.strip('\n').split('\t')[-1]  #ultima colonna

            if lecter2 == 'X' or freq_pop2 == 0 or freq_pop2 == 1:
                print(pos_pop2, lecter2, freq_pop2)
                continue

            if pos_pop2 not in pos_to_freq_pop2:
                pos_to_freq_pop2[pos_pop2] = []
            pos_to_freq_pop2[pos_pop2].append(float(freq_pop2))

            pos_set.add(pos_pop2)
        
        f1.close()
        f2.close()

        for pos in sorted(pos_set):
            if pos in pos_to_freq_pop1 and pos in pos_to_freq_pop2:
                if len(pos_to_freq_pop1[pos]) != 2 or len(pos_to_freq_pop2[pos]) != 2:
                    #print('Not biallelic site')
                    continue
                #print('pop1', pos, pos_to_freq_pop1[pos])
                #print('pop2', pos, pos_to_freq_pop2[pos])
                #print(freq_pop1)
                #print(freq_pop2)
                freq_pop1 = sorted(pos_to_freq_pop1[pos])[0]
                freq_pop2 = sorted(pos_to_freq_pop2[pos])[0]


                mean = statistics.mean([freq_pop1, freq_pop2])
                #print(mean)

                fst = statistics.pvariance([freq_pop1, freq_pop2])/((mean)*(1-mean))
                #print(freq_pop1, freq_pop2)
                
                fst_list.append(fst)

        if len(fst_list) == 0:
            #print(num_rep, 'missing values', fst_list)
            continue

        mean_fst_list.append(statistics.mean(fst_list))
        
    print('t{} <- c({})'.format(T, ','.join([str(x) for x in mean_fst_list])))