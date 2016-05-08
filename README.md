## Setup

Our use of NLTK depends on several corpora.
To install them, run the following in a Python environment:

```
import nltk
nltkl.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

## Running the script

1. open an ipython terminal
2. `run semantic_classifier.py`
3. `output = run('filename.txt', min_size, max_size, max_dist)`
4. `output.hypernyms`

Replace the 'filename.txt' with the input file of choice, and set the `min_size`,
`max_size`, and `max_dist.` The last step outputs the ordered list of hypernyms.

## Algorithm

semantic_classifier.py

1. Extract all nouns from document, noun_extractor.py

    a. Strip all punctuation and non-ascii characters from each line
    b. Tokenize the line
    c. Tag the POS of each token
    d. Filter out all non-noun tokens
    e. Add all noun tokens to a Python dict and track occurrences of each noun

2. Convert nouns to synsets and remove nouns for which no synset exists

3. Generate the 2D matrix of similarity values

4. Perform hierarchical clustering

5. Get clusters based on min_size, max_size, and dist parameters.

6. Sort clusters by noun occurrence, most frequent first.

7. Find the least common ancestor of each cluster of synsets.


## Notes/Ideas/Issues

1. Semantic classification vs. what the article is about

2. large clusters vs. iterative clusters of pairs

    The larger the cluster size, the more abstract and oftentimes less accurate
    the hypernym. The smaller the cluster size, especially pairs, yield the
    most accurate hypernyms, but there is less semantic synthesis.

3. hypernym vs. content

    E.g. "Photograph" is not clustered with "photography," their wup_similarity
    is only 0.1176. But the wup_similarity of "photograph" with "painting" is
    0.705

4. Incorporate noun counts for assigning 'salience scores' to each hypernym

5. NLTK's POS tagger sometimes mis-tags words as nouns. For instance, it tags "tamer"
in the following sentence as a noun: "Scientists once thought that some visionary hunter-gatherer nabbed a wolf puppy from its den one day and started raising tamer and tamer wolves".

6. Currently, the algorithm only takes the first synset and first common hypernym

    a. The first synset is the most frequently occurring, but it might be the
    incorrect sense of the noun.
    b. A set of synsets might have multiple lowest common hypernyms, some of which
    may be more accurate than others.

7. How to do evaluation?

8. Morphology — collapse 'photography' and 'photograph'?

9. Methodological limitations

    a. Only accounts for nouns
    b. Hypernym is not equivalent to 'semantic class' or 'content'
    c. A document's complete semantic meaning cannot fully be captured by a set
    of nouns

10. discuss clustering mode, i.e. median vs. complete