"""Functions for CFG testing"""

from nltk_light.parse.chart import ChartParser
from nltk_light.grammar import CFG
from nltk_light.tokenize.regexp import wordpunct_tokenize

def test_cfg(string):
    '''Compute score based on CFG input'''
    pos = open('pos.txt').readlines()
    pos = [line.strip() for line in pos]

    neg = open('neg.txt').readlines()
    neg = [line.strip() for line in neg]

    lowstring = string.lower().replace("Þ", "->")
    gram = CFG.fromstring(lowstring)
    parser = ChartParser(gram)
    p = 0
    n = 0
    fneg = []
    fpos = []
    for text in pos:
        tokens = wordpunct_tokenize(text.lower())
        try:
            trees = parser.parse(tokens)
        except ValueError:
            trees = []
        if len(list(trees)) > 0:
            p += 1
        else:
            fneg.append(text)
    for text in neg:
        tokens = wordpunct_tokenize(text.lower())
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
