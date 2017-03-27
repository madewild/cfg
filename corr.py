#!/usr/bin/python

"""
Correction software
"""

#pylint: disable = locally-disabled, invalid-name

import os
import nltk

path = 'travaux/2e sess/'

files = os.listdir(path)
files = ['Méryem Lahouel_3506608_assignsubmission_file_lahouel_meryem.cfg']

pos = open('pos.txt').readlines()
pos = [line.strip() for line in pos]

neg = open('neg.txt').readlines()
neg = [line.strip() for line in neg]

total = 0

for f in sorted(files):
    fullpath = path+f
    gram = open(fullpath).read().lower()
    gram = nltk.CFG.fromstring(gram)
    parser = nltk.ChartParser(gram)
    p = 0
    n = 0
    for text in pos:
        tokens = nltk.tokenize.wordpunct_tokenize(text.lower())
        try:
            trees = parser.parse(tokens)
        except ValueError:
            #print(sys.exc_info()) # affiche les mots manquants
            trees = []
        if len(list(trees)) > 0:
            p += 1
        else:
            print(text) # affiche les faux négatifs
    for text in neg:
        tokens = nltk.tokenize.wordpunct_tokenize(text.lower())
        try:
            trees = parser.parse(tokens)
        except ValueError:
            trees = []
        for tree in trees:
            if tree:
                n += 1
                #print(text) # affiche les faux positifs
                #print(tree)
    score = max(1, p-n)
    total += score
    print("\t".join([f.split("_")[0], str(score), str(p), str(n)]))
print('Moyenne :', total/len(files))
