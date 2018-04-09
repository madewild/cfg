# -*- coding: utf-8 -*-
"""Functions for CFG testing"""

import nltk

def test_cfg(string):
    '''Compute score based on CFG input'''
    pos = open('pos.txt').readlines()
    pos = [line.strip() for line in pos]

    neg = open('neg.txt').readlines()
    neg = [line.strip() for line in neg]

    lowstring = string.lower().encode('utf-8').replace("Þ", "->")
    gram = nltk.CFG.fromstring(lowstring)
    parser = nltk.ChartParser(gram)
    p = 0
    n = 0
    fneg = []
    fpos = []
    for text in pos:
        tokens = nltk.tokenize.wordpunct_tokenize(text.lower())
        try:
            trees = parser.parse(tokens)
        except ValueError:
            trees = []
        if len(list(trees)) > 0:
            p += 1
        else:
            fneg.append(text)
    for text in neg:
        tokens = nltk.tokenize.wordpunct_tokenize(text.lower())
        try:
            trees = parser.parse(tokens)
        except ValueError:
            trees = []
        for tree in trees:
            if tree:
                n += 1
                fpos.append(text)
                break
    score = max(0, p-n)
    return score, p, n, fneg, fpos
