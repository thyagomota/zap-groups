# zap-groups
# Author: Thyago Mota
# Description: Extracts nouns frequencies from a file containing a list of WhatsApp groups
# Date: August 2, 2020

import re, sys, nltk
from nltk.corpus import mac_morpho
# nltk.download('mac_morpho')

# sentences = nltk.sent_tokenize("O carro começou a falhar no meio do caminho.", language = "portuguese")
# sentences = nltk.sent_tokenize("O carro começou a falhar no meio do caminho.")

print("Training tagger...")
macMorpho = mac_morpho.tagged_sents()

sizeTraining = int(len(macMorpho) * 0.9)
training_sentences = macMorpho[:sizeTraining]

tagger0 = nltk.tag.UnigramTagger(training_sentences)
tagger1 = nltk.tag.BigramTagger(training_sentences, backoff=tagger0)
posTagger = nltk.tag.TrigramTagger(training_sentences, backoff=tagger1)
print("Done!")

# words = nltk.word_tokenize("O carro começou a falhar no meio do caminho.")
# print(posTagger.tag(words))


# nouns = []
# for sentence in sentences:
#     for word, pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
#         print(word, pos)
#         if pos == "NN" or pos == "NNP" or pos == "NNS" or pos == "NNPS":
#             nouns.append((word, pos))
# print(nouns)
# sys.exit(1)

GROUPS_FILE_NAME = "groups.txt"
OUTPUT_FILE_NAME = "nouns.csv"

# open sample file
f_in = open(GROUPS_FILE_NAME, "rt")

# read one line at a time
print("Processing...")
nouns = {}
for line in f_in:

    # strip last character from the line
    line = line.strip()

    # extract info
    fields = line.split(",")
    description = ""
    link = ""
    for field in fields:
        if re.match("^https://chat.whatsapp.com/", field):
            link = field
            # print(link)
        else:
            # NLP of the description
            words = nltk.word_tokenize(field)
            for word, pos in posTagger.tag(words):
                word = word.lower()
                if pos == "N":
                    if word not in nouns:
                        nouns[word] = 0
                    nouns[word] += 1

# close sample file
f_in.close()

# convert map to list
noun_pairs = []
for noun in nouns:
    noun_pairs.append((noun, nouns[noun]))

# sort list by 2nd element
noun_pairs.sort(key = lambda x: x[1], reverse = True)
f_out = open(OUTPUT_FILE_NAME, "wt")
for noun, frequency in noun_pairs:
    f_out.write(noun + "," + str(frequency) + "\n")
f_out.close()

