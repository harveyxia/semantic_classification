from nltk.corpus import wordnet as wn
import noun_extractor
import cluster

import pdb

# find lowest common ancestory of multiple elements
def lca(synset):
    hypernym = None
    hypernym = reduce(lambda x, y: x.lowest_common_hypernyms(y)[0], synset)
    return hypernym

def run(filename):
    noun_dict = noun_extractor.get_nouns(filename)
    synset_list = cluster.get_synset_list(noun_dict)
    matrix = cluster.gen_sim_matrix(synset_list)
    clustering = cluster.format_clustering(cluster.cluster(matrix), synset_list)

    # clusters = cluster.get_clusters(0.5, clustering, synset_list)
    # pdb.set_trace()
    return clustering

filename = 'test_article.txt'
noun_dict = noun_extractor.get_nouns(filename)
synset_list = cluster.get_synset_list(noun_dict)
matrix = cluster.gen_sim_matrix(synset_list)
clustering = cluster.format_clustering(cluster.cluster(matrix), synset_list)
clusters = cluster.get_clusters(clustering, synset_list, size=3)
clusters = filter(lambda x: x[0] is not None, clusters)
hypernyms = map(lambda x: lca(x), clusters)