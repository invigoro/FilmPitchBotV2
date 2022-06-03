import random
import re
import sys

def createBigrams(paragraphs):
    bigrams = {}
    cleaned = cleanParagraph(paragraphs)
    for p in cleaned:
        word = None
        description = str.split(p, " ")
        for w in description: 
            if(word is not None):
                bentry = bigrams.get(word)
                if(bentry):
                    bentry[w] = (bentry.get(w) or 0) + 1
                else:
                    bigrams[word] = {
                        w: 1
                    }
            word = w

        #assign end of sentence
        w = description[-1]
        bentry = bigrams.get(word)
        if(bentry): 
            bentry["\n"] = (bentry.get(w) or 0) + 1
        else:
            bigrams[word] = {
                "\n": 1
            }
    return bigrams

def createTrigrams(paragraphs): 
    trigrams = {}
    cleaned = cleanParagraph(paragraphs)
    for p in cleaned:
        twowords = []
        description = str.split(p, " ")
        for w in description: 
            if(len(twowords) == 2):
                word = f'{twowords[0]} {twowords[1]}'
                tentry = trigrams.get(word)
                if(tentry):
                    tentry[w] = (tentry.get(w) or 0) + 1
                else:
                    trigrams[word] = {
                        w: 1
                    }
                twowords = twowords[1:]
            twowords.append(w)
        
        #assign end of sentence
        if(len(twowords) == 2):
            w = description[-1]
            word = f'{twowords[0]} {twowords[1]}'
            tentry = trigrams.get(word)
            if(tentry): 
                tentry["\n"] = (tentry.get(w) or 0) + 1
            else:
                trigrams[word] = {
                    "\n": 1
                }
    return trigrams

# for merging two dictionaries, e.g. two bigram dicts or two trigram dicts
def mergeGrams(gram1, gram2):
    for first, poss in gram2.items():
        existingFirst = gram1.get(first)
        if existingFirst:
            for second, count in poss.items():
                existingSecond = existingFirst.get(second)
                if existingSecond:
                    gram1[first][second] += count
                else:
                    gram1[first][second] = count
        else:
            gram1[first] = poss
    return gram1


def getNext(bigrams, trigrams, sentence, endSentenceWeight = 0):
    if(endSentenceWeight >= 1): return '\n...'
    if(len(sentence) >= 2):
        #first remove immediate duplicates as options
        bs = bigrams.get(sentence[-1])
        ts = trigrams.get(f'{sentence[-2]} {sentence[-1]}')
        bskeys = list(filter(lambda key: key is not sentence[-2], bs.keys()))
        if(ts):
            tskeys = list(filter(lambda key: key is not sentence[-2], ts.keys()))

            # 50/50 random between tri and bi
            useTri = bool(random.randint(0, 1)) and len(tskeys) > 0
            if(useTri):
                return getRandomGram(getFilteredDict(ts, tskeys, endSentenceWeight))
            else:
                return getRandomGram(getFilteredDict(bs, bskeys, endSentenceWeight))


    else: # should only happen at the beginning of the sentence
        return getRandomGram(bigrams.get(sentence[0]))


def getFilteredDict(dic, filteredKeys, weight):
    result = {}
    for key in filteredKeys:
        if key == '\n': #heavily increase probability of ending a sentence as weight increases
            result[key] = dic[key] * (1 / (1 - weight))
        else: 
            result[key] = dic[key]
    return result

def getRandomGram(grams):
    range = sum(grams.values())
    target = random.uniform(0, range)
    start = 0
    result = None
    for key, val in grams.items():
        start += val
        if start >= target:
            result = key
            break
    return result

def generateSentence(bigrams, trigrams, seed, prev, goalLength):
    if((not seed and not prev) or (seed and prev)):
        sys.exit("Need either a previous sentence or a seed word.")
    sentence = []
    if(seed): 
        # Start with a seed word
        sentence.append(seed)
    else:
        # base it on prev 2 words
        prevEnd = prev[-2:]
        sentenceStart = getNext(bigrams, trigrams, prevEnd, 0)
        # should it do two words or just do the one for a cleaner break?
        # sentence = [sentenceStart, getNext(bigrams, trigrams, [prevEnd[-1], sentenceStart])]
        sentence.append(sentenceStart)
    sentenceLength = countSentenceCharacters(sentence)

    # loop through and re-weight priority for ending the sentence as it gets longer
    while(sentenceLength < goalLength * 2):
        nextWord = getNext(bigrams, trigrams, sentence, sentenceLength / (goalLength * 2))
        if nextWord == '\n...':
            sentence.append("...")
        if(nextWord[0] == '\n'): 
            break
        sentence.append(nextWord)
        sentenceLength = countSentenceCharacters(sentence)
    return sentence

def countSentenceCharacters(sentence):
    return len(' '.join(sentence))

# replace ". [Capital]" with ". \n " so that we know where sentences end
def cleanParagraph(paragraphs):
    result = []
    #pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    pattern = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", re.M)
    for p in paragraphs:
        spl = pattern.split(p)
        result.extend(spl)
    return result

def getRandomSentenceStart(paragraphs):
    cleaned = cleanParagraph(paragraphs)
    start = random.randint(0, len(cleaned) - 1)
    return str.split(cleaned[start], " ")[0]