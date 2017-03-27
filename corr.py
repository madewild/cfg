#!/usr/bin/python

"""
Correction software
"""

#pylint: disable = locally-disabled, invalid-name

import nltk

pos = open('pos.txt').readlines()
pos = [line.strip() for line in pos]

neg = open('neg.txt').readlines()
neg = [line.strip() for line in neg]

string = 'type CFG here'

lowstring = string.lower()
gram = nltk.CFG.fromstring(lowstring)
parser = nltk.ChartParser(gram)
p = 0
n = 0
for text in pos:
    tokens = nltk.tokenize.wordpunct_tokenize(text.lower())
    try:
        trees = parser.parse(tokens)
    except ValueError:
        trees = []
    if len(list(trees)) > 0:
        p += 1
for text in neg:
    tokens = nltk.tokenize.wordpunct_tokenize(text.lower())
    try:
        trees = parser.parse(tokens)
    except ValueError:
        trees = []
    for tree in trees:
        if tree:
            n += 1
score = max(0, p-n)
print("Score partiel : " + str(score) + "/10 (" + str(p) + " bonnes phrases et " + str(n) + " mauvaises phrases reconnues)")
