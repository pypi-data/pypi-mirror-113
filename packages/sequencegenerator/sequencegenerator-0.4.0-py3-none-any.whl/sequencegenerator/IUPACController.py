import random

IUPAC_RESOLVER = {
    'R': ['A','G'],
    'Y': ['C','T'],
    'S': ['G','C'],
    'W': ['A','T'],
    'K': ['G','T'],
    'M': ['A','C'],
    'B': ['C','G','T'],
    'D': ['A','G','T'],
    'H': ['A','C','T'],
    'V': ['A','C','G'],
    'N': ['A','C','G','T'],
}

def createMutationMap(seq):
    index_mutation_mapping = {}
    for index,value in enumerate(seq):
        if value in IUPAC_RESOLVER.keys():
            index_mutation_mapping.update({index:value})
    return index_mutation_mapping

def updateNucleotide(seq,index,newNucleotide):
    return seq[:index] + newNucleotide + seq[index+1:]

def initialMutation(seq,mutation_map):
    for attr, value in mutation_map.items():
        seq = updateNucleotide(seq,attr,random.choice(IUPAC_RESOLVER[value]))
    return seq

def mutateSequence(seq,number_mutations,mutation_positions):
    mutation_indexs = random.sample(mutation_positions.keys(), number_mutations)
    for mutation_position in mutation_indexs:
        seq = updateNucleotide(seq,mutation_position,random.choice(IUPAC_RESOLVER[mutation_positions[mutation_position]]))
    return seq

myseq = 'NNNNNNNNNNNNNNNNNNNNNNNNN'
mutation_map = createMutationMap(myseq)

myseq = initialMutation(myseq,mutation_map)
print(mutateSequence(myseq,5,mutation_map))
print(mutateSequence(myseq,5,mutation_map))
print(mutateSequence(myseq,5,mutation_map))
print(mutateSequence(myseq,5,mutation_map))
# print(random.choice(IUPAC_RESOLVER('N')))
