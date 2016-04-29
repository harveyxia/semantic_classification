from nltk.corpus import wordnet as wn
from collections import defaultdict
import fastcluster
import itertools

import pdb 

def get_synset_list(noun_dict):
    synset_list = []
    # create ordered list of nouns
    noun_list = [noun for noun in noun_dict]
    for noun in noun_list:
        synsets = wn.synsets(noun)
        # if no synset found
        if len(synsets) == 0:
            synset_list.append(None)
        else:
            # grab most common synset for each noun
            synset_list.append(synsets[0])
    return synset_list

# given a dict of noun:count, generate 2-dimensional similarity matrix
# synset_list defines the mapping from index to synset for matrix
def gen_sim_matrix(synset_list):
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

# perform hiearchical clustering
def cluster(matrix):
    return fastcluster.linkage(matrix)

# return a set of disjoint and possibly incomplete set of clusters of synsets
# where the distance of the cluster is <= dist
# dist is a value between 0 and 1, 1 being the max distance in the set of synsets
def get_clusters(dist, clustering, synset_list):
    d = dist*(clustering[-1][2])
    clusters = []
    # get all clusters with less than d distance
    for cluster in clustering:
        if cluster[2] <= d:
            clusters.append(cluster)
    # sort by largest clusters first
    clusters = sorted(clusters, key=lambda x: x[3], reverse=True)
    # assign elements to clusters uniquely
    # for cluster in clusters:

    return clusters

def get_cluster_members(i, clustering, synset_list):
    l = int(clustering[i-len(synset_list)][0])
    r = int(clustering[i-len(synset_list)][1])
    members = []
    if r < len(synset_list):
        members.append(synset_list[r])
    else:
        members.extend(get_cluster_members(r, clustering, synset_list))

    if l < len(synset_list):
        members.append(synset_list[l])
    else:
        members.extend(get_cluster_members(l, clustering, synset_list))
    return members