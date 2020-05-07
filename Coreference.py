from __init__ import *

class Coreference:
    notdialog = []
    dialog = []
    def __init__(self, notdialog, dialog, text, parsername, parserpron = None):
        self.notdialog = notdialog
        self.dialog = dialog
        self.parsername = parsername
        self.parserpron = parserpron
        self.text = text

    def FindCoreference(self):
        numberofline = 0
        numberoflinename = []
        numberoflinepron = []

        factsname = facts()
        factspron = facts()

        for line in self.text:
            matchesname = list(self.parsername.findall(line))
            spanname = [_.span for _ in matchesname]
            factname = [_.fact for _ in matchesname]
            factsname.fact = factsname.fact + factname
            factsname.spans = factsname.spans + spanname
            for f in factname:
                numberoflinename.append(numberofline)
            matchespron = list(self.parserpron.findall(line))
            spanpron = [_.span for _ in matchespron]
            factpron = [_.fact for _ in matchespron]
            factspron.fact = factspron.fact + factpron
            factspron.spans = factspron.spans + spanpron
            for f in factpron:
                numberoflinepron.append(numberofline)
            numberofline += 1
        factsname.numberofline = numberoflinename
        factspron.numberofline = numberoflinepron

        factspron = self.__isGoodPron(factspron)
        PERSONS = self.__SortByPerson(factsname, factspron, self.notdialog, self.dialog)
        self.__delrepeat(PERSONS)
        return PERSONS

    def Test(self):
        numberofline = 0
        numberoflinename = []
        numberoflinepron = []

        facts = Testfacts()

        for line in self.text:
            matches = list(self.parsername.findall(line))
            tokens = list([_.tokens for _ in matches])
            if matches:
                facts.add(tokens, numberofline)
            numberofline += 1
        """self.__testIsGoodNpro(facts)"""
        self.__testCoreference(facts)

    def __testIsGoodNpro(self,tokensspron):
        token = 0
        while token < len(tokensspron.tokens):
            t = 0
            while t < len(tokensspron.tokens[token]):
                flag = False
                if tokensspron.tokens[token][t][0].normalized != 'я':
                    flag = True
                if flag:
                    tokensspron.tokens[token].pop(t)
                    continue
                t += 1
            if tokensspron.tokens[token] == []:
                tokensspron.tokens.pop(token)
                continue
        token += 1
        pass

    def __testCoreference(self, tokens):
        Ya = frozenset({'1per', 'NPRO', 'sing'})
        Mi = frozenset({'1per', 'NPRO', 'plur'})
        Ti = frozenset({'2per', 'NPRO', 'sing'})
        Vi = frozenset({'2per', 'NPRO', 'plur'})
        On = frozenset({'3per', 'Anph', 'NPRO', 'sing', 'masc'})
        Ona = frozenset({'3per', 'Anph', 'NPRO', 'sing', 'femn'})

        numberofline = 0
        PERSONS = []
        PERSONSNAME = []
        while numberofline < len(self.text):
            flag = 0
            for nd in self.notdialog:
                if nd.numberoflines.count(numberofline):
                    flag = 1
                    break
            for d in self.dialog:
                if d.numberoflines.count(numberofline):
                    flag = -1
                    break

            if tokens.numberoflines.count(numberofline):
                indexoftokens = tokens.numberoflines.index(numberofline)
                for token in tokens.tokens[indexoftokens]:
                    tokenform = token[0].forms[0].grams.values
                    if flag == 1:
                        if Ya.issubset(tokenform) or Mi.issubset(tokenform):
                            if len(PERSONS) == 0:
                                PERSONS.append(Person('автор'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                PERSONSNAME.append('автор')
                            else:
                                if PERSONSNAME.count('автор'):
                                    PERSONS[PERSONSNAME.index('автор')].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                else:
                                    PERSONS.append(Person('автор'))
                                    PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                    PERSONSNAME.append('автор')
                            continue
                        if Vi.issubset(tokenform) or Ti.issubset(tokenform):
                            if len(PERSONS) == 0:
                                PERSONS.append(Person('читатель'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                PERSONSNAME.append('читатель')
                            else:
                                if PERSONSNAME.count('читатель'):
                                    PERSONS[PERSONSNAME.index('читатель')].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                else:
                                    PERSONS.append(Person('читатель'))
                                    PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                    PERSONSNAME.append('читатель')
                            continue
                        if On.issubset(tokenform):
                            if len(PERSONS) == 0:
                                PERSONS.append(Person('мастер', 'masc'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                PERSONSNAME.append({'мастер', 'masc'})
                            else:
                                countofmasc = 0
                                for p in PERSONSNAME:
                                    for c in p:
                                        if c == 'masc':
                                            countofmasc += 1

                                if countofmasc != 0:
                                    Mascs = [countofmasc]
                                    i = 0
                                    indexoflastmasc = 0
                                    while i < countofmasc:
                                        while True:
                                            if 'masc' in PERSONSNAME[indexoflastmasc] :
                                                break
                                            else:
                                                indexoflastmasc += 1

                                        Mascs[i] = PERSONS[indexoflastmasc]
                                        i += 1
                                    maxline = 0
                                    maxspan = []
                                    indexoflastmasc = 0
                                    n = []
                                    for m in Mascs:
                                        if m.lines[len(m.lines) - 1] > maxline:
                                            maxline = m.lines[len(m.lines) - 1]
                                            maxspan = m.spans[len(m.spans) - 1]
                                            indexoflastmasc = Mascs.index(m)
                                            n = m
                                        else:
                                            if m.lines[len(m.lines) - 1] == maxline:
                                                if maxspan.stop < m.spans[len(m.spans) - 1].start:
                                                    maxline = m.lines[len(m.lines) - 1]
                                                    maxspan = m.spans[len(m.spans) - 1]
                                                    indexoflastmasc = Mascs.index(m)
                                                    n = m
                                    PERSONS[PERSONS.index(n)].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                else:
                                    PERSONS.append(Person('мастер', 'masc'))
                                    PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                    PERSONSNAME.append({'мастер', 'masc'})
                            continue
                        if Ona.issubset(tokenform):
                            if len(PERSONS) == 0:
                                PERSONS.append(Person('марагарита', 'femn'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                PERSONSNAME.append({'мастер', 'masc'})
                            else:
                                countofmasc = 0
                                for p in PERSONSNAME:
                                    for c in p:
                                        if c == 'femn':
                                            countofmasc += 1
                                if countofmasc != 0:
                                    Mascs = [countofmasc]
                                    i = 0
                                    indexoflastmasc = 0
                                    while i < countofmasc:
                                        while True:
                                            if 'femn' in PERSONSNAME[indexoflastmasc]:
                                                break
                                            else:
                                                indexoflastmasc += 1
                                        Mascs[i] = PERSONS[indexoflastmasc]
                                        i += 1
                                    maxline = 0
                                    maxspan = []
                                    indexoflastmasc = 0
                                    n = []
                                    for m in Mascs:
                                        if m.lines[len(m.lines) - 1] > maxline:
                                            maxline = m.lines[len(m.lines) - 1]
                                            maxspan = m.spans[len(m.spans) - 1]
                                            indexoflastmasc = Mascs.index(m)
                                            n = m
                                        else:
                                            if m.lines[len(m.lines) - 1] == maxline:
                                                if maxspan.stop < m.spans[len(m.spans) - 1].start:
                                                    maxline = m.lines[len(m.lines) - 1]
                                                    maxspan = m.spans[len(m.spans) - 1]
                                                    indexoflastmasc = Mascs.index(m)
                                                    n = m
                                    PERSONS[PERSONS.index(n)].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                else:
                                    PERSONS.append(Person('марагарита', 'femn'))
                                    PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,token[0].forms[0].grams.values)
                                    PERSONSNAME.append({'марагарита', 'femn'})
                            continue








            numberofline += 1




    def __isGoodPron(self, factspron):
        k = 0
        while k < len(factspron.numberofline):
            """if factspron.fact[k].name != 'он' and factspron.fact[k].name != 'я' and factspron.fact[k].name != 'ты' and factspron.fact[k].name != 'вы':"""
            if factspron.fact[k].name != 'она' and factspron.fact[k].name != 'я' and factspron.fact[k].name != 'ты' and factspron.fact[k].name != 'вы':
                factspron.delete(k)
            else:
                k += 1
        return factspron

    def __SortByPerson(self, factsname, factspron, notdialog, dialog):
        PERSONS = []
        PERSONSNAME = []
        linename = 0
        lastname1 = ''
        nollastname1 = 0
        lastname2 = ''
        nollastname2 = 0
        while linename < len(factsname.numberofline):
            flag = 0
            for nd in notdialog:
                if nd.numberoflines.count(linename):
                    flag = 1
                    break
            for d in dialog:
                if d.numberoflines.count(linename):
                    flag = -1
                    break
            if flag == 1:
                name = factsname.fact[linename].first
                if len(PERSONS) == 0:
                    PERSONS.append(Person(name))
                    PERSONS[0].__add__(name,factsname.spans[linename],factsname.numberofline[linename])
                    lastname1 = name
                    nollastmane1 = linename
                    PERSONSNAME.append(name)
                else:
                    for person in PERSONS:
                        if PERSONSNAME.count(name) == 0:
                            PERSONS.append(Person(name))
                            PERSONSNAME.append(name)
                            PERSONS[len(PERSONS) - 1].__del__()
                            PERSONS[len(PERSONS) - 1].__add__(name, factsname.spans[linename],factsname.numberofline[linename])
                            lastname2 = lastname1
                            nollastmane2 = nollastname1
                            lastname1 = name
                            nollastmane1 = linename
                            break
                        else:
                            num = PERSONSNAME.index(name)
                            PERSONS[num].__add__(name, factsname.spans[linename],factsname.numberofline[linename])
                            break
                if linename < len(factspron.numberofline):
                    linenpro = 0
                else:
                    break
                while factspron.numberofline[linenpro] - factsname.numberofline[linename] < 0:
                    if linenpro < len(factspron.numberofline) - 1:
                        linenpro += 1
                    else: break
                if linenpro < len(factspron.numberofline):
                    while factspron.numberofline[linenpro] - factsname.numberofline[linename] >= 0 and factspron.numberofline[linenpro] - factsname.numberofline[linename] <= 5:
                        if factspron.numberofline[linenpro] == factsname.numberofline[linename]:
                            if factspron.spans[linenpro].start > factsname.spans[linename].stop:
                                num = PERSONSNAME.index(factsname.fact[linename].first)
                                PERSONS[num].__add__(factspron.fact[linenpro],factspron.spans[linenpro],factspron.numberofline[linenpro])
                                lastname2 = lastname1
                                nollastmane2 = nollastname1
                                lastname1 = name
                                nollastmane1 = linename
                        else:
                            num = PERSONSNAME.index(factsname.fact[linename].first)
                            PERSONS[num].__add__(factspron.fact[linenpro], factspron.spans[linenpro], factspron.numberofline[linenpro])
                            lastname2 = lastname1
                            nollastmane2 = nollastname1
                            lastname1 = name
                            nollastmane1 = linename
                        if linenpro + 1 < len(factspron.numberofline):
                            linenpro += 1
                        else:
                            break
            if  flag == -1:
                name = 'маргарита'
                if len(PERSONS) == 0:
                    PERSONS.append(Person(name))
                    PERSONSNAME.append(name)
                    PERSONS[0].__add__(name,factsname.spans[linename],factsname.numberofline[linename])
                    lastname1 = name
                    nollastmane1 = linename
                    PERSONSNAME.append(name)
                else:
                    for person in PERSONS:
                        if PERSONSNAME.count(name) == 0:
                            PERSONS.append(Person(Name))
                            PERSONSNAME.append(name)
                            PERSONS[len(PERSONS) - 1].__del__()
                            PERSONS[len(PERSONS) - 1].__add__(name, factsname.spans[linename],factsname.numberofline[linename])
                            lastname2 = lastname1
                            nollastmane2 = nollastname1
                            lastname1 = name
                            nollastmane1 = linename
                        else:
                            num = PERSONSNAME.index(name)
                            PERSONS[num].__add__(name, factsname.spans[linename],factsname.numberofline[linename])
                if linename < len(factspron.numberofline):
                    linenpro = linename
                else:
                    break
                while factspron.numberofline[linenpro] - factsname.numberofline[linename]< 0:
                    if linenpro < len(factspron.numberofline) - 1:
                        linenpro += 1
                    else: break
                if linenpro < len(factspron.numberofline):
                    while factspron.numberofline[linenpro] - factsname.numberofline[linename] >= 0 \
                            and factspron.numberofline[linenpro] - factsname.numberofline[linename] <= 2:
                        if factspron.numberofline[linenpro] == factsname.numberofline[linename]:
                            if factspron.spans[linenpro].start > factsname.spans[linename].start:
                                if PERSONSNAME.count(factsname.fact[linename].first):
                                    num = PERSONSNAME.index(factsname.fact[linename].first)
                                    PERSONS[num].__add__(factspron.fact[linenpro],factspron.spans[linenpro],factspron.numberofline[linenpro])
                                    lastname2 = lastname1
                                    nollastmane2 = nollastname1
                                    lastname1 = name
                                    nollastmane1 = linename
                        else:
                            if PERSONSNAME.count(factsname.fact[linename].first):
                                num = PERSONSNAME.index(factsname.fact[linename].first)
                                PERSONS[num].__add__(factspron.fact[linenpro], factspron.spans[linenpro], factspron.numberofline[linenpro])
                                lastname2 = lastname1
                                nollastmane2 = nollastname1
                                lastname1 = name
                                nollastmane1 = linename
                        if linenpro + 1 < len(factspron.numberofline):
                            linenpro += 1
                        else:
                            break
            linename += 1
        return PERSONS

    def __delrepeat(self, PERSONS):
        number = 0
        while number < len(PERSONS) - 1:
            persline = 0
            while persline < len(PERSONS[number].lines):
                nextpersline = 0
                while nextpersline < len(PERSONS[number + 1].lines):
                    if PERSONS[number].lines[persline] == PERSONS[number + 1].lines[nextpersline]:
                        if PERSONS[number].spans[persline].start < PERSONS[number + 1].spans[nextpersline].start:
                            if PERSONS[number].words[persline] != PERSONS[number].Name:
                                PERSONS[number].lines.pop(persline)
                                PERSONS[number].spans.pop(persline)
                                PERSONS[number].words.pop(persline)
                            nextpersline += 1
                        else:
                            if PERSONS[number].spans[persline].start > PERSONS[number + 1].spans[nextpersline].start:
                                if PERSONS[number + 1].words[nextpersline] != PERSONS[number + 1].Name:
                                    PERSONS[number + 1].lines.pop(nextpersline)
                                    PERSONS[number + 1].spans.pop(nextpersline)
                                    PERSONS[number + 1].words.pop(nextpersline)
                                else:
                                    nextpersline += 1
                            else:
                                i = persline
                                while PERSONS[number].words[i] != PERSONS[number].Name:
                                    if i > 0:
                                        i -= 1
                                    else:
                                        break
                                j = nextpersline
                                while PERSONS[number + 1].words[j] != PERSONS[number + 1].Name:
                                    if j > 0:
                                        j -= 1
                                    else:
                                        break

                                if PERSONS[number].lines[i] > PERSONS[number + 1].lines[j]:
                                    if PERSONS[number + 1].words[nextpersline] != PERSONS[number + 1].Name:
                                        PERSONS[number + 1].lines.pop(nextpersline)
                                        PERSONS[number + 1].spans.pop(nextpersline)
                                        PERSONS[number + 1].words.pop(nextpersline)
                                    else:
                                        nextpersline += 1
                                else:
                                    if PERSONS[number].lines[i] < PERSONS[number + 1].lines[j]:
                                        if PERSONS[number].words[persline] != PERSONS[number].Name:
                                            PERSONS[number].lines.pop(persline)
                                            PERSONS[number].spans.pop(persline)
                                            PERSONS[number].words.pop(persline)
                                        nextpersline += 1
                                    else:
                                        if PERSONS[number].spans[i].start < PERSONS[number + 1].spans[i].start:
                                            if PERSONS[number].words[persline] != PERSONS[number].Name:
                                                PERSONS[number].lines.pop(persline)
                                                PERSONS[number].spans.pop(persline)
                                                PERSONS[number].words.pop(persline)
                                            nextpersline += 1
                                        else:
                                            if PERSONS[number + 1].words[nextpersline] != PERSONS[number + 1].Name:
                                                PERSONS[number + 1].lines.pop(nextpersline)
                                                PERSONS[number + 1].spans.pop(nextpersline)
                                                PERSONS[number + 1].words.pop(nextpersline)
                                            else:
                                                nextpersline += 1
                    else:
                        nextpersline += 1
                persline += 1
            number += 1

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
                            continue
                    if pers.words[n] == pers.Name:
                        pers.lines.pop(n)
                        pers.words.pop(n)
                        pers.spans.pop(n)
                        continue
                    m += 1
                n += 1

        return PERSONS