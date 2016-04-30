from nltk.corpus import wordnet as wn
from collections import defaultdict
import fastcluster
import itertools
import sys
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
            # synsets are found. Replace None with 
            if sim_values[pair] is None:
                sim_values[pair] = 0
            else:
                # wu-palmer score of 1 means identity, take the inverse for dist
                sim_values[pair] = sim_values[pair]
    return dict(sim_values)

# perform hiearchical clustering
def cluster(matrix):
    return fastcluster.weighted(matrix)

# replaces stepwise cluster distance of the whole cluster
def format_clustering(clustering, synset_list):
    table = {}
    new_clustering = []
    for (i, cluster) in enumerate(clustering):
        new_cluster = [int(cluster[0]), int(cluster[1]), float(cluster[2]), int(cluster[3])]
        r_dist = l_dist = float(0)
        l = int(cluster[0])
        r = int(cluster[1])
        if l >= len(synset_list):
            l_dist = table[l][2]
        if r >= len(synset_list):
            r_dist = table[r][2]
        new_cluster[2] += (r_dist + l_dist)
        new_clustering.append(new_cluster)
        table[i+len(synset_list)] = new_cluster
    return new_clustering

# return a set of disjoint and possibly incomplete set of clusters of synsets
# elements may be in more than one cluster
# where the distance of the cluster is <= dist
# dist is the threshold at which to consider clusters
def get_clusters(clustering, synset_list, dist=None, size=2):
    clusters = []
    # get all clusters with less than d distance
    filtered_clustering = list(clustering)
    if dist is not None:
        filtered_clustering = filter(lambda x: x[2] <= dist, filtered_clustering)
    filtered_clustering = filter(lambda x: x[3] == size, filtered_clustering)
    # sort by smallest clusters first
    filtered_clustering = sorted(filtered_clustering, key=lambda x: x[2], reverse=False)
    # assign elements to clusters uniquely
    for cluster in filtered_clustering:
        members = get_cluster_members(cluster[0], clustering, synset_list)
        members.extend(get_cluster_members(cluster[1], clustering, synset_list))
        
        clusters.append(members)
    return clusters

# grabs all elements of a cluster as represented in a stepwise dendrogram
# clustering is a stepwise dendrogram representation of the clustering
def get_cluster_members(i, clustering, synset_list):
    members = []
    if i >= len(synset_list):
        i = i-len(synset_list)
        l = int(clustering[i][0])
        r = int(clustering[i][1])
        # if r < len(synset_list):
        #     members.append(synset_list[r])
        # else:
        members.extend(get_cluster_members(r, clustering, synset_list))

        # if l < len(synset_list):
        #     members.append(synset_list[l])
        # else:
        members.extend(get_cluster_members(l, clustering, synset_list))
    else:
        members.append(synset_list[i])
    return members