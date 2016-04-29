from collections import defaultdict
from nltk.tag import _pos_tag as pos_tag
from nltk.tokenize import word_tokenize
from nltk.tag.perceptron import PerceptronTagger

tagger = PerceptronTagger()

# Given a filename, return a dict of nouns:count
def get_nouns(filename):
    noun_dict = defaultdict(int)
    with open(filename, 'r') as f:
        for line in f:
            # 1. tokenize the text line
            tokens = word_tokenize(line)
            # 2. tag the POS of each lexical item
            tags = pos_tag(tokens, None, tagger)   # tagset is set to None
            # 3. filter for nouns
            nouns = filter(lambda tag: tag[1]=='NN', tags)
            for noun in nouns:
                noun_dict[noun] += 1
    return noun_dict