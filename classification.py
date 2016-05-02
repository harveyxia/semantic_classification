class Classification():
    """
    Object representation of output of semantic classifier algorithm.
    """

    def __init__(self, noun_dict, synset_list, synset_dict,
                matrix, clustering, clusters, hypernyms):
        self.noun_dict = noun_dict
        self.synset_list = synset_list
        self.synset_dict = synset_dict
        self.matrix = matrix
        self.clustering = clustering
        self.clusters = clusters
        self.hypernyms = hypernyms