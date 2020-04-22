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
from yargy.tokenizer import MorphTokenizer
from yargy import interpretation as interp
from yargy.interpretation import fact, attribute
from natasha.markup import show_markup, show_json
from natasha.data import load_dict
from yargy.relations import gnc_relation
from natasha import NamesExtractor
from nltk import sent_tokenize, download


extractor = NamesExtractor()

PER3 = gram('3per')
NPRO = gram('NPRO')
NOMN = gram('nomn')
PER1 = gram('1per')
PER2 = gram('2per')
FEM = gram('femn')


Pron = fact(
    'Pronoun',
    ['name']
)


PRON = rule(or_(
    and_(
        PER3,
        NPRO,
        NOMN,
        FEM
    ).interpretation(Pron.name.inflected()),
    and_(
        PER1,
        NPRO,
        FEM
    ).interpretation(Pron.name.inflected()),
    and_(
        PER2,
        NPRO,
        FEM
    ).interpretation(Pron.name.inflected())
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

parsername = Parser(NAME)
parserpron = Parser(PRON)

lines = []
txt =[]
with open ('text.txt') as file:
    for line in file:
        l = line.rstrip()
        lines.append(l)

txt = ''.join(lines)
text = []
sentences = sent_tokenize(txt,'russian')
for sentence in sentences:
    text.append(sentence)

class facts:
    fact = []
    spans = []
    numberofline = []
    def __init__(self):
        """Constructor"""
        pass

    def reverse(self):
        self.fact.reverse()
        self.spans.reverse()
        self.numberofline.reverse()

    def delete(self,num):
        self.fact.pop(num)
        self.spans.pop(num)
        self.numberofline.pop(num)


facts1 = facts()
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
    matches2 =list(parserpron.findall(line))
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



linename = 0
SPANSPRO = []
LINESPRO = []
NAMES = []
LINESNAME = []
while linename < len(facts1.numberofline):
    name = facts1.spans[linename]
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
                if pro.start > name.start:
                    SPANSPRO.append(pro)
                    LINESPRO.append(facts2.numberofline[linenpro])
            else:
                break
        else:
            break

        linenpro +=1

    linename += 1
k = 0
while k < len(LINESPRO):
    j = k + 1
    while j<len(LINESPRO):
        if LINESPRO[k] == LINESPRO[j] and SPANSPRO[k] == LINESPRO[j]:
            LINESPRO.pop(j)
            SPANSPRO.pop(j)
            j -= 1
        j += 1
    k += 1

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


def show_spans(text, spans, name, file):
    print(''.join(format_spans(text, spans, name)))
    file.write(''.join(format_spans(text, spans, name)))
    file.write('\n')




numberofline = 0
i = 0
j = 0
span = []
name = ''
file = open('newtext.txt','w')

for line in text:
    if numberofline == LINESNAME[j]:
        name = NAMES[j]
        j += 1
    while LINESPRO[i] == numberofline and i < len(LINESPRO):
        span.append(SPANSPRO[i])
        if i < len(LINESPRO)-1:
            i += 1
    show_spans(line, span, name, file)
    if len(span) != 0:
        span.pop()
    numberofline += 1


exit(0)

