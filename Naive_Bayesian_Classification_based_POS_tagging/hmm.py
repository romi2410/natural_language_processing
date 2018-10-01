"""
Author - Romi Padam

"""

#-----------------------------------------------------------------------#
#--------------Reading file and extracting words & tags-----------------#
#-----------------------------------------------------------------------#
def readTaggedCorpus(file):
    tags = []
    words = []

    f = open(file, 'r')
    for sentence in f.read().split('\n'):
        for word in sentence.split():
            words.append(word.split('_')[0])
            tags.append(word.split('_')[1])

    f.close()

    return words, tags

#-----------------------------------------------------------------------#
#---------Creating Bigrams, calculating bigram & unigram counts---------#
#-----------------------------------------------------------------------#
def createBigram(tags):
    bigrams = []
    bigramCounts = {}
    unigramCounts = {}
    tagSize = len(tags)

    for i in range(tagSize-1):
        bigram = (tags[i], tags[i+1])
        bigrams.append(bigram)

        if bigram in bigramCounts:
            bigramCounts[bigram] += 1
        else:
            bigramCounts[bigram] = 1

        if tags[i] in unigramCounts:
            unigramCounts[tags[i]] += 1
        else:
            unigramCounts[tags[i]] = 1

    return bigrams, bigramCounts, unigramCounts

#-----------------------------------------------------------------------#
#-------------Calculating tag transition probabilities------------------#
#-----------------------------------------------------------------------#
def computeTagTansitionProb(bigrams, bigramCounts, unigramCounts):
    tagTansitionProb = {}

    for bigram in bigrams:
        tagTansitionProb[bigram] = bigramCounts.get(bigram)/unigramCounts.get(bigram[0])

    return tagTansitionProb

#-----------------------------------------------------------------------#
#---------Creating Bigrams, calculating bigram & unigram counts---------#
#-----------------------------------------------------------------------#
def createBigramWordsTags(words, tags):
    bigramWordsTags=[]
    bigramCountsWordsTags = {}

    corpusSize = len(words)
    for i in range(corpusSize-1):
        bigram = (tags[i], words[i])
        bigramWordsTags.append(bigram)

        if bigram in bigramCountsWordsTags:
            bigramCountsWordsTags[bigram] += 1
        else:
            bigramCountsWordsTags[bigram] = 1

    return bigramWordsTags, bigramCountsWordsTags

#-----------------------------------------------------------------------#
#---------------------Calculating likelihood probabilities--------------#
#-----------------------------------------------------------------------#
def computeLikelihoodProb(bigramWordsTags, bigramCountsWordsTags, unigramCounts):
    likelihoodProb={}

    for bigram in bigramWordsTags:
        likelihoodProb[bigram] = bigramCountsWordsTags.get(bigram)/unigramCounts.get(bigram[0])

    return likelihoodProb

#-----------------------------------------------------------------------#
#------------------------Print Report-----------------------------------#
#-----------------------------------------------------------------------#
def printReport(filename, bigrams, bigramCounts, bigramProb):
    file = open(filename, 'w')
    file.write("{:<30}{:<20}{:<20}\n".format('(Bigrams', 'Counts', 'Probabilities)'))
    file.write("{:<30}{:<20}{:<20}\n".format('(-------', '------', '-------------)'))
    for i in range(len(bigrams)):
        file.write("({:<30},{:<20},{:<20})\n".format(str(bigrams[i]), str(bigramCounts[bigrams[i]]), str(bigramProb[bigrams[i]])))
    file.close()

#-----------------------------------------------------------------------#
#---------------------------------Main----------------------------------#
#-----------------------------------------------------------------------#
if __name__ == '__main__':
    file = 'HW2_S18_NLP6320_POSTaggedTrainingSet-Unix.txt'

    # Step 1 - Computing tag trasition probabilities, P(ti|ti-1)
    # 1. Extracting words and tags from a tagged corpus
    words, tags = readTaggedCorpus(file)
    # 2. Creating Bigrams & Unigrams for tags (tag given previous tag)
    bigrams, bigramCounts, unigramCounts = createBigram(tags)
    # 3. Computing tag transition probabilities
    tagTansitionProb = computeTagTansitionProb(bigrams, bigramCounts, unigramCounts)
    print("Printing report for bigram model of tag transition probabilities...")
    printReport('tagTransitionProb.txt', bigrams, bigramCounts, tagTansitionProb)

    # Step 2 - Computing likelihood probabilities, P(wi|ti)
    # 1. Creating Bigrams for tags and words (word given tag)
    bigramWordsTags, bigramCountsWordsTags = createBigramWordsTags(words, tags)
    # 2. Computing likelihood probabilities
    likelihoodProb = computeLikelihoodProb(bigramWordsTags, bigramCountsWordsTags, unigramCounts)
    print("Printing report for bigram model of likelihood probabilities...")
    printReport('likelihoodProb.txt', bigramWordsTags, bigramCountsWordsTags, likelihoodProb)

    print("End of program")
