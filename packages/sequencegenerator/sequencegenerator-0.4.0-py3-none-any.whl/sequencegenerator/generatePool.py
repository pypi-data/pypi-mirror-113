import math
import random
from IUPACController import createMutationMap
from IUPACController import initialMutation
from IUPACController import mutateSequence


from Bio.SeqUtils import GC
from Bio.SeqUtils import MeltingTemp as mt

NUCLEOTIDES = ['A','T','C','G']

def get_random_sequence(length):
    my_inital_seq = ''
    for i in range(40):
        my_inital_seq+=random.sample(set('ATCG'),1)[0]
    return my_inital_seq

def reverse_seq(string):
    return string[::-1]

def compliment(string):
    new_string = ''
    for letter in string:
        if letter == 'A':
            new_string+='T'
        if letter == 'T':
            new_string+='A'
        if letter == 'C':
            new_string+='G'
        if letter == 'G':
            new_string+='C'
    return new_string

def calculate_inverted_repeats(my_inital_seq, minimum_repeat_length):
    inverted_repeat_match_counter = 0
    max_possible_overlap = math.floor(len(my_inital_seq) / 2) - 1
    for i in range(minimum_repeat_length,max_possible_overlap+1):
        for start_position in range(len(my_inital_seq)-((i)+(i-1))):
            inverted_repeat_to_test_downstream = compliment(reverse_seq(my_inital_seq[start_position:start_position+i]))
            downstream_seq = my_inital_seq[start_position+i:]
            if inverted_repeat_to_test_downstream in downstream_seq:
                inverted_repeat_match_counter+=1
    return inverted_repeat_match_counter

def calculate_gc_deviation(my_initial_seq):
    return (50 - GC(my_initial_seq))**2

def TM_deviance(my_initial_seq):
    return (60 - mt.Tm_NN(my_initial_seq))**2

def score(sequence):
    return calculate_inverted_repeats(sequence,4)*10 + calculate_inverted_repeats(sequence,6)*10 + calculate_gc_deviation(sequence) + TM_deviance(sequence)


def monte_carlo_simulated_anneal(seq, initial_temperature, iteration_length,mutation_positions):
    for iteration in range(iteration_length):
        print(seq)
        # maintaing old sequence
        old_seq = seq 
        # Fast simulated annealing temperature
        temperature = initial_temperature/(iteration + 1)
        # seq pre_mutation_objective
        pre_mutation_objective = score(seq)
        print('pre_mutation_objective: ' + str(pre_mutation_objective))
        # mutate seq
        seq = mutateSequence(seq,math.ceil(temperature),mutation_positions)
        # seq post mutation objective
        post_mutation_objective = score(seq)
        print('post_mutation_objective: ' + str(post_mutation_objective))
        if pre_mutation_objective > post_mutation_objective:
            continue
        else:
            #metropolisis acceptance criterion
            criterion = math.exp(-(post_mutation_objective - pre_mutation_objective)/temperature)
            if criterion > random.uniform(0, 1):
                continue
            else:
                seq = old_seq
    return seq

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def generatePool(input_sequence,initial_temperature, iteration_length, Tm_flexibility, GC_flexibility, poolLength):
    pool = []
    mutation_positions = createMutationMap(input_sequence)
    input_sequence = initialMutation(input_sequence,mutation_positions)
    while len(pool) < poolLength:
        optimised_sequence = monte_carlo_simulated_anneal(input_sequence,initial_temperature,iteration_length,mutation_positions)
        no4repeats = calculate_inverted_repeats(optimised_sequence,4)
        no6repeats = calculate_inverted_repeats(optimised_sequence,6)
        optimised_TM = mt.Tm_NN(optimised_sequence)
        optimised_GC = GC(optimised_sequence)
        if no4repeats == 0 and no6repeats == 0 and 60-Tm_flexibility < optimised_TM < 60+Tm_flexibility and 50-GC_flexibility < optimised_GC < 50+GC_flexibility:
            pool.append(optimised_sequence)
    return pool

my_pool = generatePool(input_sequence='NNNNNNNSSRRRNNNNNNNNNNNNSSSRSRSR',initial_temperature=10, iteration_length=100, Tm_flexibility=5, GC_flexibility=5, poolLength=3)
