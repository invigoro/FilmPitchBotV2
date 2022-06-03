from text_helpers import *

text = """\
Mr. Smith bought cheapsite.com for 1.5 million dollars, i.e. he paid a lot for it. Did he mind? Adam Jones Jr. thinks he didn't. In any case, this isn't true... Well, with a probability of .9 it isn't.
"""
cleaned = cleanParagraph([text])
assert isinstance(cleaned, list)

paragraphs = ["Oh that this too, too, too sullied flesh would melt, thaw, and resolve itself into a dew, or that the Everlasting had not fix'd his canon 'gainst self-slaughter!", "I saw a man this morning who did not wish to die.", "Tomorrow, and tomorrow, and tomorrow creeps into this petty place from day to day.", "It goes it goes it goes it goes YUH. Guillotine!", "Friends, Romans, countrymen! Lend me your ears! I come to bury Caesar, not to praise him. The evil that men do lives after them; the good is oft interred with their bones. So let it be with Caesar!"]
bigrams = createBigrams(paragraphs)
assert isinstance(bigrams, dict)

trigrams = createTrigrams(paragraphs)
assert isinstance(trigrams, dict)

merged = mergeGrams(bigrams, trigrams)
merged = mergeGrams(bigrams, merged)

sentenceCount = countSentenceCharacters(["This", "sentence", "is", "short."])
assert sentenceCount == 23

next1 = getNext(bigrams, trigrams, ["It"])
next2 = getNext(bigrams, trigrams, ["It", next1])
assert isinstance(next2, str)

sentence = generateSentence(bigrams, trigrams, "It", None, 100)
print(sentence)