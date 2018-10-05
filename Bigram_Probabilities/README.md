**Bigram Model - **

Approximates the probability of a word given all the
previous words by using only the conditional probability of the
preceding word.

**Bigram Probabilty** - To compute a particular bigram probability of a word
  y given a previous word x, we’ll compute the count of the bigram C(xy)
  and normalize by the sum of all bigrams that share the first word x.
  
**Add One Smoothing** - Take matrix of bigram counts, before we normalize
  them into probabilities, and add one to all the counts.
  
**Good Turing Discounting** - Estimate the probability of things that occur
c times in the training corpus by the MLE probability of things that occur
c+1 times in the corpus.

**To run the program:** Navigate to the path where python program is downloaded and type ‘python ./bigram.py’ to run the code. 

**Output:** Following four files will be generated on running the program –

1.	bigramNoSmoothing.txt – will contain bigrams, bigram counts and bigram probabilities for bigram model with no smoothing.

2.	bigramAddOneSmoothing.txt - will contain bigrams, bigram counts and bigram probabilities for bigram model with Add-one (or Laplace) smoothing.

3.	bigramGoodTuringDiscounting.txt - will contain bigrams, bigram counts and bigram probabilities for bigram model with Good-turing discounting based smoothing.

4.	unigramCounts.txt - will contain unigrams and unigram counts of the entire corpus.
