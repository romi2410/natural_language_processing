"""
Author - Romi Padam

"""
from collections import Counter

#-----------------------------------------------------------------------#
#--------------Reading file and extracting words & tags-----------------#
#-----------------------------------------------------------------------#
def readTaggedCorpus(file):
    words = []
    tags = []

    f = open(file, 'r')
    for sentence in f.read().split('\n'):
        for word in sentence.split():
            words.append(word.split('_')[0])
            tags.append(word.split('_')[1])

    f.close()

    return words, tags

#-----------------------------------------------------------------------#
#----------------Find most likely tag for each word---------------------#
#-----------------------------------------------------------------------#
def selectMostLikely(words, tags):
    wordTagDict = {}

    for i in range(len(words)):
        if not words[i] in wordTagDict:
            wordTagDict[words[i]] = [tags[i]]
        else:
            wordTagDict[words[i]].append(tags[i])

    for key, value in wordTagDict.items():
        mostLikely = Counter(value).most_common()[0][0]
        wordTagDict[key] = mostLikely

    finWordTag = []
    for word in words:
        finWordTag.append(wordTagDict[word])

    return finWordTag

#-----------------------------------------------------------------------#
#---------------------------Brills algorithm----------------------------#
#-----------------------------------------------------------------------#
def brills(tags, finWordTag, fromTag, toTag):
    brillsRuleDictionary = {}

    for i in range(1,len(finWordTag)):
        if tags[i] == toTag and finWordTag[i] == fromTag:
            rule = (finWordTag[i-1], fromTag, toTag)
            if rule in brillsRuleDictionary:
                brillsRuleDictionary[rule] += 1
            else:
                brillsRuleDictionary[rule] = 1
        elif tags[i] == fromTag and finWordTag[i] == fromTag:
            rule = (finWordTag[i-1], fromTag, toTag)
            if rule in brillsRuleDictionary:
                brillsRuleDictionary[rule] -= 1
            else:
                brillsRuleDictionary[rule] = -1
    sortedBrillsRuleDictionary = sorted(brillsRuleDictionary.items(), key=lambda t: t[1], reverse=True)

    return sortedBrillsRuleDictionary[:5]

#-----------------------------------------------------------------------#
#------------------------Print Report-----------------------------------#
#-----------------------------------------------------------------------#
def printTagReport(filename, words, tags, finWordTag):
    file = open(filename, 'w')
    file.write("{:<15}{:<10}{:<10}\n".format('Word', 'Tag', 'Most-Likely Tag'))
    file.write("{:<15}{:<10}{:<10}\n".format('----', '---', '---------------'))
    for i in range(len(tags)):
        file.write("{:<15}{:<10}{:<10}\n".format(str(words[i]), str(tags[i]), str(finWordTag[i])))
    file.close()

def printReport(filename, rules):
    file = open(filename, 'w')
    file.write("{:<15}{:<10}{:<10}{:<10}\n".format('Previous Word', 'From', 'To', 'Score'))
    file.write("{:<15}{:<10}{:<10}{:<10}\n".format('-------------', '----', '--',  '-----'))
    for i in range(len(rules)):
        file.write("{:<15}{:<10}{:<10}{:<10}\n".format(str(rules[i][0][0]), str(rules[i][0][1]), str(rules[i][0][2]), str(rules[i][1])))
    file.close()

#-----------------------------------------------------------------------#
#---------------------------------Main----------------------------------#
#-----------------------------------------------------------------------#
if __name__ == '__main__':
    file = 'HW2_S18_NLP6320_POSTaggedTrainingSet-Unix.txt'

    # Extracting word and tag from a tagged corpus
    words, tags = readTaggedCorpus(file)

    # Stage 1 - Label every word with its most-likely tag
    finWordTag = selectMostLikely(words, tags)
    printTagReport('mostLikelyTags.txt', words, tags, finWordTag)

    # Stage 2 - Examine every possible transformation and select the one that results in the most improved tagging
    transformNNToVB = brills(tags, finWordTag, 'NN', 'VB')
    print("Printing report with best 5 transformation rules to transform NN to VB...")
    printReport('brillsTransformationRulesNNToVB.txt', transformNNToVB)

    transformVBToNN = brills(tags, finWordTag, 'VB', 'NN')
    print("Printing report with best 5 transformation rules to transform VB to NN...")
    printReport('brillsTransformationRulesVBToNN.txt', transformVBToNN)

    # Stage 3 - Use the above generated transformation rules to re-tag the data.
    print("End of program")
