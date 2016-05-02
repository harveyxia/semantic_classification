from classification import Classification
from nltk.corpus import wordnet as wn
import noun_extractor
import cluster

import pdb

# find lowest common ancestory of multiple elements
def lca(synset):
    return reduce(lca_helper, synset)

# only return the first hypernym
def lca_helper(x, y):
    if x is None or y is None:
        return None
    hypernyms = x.lowest_common_hypernyms(y)
    if len(hypernyms) == 0:
        return None
    else:
        return hypernyms[0]

# runs the entire algorithm, wrap output in Classification object
def run(filename, min_size, max_size, dist):
    noun_dict = noun_extractor.get_nouns(filename)
    (synset_list, synset_dict) = cluster.get_synset_list(noun_dict)
    matrix = cluster.gen_sim_matrix(synset_list)
    clustering = cluster.format_clustering(cluster.cluster(matrix), synset_list)
    clusters = cluster.get_clusters(clustering, synset_list, min_size, max_size, dist=dist)
    clusters = filter(lambda x: x[0] is not None, clusters)
    cluster_counts = cluster.get_cluster_counts(clusters, synset_dict)
    # sort clusters by noun counts, most frequent first
    sorted_clusters = [x[1] for x in sorted(enumerate(clusters), key=lambda x: cluster_counts[x[0]], reverse=True)]
    hypernyms = filter(lambda x: x is not None, map(lambda x: lca(x), sorted_clusters))
    return Classification(noun_dict, synset_list, synset_dict, matrix, clustering, sorted_clusters, hypernyms)