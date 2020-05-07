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
        gram('NPRO')
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


def format_spans(text, spans, name):
    spans = sorted(spans)
    previous = 0
    for span in spans:
        start, stop = span
        yield text[previous:start]
        yield text[start:stop]
        yield ' ('
        yield name
        yield ')'
        previous = stop
    yield text[previous:]


def show_spans(text, spans, name, file,numberofline):
    print(''.join(format_spans(text, spans, name)))
    file.write(str(numberofline)+ '. ' + ''.join(format_spans(text, spans, name)))
    file.write('\n')

class Person:
    words = []
    spans = []
    lines = []
    forms = []
    def __init__(self, Name, Sex = None):
        self.Name =  Name
        self.Sex = Sex
        self.__del__()


    def __add__(self, word, span, line, form = None):
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
