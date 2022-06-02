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


def getNext(bigrams, trigrams, sentence):
    if(len(sentence) >= 2):
        #first remove immediate duplicates as options
        bs = bigrams.get(sentence[-1])
        ts = trigrams.get(f'{sentence[-2]} {sentence[-1]}')
        bskeys = filter(lambda key: key is not sentence[-2], bs.keys())
        if(ts):
            tskeys = filter(lambda key: key is not sentence[-2], ts.keys())

            # 50/50 random between tri and bi
            useTri = bool(random.randint(0, 1)) and len(tskeys > 0)
            if(useTri):
                return getRandomGram(getFilteredDict(ts, tskeys))
            else:
                return getRandomGram(getFilteredDict(bs, bskeys))


    else: # should only happen at the beginning of the sentence
        return getRandomGram(bigrams[sentence[0]])


def getFilteredDict(dic, filteredKeys):
    result = {}
    for key in filteredKeys:
        result[key] = dic[key]
    return result

def getRandomGram(grams):
    range = sum(grams.values())
    target = random.randint(0, range)
    start = 0
    result = None
    for key, val in grams:
        start += val
        if start >= target:
            result = key
            break
    return result

def generateSentence(bigrams, trigrams, seed, prev, maxLength):
    if((not seed and not prev) or (seed and prev)):
        sys.exit("Need either a previous sentence or a seed word.")
    sentence = []
    if(seed): 
        print("Start with seed word")
        sentence.append(seed)
    else:
        print("Base it on 2 prev words")
        prevEnd = str.split(prev, " ")[-2:-1]
        sentenceStart = getNext(bigrams, trigrams, prevEnd)

    while():
        print("generate sentence")
    return

def countSentenceCharacters(sentence):
    len(' '.join(sentence))

# replace ". [Capital]" with ". \n " so that we know where sentences end
def cleanParagraph(paragraphs):
    result = []
    pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    for p in paragraphs:
        spl = pattern.findall(p)
        result.extend(spl)
    return result