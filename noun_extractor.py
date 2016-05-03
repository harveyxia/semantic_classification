import string
from collections import defaultdict
from nltk.tag import _pos_tag as pos_tag
from nltk.tokenize import word_tokenize
from nltk.tag.perceptron import PerceptronTagger
from nltk.stem.regexp import RegexpStemmer

tagger = PerceptronTagger()

st = RegexpStemmer('ing$|s$|e$|able$|y$|er$', min=4)

# Given a filename, return a dict of nouns:count
def get_nouns(filename):
    noun_dict = defaultdict(int)
    with open(filename, 'r') as f:
        for line in f:
            # 1. tokenize the text line
            tokens = word_tokenize(_strip_punctuation(line))
            # 2. tag the POS of each lexical item
            tags = pos_tag(tokens, None, tagger)   # tagset is set to None
            # 3. filter for nouns
            tagged_nouns = filter(lambda tag: tag[1]=='NN', tags)
            for tagged_noun in tagged_nouns:
                noun_dict[stem_word(tagged_noun[0])] += 1
    return dict(noun_dict)

def _strip_punctuation(s):
    printable = set(string.printable)
    s = s.translate(string.maketrans("",""), string.punctuation)
    return filter(lambda x: x in printable, s)

def stem_word(word):
    return st.stem(word)