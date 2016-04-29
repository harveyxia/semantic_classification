from nltk.corpus import wordnet as wn
from collections import defaultdict
import fastcluster
import itertools

import pdb 

# given a dict of noun:count, generate 2-dimensional similarity matrix
def gen_sim_matrix(noun_dict):
    # create ordered list of nouns
    noun_list = [noun for noun in noun_dict]
    # grab most common synset for each noun
    # synset_list defines the mapping from index to synset for matrix
    synset_list = [get_synset(noun) for noun in noun_list]
    # get similarity for each pair of nouns
    sim_values = get_sim_values(synset_list)

    # initialize 2d matrix
    matrix = [[0 for i in xrange(len(synset_list))] for i in xrange(len(synset_list))]
    for (i1, syn1) in enumerate(synset_list):
        for (i2, syn2) in enumerate(synset_list):
            if syn1 is None or syn2 is None:
                matrix[i1][i2] = 0
            elif syn1 is syn2:
                matrix[i1][i2] = wn.wup_similarity(syn1, syn2)
            else:
                try:
                    matrix[i1][i2] = sim_values[(syn1, syn2)]
                except KeyError:
                    matrix[i1][i2] = sim_values[(syn2, syn1)]
    return matrix

def get_synset(noun):
    synsets = wn.synsets(noun)
    if len(synsets) == 0:
        return None
    else:
        return synsets[0]

def get_sim_values(synset_list):
    sim_values = defaultdict(int)
    for pair in itertools.combinations(synset_list, 2):
        if pair[0] is None or pair[1] is None:
            sim_values[pair] = 0
        else:
            sim_values[pair] = wn.wup_similarity(pair[0], pair[1])
            # wn.wup_similarity() returns None if no path connecting the two
            # synsets are found. Replace None with 0
            if sim_values[pair] is None:
                sim_values[pair] = 0
    return dict(sim_values)

def cluster(matrix):
    return fastcluster.linkage(matrix)