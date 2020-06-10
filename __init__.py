from yargy import (
    Parser,
    or_, rule, and_, not_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    eq, in_, dictionary,
    type, gram
)
from random import seed, sample
from yargy.tokenizer import Tokenizer
from yargy import interpretation as interp
from yargy.interpretation import fact, attribute
from natasha.markup import show_markup, show_json
from natasha.data import load_dict
from yargy.relations import gnc_relation
from natasha import NamesExtractor
from nltk import sent_tokenize, download
from yargy.predicates import  normalized
import pymorphy2
import copy

Pron = fact(
    'Pronoun',
    ['name']
)


PRON = rule(or_(
    and_(
        gram('3per'),
        gram('Anph'),
        gram('NPRO')
    ).interpretation(Pron.name.normalized()),
    and_(
        gram('1per'),
        gram('NPRO')
    ).interpretation(Pron.name.normalized()),
    and_(
        gram('2per'),
        gram('NPRO')
    ).interpretation(Pron.name.normalized()),
    and_(
        gram('ADJF'),
        gram('Apro')
    ).interpretation(Pron.name.normalized())
)
).interpretation(Pron)

Name = fact(
    'Name',
    ['first','last']
)

firstnames = []
with open('first.txt') as file:
    for line in file:
        firstname = line.rstrip()
        firstnames.append(firstname)

lastnames = []
with open('last.txt') as file:
    for line in file:
        lastname = line.rstrip()
        lastnames.append(lastname)

FIRST = morph_pipeline(firstnames).interpretation(Name.first.normalized())
LAST = morph_pipeline(lastnames).interpretation(Name.last.normalized())

NAME = or_(
    rule(FIRST),
    rule(LAST),
    rule(FIRST,LAST),
    rule(LAST,FIRST)
).interpretation(Name)

TEST = or_(
    rule(
        or_(
            gram('NPRO'),
            and_(
                gram('ADJF'),
                gram('Apro')
            ),
            gram('NOUN')
        )
    ),
        NAME
)


class Testfacts:
    def __init__(self, name = None):
        self.tokens = []
        self.numberoflines = []
        self.name = name

    def delete(self,num):
        self.tokens.pop(self.numberoflines[num])
        self.numberoflines.pop(num)

    def add(self, tokens, numberofline):
        self.tokens.append(tokens)
        self.numberoflines.append(numberofline)

class facts:
    fact = []
    spans = []
    numberofline = []
    def __init__(self):
        pass

    def reverse(self):
        self.fact.reverse()
        self.spans.reverse()
        self.numberofline.reverse()

    def delete(self,num):
        self.fact.pop(num)
        self.spans.pop(num)
        self.numberofline.pop(num)


def format_spans(text, spans, names):
    spans = sorted(spans)
    previous = 0
    i = 0
    for span in spans:
        start, stop = span
        yield text[previous:start]
        yield text[start:stop]
        yield ' ('
        yield names[i]
        yield ')'
        previous = stop
        i += 1
    yield text[previous:]


def show_spans(text, spans, name, file,numberofline):
    print(''.join(format_spans(text, spans, name)))
    file.write(str(numberofline)+ '. ' + ''.join(format_spans(text, spans, name)))
    file.write('\n')

class Form:
    def __init__(self, case, number, gender):
        self.case = case
        self.number = number
        self.gender = gender

class Person:

    def __init__(self, Name, Sex = None):
        self.Name =  Name
        self.Sex = Sex
        self.words = []
        self.spans = []
        self.lines = []
        self.forms = []
        self.__del__()


    def __add__(self, word, span, line, form = None):
        if self.__contains__(line, span) != -1:
            pass
        else:
            flag = 0
            for l in self.lines:
                if l < line:
                    continue
                elif l == line:
                    ind = self.lines.index(l)
                    while ind < len(self.lines):
                        if self.lines[ind] == line:
                            if self.spans[self.lines.index(l)] < span:
                                ind += 1
                            else:
                                i = self.lines.index(l)
                                self.words.insert(i, word)
                                self.lines.insert(i, line)
                                self.spans.insert(i, span)
                                if form != None:
                                    self.forms.insert(i, form)
                                break
                        else:
                            i = self.lines.index(l)
                            self.words.insert(i, word)
                            self.lines.insert(i, line)
                            self.spans.insert(i, span)
                            if form != None:
                                self.forms.insert(i, form)
                            break
                    else:
                        self.words.append(word)
                        self.spans.append(span)
                        self.lines.append(line)
                        if form != None:
                            self.forms.append(form)
                    break
                else:
                    i = self.lines.index(l)
                    self.words.insert(i, word)
                    self.lines.insert(i, line)
                    self.spans.insert(i, span)
                    if form != None:
                        self.forms.insert(i, form)
                    break
            else:
                self.words.append(word)
                self.spans.append(span)
                self.lines.append(line)
                if form != None:
                    self.forms.append(form)

    def isName(self):
        return self.Name

    def __del__(self):
        self.words = []
        self.spans = []
        self.lines = []
        self.forms = []

    def delelem(self, num):
        self.words.pop(num)
        self.lines.pop(num)
        self.spans.pop(num)
        self.forms.pop(num)

    def __contains__(self, line, spans):
        for l in self.lines:
            if l < line:
                continue
            elif l == line:
                index = self.lines.index(l)
                if self.spans[index] == spans:
                    return index
            else:
                break
        return  -1

def __RightIndex(list, value):
    returnlist = list.copy()
    returnlist.reverse()
    return len(list) - returnlist.index(value) - 1

def lastSpan(PERSONS, numberofline):
    if len(PERSONS) == 1:
        pers = PERSONS[0]
        return [pers,pers.lines[len(pers.lines) - 1], pers.spans[len(pers.spans) - 1]]
    else:
        PersonsLastSpan = []
        for person in PERSONS:
            flag = 0
            for line in person.lines:
                if line <= numberofline:
                    continue
                else:
                    flag = 1
                    i = __RightIndex(person.lines, line)
                    PersonsLastSpan.append([person, person.lines[i], person.spans[i]])
            if flag == 0:
                i = __RightIndex(person.lines, person.lines[len(person.lines) - 1])
                PersonsLastSpan.append([person, person.lines[i], person.spans[i]])
        p = 1
        maxline = PersonsLastSpan[0][1]
        maxspan = PersonsLastSpan[0][2]
        lastPerson = PersonsLastSpan[0][0]
        while p < len(PersonsLastSpan):
            if PersonsLastSpan[p][1] > maxline:
                maxline = PersonsLastSpan[p][1]
                maxspan = PersonsLastSpan[p][2]
                lastPerson = PersonsLastSpan[p][0]
            elif PersonsLastSpan[p][1] == maxline:
                if PersonsLastSpan[p][2].start > maxspan.stop:
                    maxline = PersonsLastSpan[p][1]
                    maxspan = PersonsLastSpan[p][2]
                    lastPerson = PersonsLastSpan[p][0]
                else:
                    PersonsLastSpan.pop(p)
                    continue
            else:
                PersonsLastSpan.pop(p)
                continue
            p += 1
        return [lastPerson, maxline, maxspan]