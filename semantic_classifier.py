import noun_extractor
import cluster

import pdb

def run(filename):
    noun_dict = noun_extractor.get_nouns(filename)
    synset_list = cluster.get_synset_list(noun_dict)
    matrix = cluster.gen_sim_matrix(synset_list)
    clustering = cluster.cluster(matrix)
    # clusters = cluster.get_clusters(0.5, clustering, synset_list)
    # pdb.set_trace()
    return clustering

filename = 'test_article.txt'
noun_dict = noun_extractor.get_nouns(filename)
synset_list = cluster.get_synset_list(noun_dict)
matrix = cluster.gen_sim_matrix(synset_list)
clustering = cluster.cluster(matrix)