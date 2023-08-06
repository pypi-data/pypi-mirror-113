import random, string
NUCLEOTIDES = ['A','C','T','G']

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def initial_mutation(seq,mutation_positions):
    seq = list(seq)
    for occurance in mutation_positions:
        seq[occurance] = random.choice(NUCLEOTIDES)
    return ''.join(seq)

input='ACXXXXXXXXXXXXXXXXXXXXXXXXXXCA'
print(initial_mutation(input,findOccurrences(input,'X')))

