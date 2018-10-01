"""
Author - Romi Padam

"""

#-----------------------------------------------------------------------#
#---------------------Reading file and extracting words-----------------#
#-----------------------------------------------------------------------#
def readCorpus(file):
    corpus = []

    f = open(file, 'r')
    for word in f.read().split():
        corpus.append(word)
    f.close()

    return corpus

#-----------------------------------------------------------------------#
#---------Creating Bigrams, calculating bigram & unigram counts---------#
#-----------------------------------------------------------------------#
def createBigram(corpus):
    bigrams = []
    bigramCounts = {}
    unigramCounts = {}
    corpusSize = len(corpus)

    for i in range(corpusSize-1):
        bigram = (corpus[i], corpus[i+1])
        bigrams.append(bigram)

        if bigram in bigramCounts:
            bigramCounts[bigram] += 1
        else:
            bigramCounts[bigram] = 1

        if corpus[i] in unigramCounts:
            unigramCounts[corpus[i]] += 1
        else:
            unigramCounts[corpus[i]] = 1

    return bigrams, bigramCounts, unigramCounts

#-----------------------------------------------------------------------#
#---------------------Calculating bigram probabilities------------------#
#-----------------------------------------------------------------------#
def calculateBigramProb(bigrams, bigramCounts, unigramCounts):
    bigramProb = {}

    for bigram in bigrams:
        bigramProb[bigram] = bigramCounts.get(bigram) / unigramCounts.get(bigram[0])

    return bigramProb

#-----------------------------------------------------------------------#
#-------Calculating bigram probabilities with Add One Smoothing---------#
#-----------------------------------------------------------------------#
def addOneSmoothing(bigrams, bigramCounts, unigramCounts):
    bigramProbAddOne = {}

    for bigram in bigrams:
        bigramProbAddOne[bigram] = (bigramCounts.get(bigram) + 1) / (unigramCounts.get(bigram[1]) + len(unigramCounts))

    return bigramProbAddOne

#-----------------------------------------------------------------------#
#------Calculating bigram probabilities with Good Turing Discounting----#
#-----------------------------------------------------------------------#
def goodTurningDiscounting(bigrams, bigramCounts):
    bins = {}
    cStar = {}
    pStar = {}
    bigramProbGoodTurning = {}

    # Computing Nc bins
    for key, value in bigramCounts.items():
        if value in bins:
            bins[value] += 1
        else:
            bins[value] = 1

    # Computing missing bins
    for b in range(max(bins, key=int)):
        if b not in bins:
            bins[b] = 0

    # Sorting bins on keys
    sortedBinsList = sorted(bins.items(), key=lambda t: t[0])

    # Calculating pStar of bin with zero count
    pStarZeroCount = sortedBinsList[0][1] / len(bigrams)

    # Calculating cStar and pStar of remaining bins
    i = 1
    for key, value in sortedBinsList:
        if i < len(sortedBinsList)-1:
            if value == 0:
                cStar[key] = 0
                pStar[key] = 0
            else:
                cStar[key] = (key + 1) * sortedBinsList[key+1][1] / value
                pStar[key] = cStar[key] / len(bigrams)

        else:
            cStar[key] = 0
            pStar[key] = 0
        i += 1

    for bigram in bigrams:
        bigramProbGoodTurning[bigram] = pStar.get(bigramCounts[bigram])

    return bigramProbGoodTurning

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
    file = "HW2_S18_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Unix.txt";

    # Reading the file's content (corpus)
    corpus = readCorpus(file)

    # Creating Bigrams & Unigrams
    bigrams, bigramCounts, unigramCounts = createBigram(corpus)

    # Writing unigram counts in a file 'unigramCounts.txt'
    file = open('unigramCounts.txt', 'w')
    file.write("{:<20}{:<20}\n".format('Unigrams', 'Counts'))
    file.write("{:<20}{:<20}\n".format('--------', '------'))
    for key, value in unigramCounts.items():
        file.write("{:<20}{:<20}\n".format(key, value))
    file.close()

    # 1. Bigram counts & probabilities with No Smoothing
    #-------------------------------------------------------------------------------#
    bigramProb = calculateBigramProb(bigrams, bigramCounts, unigramCounts)
    print("Printing report for bigram model with no smoothing...")
    printReport('bigramNoSmoothing.txt', bigrams, bigramCounts, bigramProb)

    # 2. Bigram counts & probabilities with Add-one Smoothing
    #-------------------------------------------------------------------------------#
    bigramProbAddOne = addOneSmoothing(bigrams, bigramCounts, unigramCounts)
    print("Printing report for bigram model with add-one smoothing...")
    printReport('bigramAddOneSmoothing.txt', bigrams, bigramCounts, bigramProbAddOne)

    # 3. Bigram counts & probabilities with Good-Turing Discounting based Smoothing
    #-------------------------------------------------------------------------------#
    bigramProbGoodTurning = goodTurningDiscounting(bigrams, bigramCounts)
    print("Printing report for bigram model with good-turing discounting based smoothing...")
    printReport('bigramGoodTuringDiscounting.txt', bigrams, bigramCounts, bigramProbGoodTurning)

    print("End of program")
