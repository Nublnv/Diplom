from __init__ import *
from Text_editor import *
from Coreference import *


parsertest = Parser(TEST)


coreferencetest = Coreference(text, parsertest)
PERSONS = coreferencetest.Test()
"""PERSONS = coreference.FindCoreference()"""




file = open('newtext.txt','w')
numberofline = 0
for line in text:
    span = []
    names = []
    for pers in PERSONS:
        if pers.Name == 'NOUN':
            continue
        else:
            i = 0
            while i < len(pers.lines):
                if pers.lines[i] > numberofline:
                    break
                if pers.lines[i] == numberofline:
                    names.append(pers.Name)
                    if span.count(pers.spans[i]) == 0:
                        span.append(pers.spans[i])
                i += 1
    for s in span:
        k = span.index(s)
        while k < len(span) - 1:
            if span[k].start > span[k + 1].stop:
                tmps = span[k]
                tmpn = names[k]
                span[k] = span[k + 1]
                names[k] = names[k + 1]
                span[k + 1] = tmps
                names[k + 1] = tmpn
                continue
            k += 1
    show_spans(line, span, names, file, numberofline + 1)
    numberofline += 1


exit(0)

