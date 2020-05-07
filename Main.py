from __init__ import *
from Text_editor import *
from Coreference import *

parsername = Parser(NAME)
parserpron = Parser(PRON)
parsertest = Parser(TEST)

texteditor = TextEditor(text)
notdialog = []
dialog = []
texteditor.split(text, notdialog, dialog)


"""facts1 = facts()
facts2 = facts()

numberofline = 0
numberofline1 = []
numberofline2 = []
for line in text:
    matches1 = list(parsername.findall(line))
    spans1 = [_.span for _ in matches1]
    fact1 = [_.fact for _ in matches1]
    facts1.fact = facts1.fact + fact1
    facts1.spans = facts1.spans + spans1
    for i in fact1:
        numberofline1.append(numberofline)
    matches2 = list(parserpron.findall(line))
    spans2 = [_.span for _ in matches2]
    fact2 = [_.fact for _ in matches2]
    facts2.fact = facts2.fact + fact2
    facts2.spans = facts2.spans + spans2
    for i in fact2:
        numberofline2.append(numberofline)
    facts = fact1 + fact2
    spans = spans1 + spans2
    
    numberofline += 1
facts1.numberofline=numberofline1
facts2.numberofline=numberofline2



k = 0
while k < len(facts2.numberofline):
    if facts2.fact[k].name != 'она':
        facts2.delete(k)
        k -=1
    k += 1

PERSONS = []
PERSONSNAME = []

linename = 0
SPANSPRO = []
LINESPRO = []
NAMES = []
LINESNAME = []
while linename < len(facts1.numberofline):
    namespan = facts1.spans[linename]
    name = facts1.fact[linename].first
    if len(PERSONS) == 0:
        PERSONS.append(Person(name))
        PERSONS[0].__add__(name, facts1.spans[linename], facts1.numberofline[linename])
        PERSONSNAME.append(name)
    else:
        for person in PERSONS:
            if PERSONSNAME.count(name) == 0:
                PERSONS.append(Person(name))
                PERSONS[len(PERSONS) - 1].__del__()
                PERSONS[len(PERSONS) - 1].__add__(name, namespan, facts1.numberofline[linename])
                PERSONSNAME.append(name)
            else:
                num = PERSONSNAME.index(name)
                PERSONS[num].__add__(name, namespan, facts1.numberofline[linename])
    NAMES.append(facts1.fact[linename].first)
    LINESNAME.append(facts1.numberofline[linename])
    if linename < len(facts2.numberofline):
        linenpro = linename
    else:
        break
    while facts2.numberofline[linenpro] - facts1.numberofline[linename] < 0:
        linenpro += 1
    while facts2.numberofline[linenpro] - facts1.numberofline[linename] >= 0 and facts2.numberofline[linenpro] - facts1.numberofline[linename] <= 5:
        if linenpro < len(facts2.numberofline):
            if facts2.spans[linenpro].start > facts1.spans[linename].stop:
                pro = facts2.spans[linenpro]
                if pro.start > namespan.start:
                    SPANSPRO.append(pro)
                    LINESPRO.append(facts2.numberofline[linenpro])
                    for PERSON in PERSONS:
                        if name == PERSON.isName():
                            PERSON.__add__(facts2.fact[linenpro].name,pro,facts2.numberofline[linenpro])
            else:
                break
        else:
            break

        linenpro +=1

    linename += 1



for pers in PERSONS:
    n = 0
    while n < len(pers.lines) - 1:
        m = n + 1
        while m < len(pers.lines):
            if pers.lines[m] == pers.lines[n]:
                if pers.spans[m] == pers.spans[n]:
                    pers.lines.pop(m)
                    pers.spans.pop(m)
                    pers.words.pop(m)
                else:
                    m += 1
            else:
                m += 1
            if pers.words[n] == pers.Name:
                pers.lines.pop(n)
                pers.words.pop(n)
                pers.spans.pop(n)
        n += 1

number = 0
while number < len(PERSONS) - 1:
    persline = 0
    while persline < len(PERSONS[number].lines):
        nextpersline = 0
        while nextpersline < len(PERSONS[number + 1].lines):
            if PERSONS[number].lines[persline] == PERSONS[number + 1].lines[nextpersline]:
                if PERSONS[number].spans[persline].stop < PERSONS[number + 1].spans[nextpersline].start:
                    PERSONS[number].lines.pop(persline)
                    PERSONS[number].spans.pop(persline)
                    PERSONS[number].words.pop(persline)
                    nextpersline += 1
                else:
                    PERSONS[number + 1].lines.pop(nextpersline)
                    PERSONS[number + 1].spans.pop(nextpersline)
                    PERSONS[number + 1].words.pop(nextpersline)
            else:
                nextpersline += 1
        persline += 1
    number += 1"""

coreference = Coreference(notdialog,dialog,text,parsername,parserpron)
coreferencetest = Coreference(notdialog,dialog,text, parsertest)
coreferencetest.Test()
PERSONS = coreference.FindCoreference()




file = open('newtext.txt','w')
numberofline = 0
for line in text:
    span = []
    name = ''
    for pers in PERSONS:
        i = 0
        while i < len(pers.lines):
            if pers.lines[i] == numberofline:
                name = pers.Name
                if span.count(pers.spans[i]) == 0:
                    span.append(pers.spans[i])
            i += 1

    show_spans(line, span, name, file, numberofline + 1)
    numberofline += 1


exit(0)

