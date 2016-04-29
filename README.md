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