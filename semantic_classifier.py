import noun_extractor
import cluster

def run(filename):
    noun_dict = noun_extractor.get_nouns(filename)
    matrix = cluster.gen_sim_matrix(noun_dict)
    return matrix