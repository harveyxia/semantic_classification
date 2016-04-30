## Setup

Our use of NLTK depends on several corpora.
To install them, run the following in a Python environment:

```
import nltk
nltkl.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

## Issues

NLTK's POS tagger sometimes mis-tags words as nouns. For instance, it tags "tamer"
in the following sentence as a noun: "Scientists once thought that some visionary hunter-gatherer nabbed a wolf puppy from its den one day and started raising tamer and tamer wolves".

## Notes/Ideas

1. Semantic classification vs. what the article is about

2. large clusters vs. iterative clusters of pairs

    The larger the cluster size, the more abstract and oftentimes less accurate
    the hypernym. The smaller the cluster size, especially pairs, yield the
    most accurate hypernyms, but there is less semantic synthesis.

3. Incorporate noun counts for assigning 'salience scores' to each hypernym