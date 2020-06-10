from __init__ import *
from Text_editor import TextEditor

class Coreference:
    def __init__(self, text, parsername, parserpron = None):
        self.notdialog = []
        self.dialog = []
        self.parsername = parsername
        self.parserpron = parserpron
        self.text = text
        self.textEditor = TextEditor(text)

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
        self.textEditor.split(self.text, self.notdialog, self.dialog)
        self.preTest()
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
        PERSONS = self.newCoreference(facts)
        """PERSONS = self.__testCoreference(facts)"""
        return  self.__testIsGoodNpro(PERSONS)

    def preTest(self):
        text = self.textEditor.Textwithoutdialogs()
        numberofline = 0
        numberoflinename = []
        numberoflinepron = []

        facts = Testfacts()

        for line in text:
            matches = list(self.parsername.findall(line))
            tokens = list([_.tokens for _ in matches])
            if matches:
                facts.add(tokens, numberofline)
            numberofline += 1
        self.PERSONS = self.preCoreference(facts)

    def __testIsGoodNpro(self, PERSONS):
        for person in PERSONS:
            i = 0
            while i < len(person.words):
                if person.words[i] == person.Name:
                    person.delelem(i)
                    continue
                i += 1
        return PERSONS

    def __wordform(self,token):
        Names = []
        with open('first.txt', 'r') as fnames:
            for name in fnames:
                n = name.rstrip()
                Names.append(n)
        NAMES = frozenset(Names)
        number = ''
        case = ''
        gender = ''
        if token[0].normalized in NAMES:
            number = 'sing'
        form = token[0].forms[0].grams.values
        if 'nomn' in form:
            case = 'nomn'
        if 'gent' in form:
            case = 'gent'
        if 'datv' in form:
            case = 'datv'
        if 'accs' in form:
            case = 'accs'
        if 'ablt' in form:
            case = 'ablt'
        if 'loct' in form:
            case = 'loct'
        if 'voct' in form:
            case = 'voct'
        if number == '':
            if 'sing' in form:
                number = 'sing'
            if 'plur' in form:
                number = 'plur'
        if 'femn' in form:
            gender = 'femn'
        if 'masc' in form:
            gender = 'masc'
        if 'neut' in form:
            gender = 'neut'
        return Form(case,number,gender)

    def __Dismatch(self, PersonForm, TokenForm, PersonGender = None):
        if PersonForm.gender != '':
            gender = PersonForm.gender
        else:
            gender = PersonGender
        if TokenForm.gender == '':
            return False
        if gender == TokenForm.gender:
            if PersonForm.number == TokenForm.number:
                return False
            else:
                return True
        else:
            return True

    def __ValueScore(self, PersonForm, TokenForm, PersonGender = None):
        score = 0
        if PersonForm.gender != '':
            gender = PersonForm.gender
        else:
            gender = PersonGender
        if gender == TokenForm.gender:
            score += 10
        if PersonForm.case == TokenForm.case:
            score += 10
        elif PersonForm.case == 'nomn' and not TokenForm.case == 'nomn':
            score += 5
        elif not PersonForm.case == 'nomn' and TokenForm.case == 'nomn':
            score += 0
        elif not PersonForm.case == 'nomn' and not TokenForm.case == 'nomn':
            score += 10
        return score

    def __Score(self, PersonForm, TokenForm, PersonGender = None):
        if self.__Dismatch(PersonForm, TokenForm, PersonGender):
            return None
        else:
            return self.__ValueScore(PersonForm, TokenForm, PersonGender)

    def __BestFirst(self, PERSONS, token, numberofline):
        CouldPersons = []
        tokenform = self.__wordform(token)
        if tokenform.gender == 'neut':
            for person in PERSONS:
                if person.Name == 'NOUN':
                    return person

        for person in PERSONS:
            if person.lines[len(person.lines) - 1] == numberofline:
                score = self.__Score(person.forms[len(person.forms) - 1], tokenform, person.Sex)
                if score != None:
                    if person.Name =='NOUN':
                        score -= 20
                    score -= numberofline - person.lines[len(person.lines) - 1]
                    CouldPersons.append([person, score])
        if CouldPersons == []:
            MbPersons = []
            for person in PERSONS:
                score = self.__Score(person.forms[len(person.forms) - 1], tokenform, person.Sex)
                if score != None:
                    if person.Name == 'NOUN':
                        score -= 20
                    score -= numberofline - person.lines[len(person.lines) - 1]
                    MbPersons.append([person, score])

            p = 1
            persbestscore = MbPersons[0]
            bestpers = [MbPersons[0][0]]
            while p < len(MbPersons):
                if MbPersons[p][1] > persbestscore[1]:
                    bestpers = []
                    bestpers.append(MbPersons[p][0])
                elif MbPersons[p][1] == persbestscore[1]:
                    bestpers.append(MbPersons[p][0])
                p += 1
            return lastSpan(bestpers, numberofline)[0]
        else:
            p = 1
            persbestscore = CouldPersons[0]
            bestpers = [CouldPersons[0][0]]
            while p < len(CouldPersons):
                if CouldPersons[p][1] > persbestscore[1]:
                    bestpers = []
                    bestpers.append(CouldPersons[p][0])
                elif CouldPersons[p][1] == persbestscore[1]:
                    bestpers.append(CouldPersons[p][0])
                p += 1
            return lastSpan(bestpers,numberofline)[0]

    def preCoreference(self,tokens):
        Ya = frozenset({'1per', 'NPRO', 'sing'})
        Mi = frozenset({'1per', 'NPRO', 'plur'})
        Ti = frozenset({'2per', 'NPRO', 'sing'})
        Vi = frozenset({'2per', 'NPRO', 'plur'})
        On = frozenset({'3per', 'Anph', 'NPRO', 'sing', 'masc'})
        Ona = frozenset({'3per', 'Anph', 'NPRO', 'sing', 'femn'})

        def Moi(token):
            return True if token[0].normalized == 'мой' else False

        Names = []
        with open('first.txt', 'r') as fnames:
            for name in fnames:
                n = name.rstrip()
                Names.append(n)
        NAMES = frozenset(Names)

        numberofline = 0
        PERSONS = []
        PERSONSNAME = []

        while numberofline < len(self.text):

            if tokens.numberoflines.count(numberofline):
                indexoftokens = tokens.numberoflines.index(numberofline)
                for token in tokens.tokens[indexoftokens]:
                    tokenform = token[0].forms[0].grams.values
                    if Ya.issubset(tokenform) or Mi.issubset(tokenform) or Moi(token):
                        if len(PERSONS) == 0:
                            PERSONS.append(Person('автор', ''))
                            PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                              self.__wordform(token))
                            PERSONSNAME.append({'автор', ''})
                        else:
                            if PERSONSNAME.count({'автор', ''}):
                                PERSONS[PERSONSNAME.index({'автор', ''})].__add__(token[0].value, token[0].span,
                                                                                  numberofline,
                                                                                  self.__wordform(token))
                            else:
                                PERSONS.append(Person('автор', ''))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({'автор', ''})
                        continue
                    if Vi.issubset(tokenform) or Ti.issubset(tokenform):
                        if len(PERSONS) == 0:
                            PERSONS.append(Person('читатель', ''))
                            PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                              self.__wordform(token))
                            PERSONSNAME.append({'читатель', ''})
                        else:
                            if PERSONSNAME.count({'читатель', ''}):
                                PERSONS[PERSONSNAME.index({'читатель', ''})].__add__(token[0].value, token[0].span,
                                                                                     numberofline,
                                                                                     self.__wordform(token))
                            else:
                                PERSONS.append(Person('читатель', ''))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({'читатель', ''})
                        continue
                    if On.issubset(tokenform):
                        if len(PERSONS) == 0:
                            PERSONS.append(Person('мастер', 'masc'))
                            PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                              self.__wordform(token))
                            PERSONSNAME.append({'мастер', 'masc'})
                        else:
                            countofmasc = 0
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == 'masc':
                                        countofmasc += 1
                            if countofmasc != 0:
                                Mascs = []
                                i = 0
                                indexoflastmasc = 0
                                while i < countofmasc:
                                    while True:
                                        if 'masc' in PERSONSNAME[indexoflastmasc]:
                                            break
                                        else:
                                            indexoflastmasc += 1
                                    Mascs.append(PERSONS[indexoflastmasc])
                                    i += 1
                                    indexoflastmasc += 1
                                maxline = 0
                                maxspan = []
                                indexoflastmasc = 0
                                n = []
                                for m in Mascs:
                                    """if m.forms[len(m.forms) - 1] == token[0].forms[0].grams.values:"""
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
                                """if n != []:
                                    if n.forms[len(n.forms) - 1] == token[0].forms[0].grams.values:"""
                                PERSONS[PERSONS.index(n)].__add__(token[0].value, token[0].span, numberofline,
                                                                  self.__wordform(token))
                            else:
                                PERSONS.append(Person('мастер', 'masc'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({'мастер', 'masc'})
                        continue
                    if Ona.issubset(tokenform):
                        if len(PERSONS) == 0:
                            PERSONS.append(Person('маргарита', 'femn'))
                            PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                              self.__wordform(token))
                            PERSONSNAME.append({'маргарита', 'femn'})
                        else:
                            countofmasc = 0
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == 'femn':
                                        countofmasc += 1
                            if countofmasc != 0:
                                Mascs = []
                                i = 0
                                indexoflastmasc = 0
                                while i < countofmasc:
                                    while True:
                                        if 'femn' in PERSONSNAME[indexoflastmasc]:
                                            break
                                        else:
                                            indexoflastmasc += 1
                                    Mascs.append(PERSONS[indexoflastmasc])
                                    i += 1
                                    indexoflastmasc += 1
                                maxline = 0
                                maxspan = []
                                indexoflastmasc = 0
                                n = []
                                for m in Mascs:
                                    if m.forms[len(m.forms) - 1] == self.__wordform(token):
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
                                if n != []:
                                    if n.forms[len(n.forms) - 1] == self.__wordform(token):
                                        PERSONS[PERSONS.index(n)].__add__(token[0].value, token[0].span,
                                                                          numberofline, self.__wordform(token))
                            else:
                                PERSONS.append(Person('маргарита', 'femn'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({'маргарита', 'femn'})
                        continue
                    if token[0].normalized in NAMES:
                        gender = ''
                        if token[0].forms[0].grams.gender.female:
                            gender = 'femn'
                        if token[0].forms[0].grams.gender.male:
                            gender = 'masc'
                        if len(PERSONS) == 0:
                            PERSONS.append(Person(token[0].normalized, gender))
                            PERSONS[len(PERSONS) - 1].__add__(token[0].normalized, token[0].span, numberofline,
                                                              self.__wordform(token))
                            PERSONSNAME.append({token[0].normalized, gender})
                        else:
                            n = None
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == token[0].normalized:
                                        n = PERSONSNAME.index(p)
                                        break
                            if n != None:
                                PERSONS[n].__add__(token[0].normalized, token[0].span, numberofline,
                                                   self.__wordform(token))
                            else:
                                PERSONS.append(Person(token[0].normalized, gender))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].normalized, token[0].span, numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({token[0].normalized, gender})
                            continue
            numberofline += 1
        textEditor = TextEditor(self.text, PERSONS)
        textEditor.NamesofDialog(self.dialog, self.notdialog)
        return PERSONS

    def newCoreference(self,tokens):
        textEditor = TextEditor(self.text, self.dialog, self.notdialog)
        fper = frozenset({'1per', 'NPRO'})
        sper = frozenset({'2per', 'NPRO'})
        tper = frozenset({'3per', 'Anph', 'NPRO', 'sing'})
        noun = frozenset({'NOUN'})
        gramname = frozenset({'Name'})
        gramsurn = frozenset({'Surn'})
        grampatr = frozenset({'Patr'})

        def Moi(token):
            return True if token[0].normalized == 'мой' else False
        Names = []
        with open('first.txt', 'r') as fnames:
            for name in fnames:
                n = name.rstrip()
                Names.append(n)
        NAMES = frozenset(Names)
        numberofline = 0
        PERSONS = []
        PERSONSNAME = []


        while numberofline < len(self.text):
            flag = 0
            numberofdialog = None
            for nd in self.notdialog:
                if nd.numberoflines.count(numberofline):
                    flag = 1
                    break
            for d in self.dialog:
                if d.numberoflines.count(numberofline):
                    flag = -1
                    numberofdialog = self.dialog.index(d)
                    break

            if tokens.numberoflines.count(numberofline):
                indexoftokens = tokens.numberoflines.index(numberofline)
                for token in tokens.tokens[indexoftokens]:
                    tokenform = token[0].forms[0].grams.values

                    if flag == 1:
                        if fper.issubset(tokenform) or Moi(token):
                            if len(PERSONS) == 0:
                                PERSONS.append(Person('автор'))
                                PERSONS[0].__add__(token[0].value,token[0].span, numberofline, self.__wordform(token))
                                PERSONSNAME.append({'автор', ''})
                            else:
                                if PERSONSNAME.count({'автор',''}):
                                    PERSONS[PERSONSNAME.index({'автор',''})].__add__(token[0].value,token[0].span, numberofline, self.__wordform(token))
                                else:
                                    PERSONS.append(Person('автор'))
                                    PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                       self.__wordform(token))
                                    PERSONSNAME.append({'автор', ''})
                        elif sper.issubset(tokenform):
                            if len(PERSONS) == 0:
                                PERSONS.append(Person('читатель'))
                                PERSONS[0].__add__(token[0].value, token[0].span, numberofline, self.__wordform(token))
                                PERSONSNAME.append({'читатель', ''})
                            else:
                                if PERSONSNAME.count({'читатель',''}):
                                    PERSONS[PERSONSNAME.index({'читатель', ''})].__add__(token[0].value,token[0].span, numberofline, self.__wordform(token))
                                else:
                                    PERSONS.append(Person('читатель'))
                                    PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                       self.__wordform(token))
                                    PERSONSNAME.append({'читатель', ''})
                        elif tper.issubset(tokenform):
                            sex = self.__wordform(token).gender
                            if len(PERSONS) == 0:
                                if sex == 'masc':
                                    PERSONS.append(Person('мастер', sex))
                                    PERSONS[0].__add__(token[0].value, token[0].span, numberofline, self.__wordform(token))
                                    PERSONSNAME.append({'мастер', sex})
                                elif sex == 'femn':
                                    PERSONS.append(Person('маргарита', sex))
                                    PERSONS[0].__add__(token[0].value, token[0].span, numberofline,
                                                       self.__wordform(token))
                                    PERSONSNAME.append({'маргарита', sex})
                                else:
                                    continue
                            else:
                                indofpers = None
                                for pers in PERSONSNAME:
                                    if indofpers != None:
                                        break
                                    for p in pers:
                                        if p == sex:
                                            indofpers = PERSONSNAME.index(pers)

                                if indofpers != None:
                                    p = self.__BestFirst(PERSONS,token,numberofline)
                                    if p.Name != 'NOUN':
                                        p.__add__(token[0].value, token[0].span, numberofline, self.__wordform(token))
                                    else:
                                        PERSONS.append(Person(p.words[len(p.words) - 1]))
                                        PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,self.__wordform(token))
                                        PERSONSNAME.append({p.words[len(p.words) - 1],''})
                                elif sex == 'femn':
                                    PERSONS.append(Person('маргарита', sex))
                                    PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                       self.__wordform(token))
                                    PERSONSNAME.append({'маргарита', sex})

                                elif sex == 'masc':
                                    PERSONS.append(Person('мастер', sex))
                                    PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                                      self.__wordform(token))
                                    PERSONSNAME.append({'мастер', sex})

                        elif token[0].normalized in NAMES:
                            gender = ''
                            if token[0].forms[0].grams.gender.female:
                                gender = 'femn'
                            if token[0].forms[0].grams.gender.male:
                                gender = 'masc'
                            n = None
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == token[0].normalized:
                                        n = PERSONSNAME.index(p)
                            if n != None:
                                PERSONS[n].__add__(token[0].normalized, token[0].span, numberofline,
                                                   self.__wordform(token))
                            else:
                                PERSONS.append(Person(token[0].normalized, gender))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].normalized, token[0].span,
                                                                  numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({token[0].normalized, gender})
                        else:
                            if noun.issubset(tokenform) and not gramname.issubset(tokenform) and not gramsurn.issubset(tokenform) and \
                                    not grampatr.issubset(tokenform):
                                if len(PERSONS) == 0:
                                    PERSONS.append(Person('NOUN'))
                                    PERSONS[0].__add__(token[0].normalized, token[0].span,
                                                                  numberofline,
                                                                  self.__wordform(token))
                                    PERSONSNAME.append({'NOUN',''})
                                else:
                                    ind = -1
                                    for pers in PERSONSNAME:
                                        for n in pers:
                                            if n == 'NOUN':
                                                ind = PERSONSNAME.index(pers)
                                                break
                                    if ind != -1:
                                        PERSONS[ind].__add__(token[0].normalized, token[0].span,
                                                                  numberofline,
                                                                  self.__wordform(token))
                                    else:
                                        PERSONS.append(Person('NOUN'))
                                        PERSONS[len(PERSONS) - 1].__add__(token[0].normalized, token[0].span,
                                                                  numberofline,
                                                                  self.__wordform(token))
                                        PERSONSNAME.append({'NOUN',''})
                    if flag == -1:
                        if self.dialog[numberofdialog].owner.count('') != 0:
                            textEditor.NamesDialog(numberofdialog, PERSONS)
                        if fper.issubset(tokenform):
                            for person in PERSONS:
                                if person.Name == self.dialog[numberofdialog].owner[self.dialog[numberofdialog].numberoflines.index(numberofline)]:
                                    person.__add__(token[0].normalized, token[0].span,numberofline,self.__wordform(token))
                                    break
                        elif sper.issubset(tokenform):
                            for person in PERSONS:
                                owner = self.dialog[numberofdialog].owner[self.dialog[numberofdialog].numberoflines.index(numberofline)]
                                if len(self.dialog[numberofdialog].owners) == 2:
                                    if self.dialog[numberofdialog].owners.index(owner) == 0:
                                        if person.Name == self.dialog[numberofdialog].owners[1]:
                                            person.__add__(token[0].normalized, token[0].span, numberofline, self.__wordform(token))
                                            break
                                    elif self.dialog[numberofdialog].owners.index(owner) == 1:
                                        if person.Name == self.dialog[numberofdialog].owners[0]:
                                            person.__add__(token[0].normalized, token[0].span, numberofline, self.__wordform(token))
                                            break
                                else:
                                    PersonCouldBeInDialog = []
                                    for person in PERSONS:
                                        if self.dialog[numberofdialog].owners.count(person.Name) == 0:
                                            PersonCouldBeInDialog.append(person)
                                    p = self.__BestFirst(PersonCouldBeInDialog, token, numberofline)
                                    if p.Name != 'NOUN':
                                        p.__add__(token[0].value, token[0].span, numberofline, self.__wordform(token))
                        elif tper.issubset(tokenform):
                            PersonCouldBeInDialog = []
                            for person in PERSONS:
                                if self.dialog[numberofdialog].owners.count(person.Name) == 0:
                                    PersonCouldBeInDialog.append(person)
                            p = self.__BestFirst(PersonCouldBeInDialog, token, numberofline)
                            if p.Name != 'NOUN':
                                p.__add__(token[0].value, token[0].span, numberofline, self.__wordform(token))
                            else:
                                PERSONS.append(Person(p.words[len(p.words) - 1]))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({p.words[len(p.words) - 1], ''})
                        elif token[0].normalized in NAMES:
                            gender = ''
                            if token[0].forms[0].grams.gender.female:
                                gender = 'femn'
                            if token[0].forms[0].grams.gender.male:
                                gender = 'masc'
                            n = None
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == token[0].normalized:
                                        n = PERSONSNAME.index(p)
                            if n != None:
                                PERSONS[n].__add__(token[0].normalized, token[0].span, numberofline,
                                                   self.__wordform(token))
                            else:
                                PERSONS.append(Person(token[0].normalized, gender))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].normalized, token[0].span,
                                                                  numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({token[0].normalized, gender})
            numberofline += 1
        return PERSONS

    def PersonsinLine(self,PERSONS, tokens):
        Persons = []
        Names = []
        with open('first.txt', 'r') as fnames:
            for name in fnames:
                n = name.rstrip()
                Names.append(n)
        NAMES = frozenset(Names)
        for token in tokens:
            if not token[0].normalized in NAMES:
                continue
            else:
                for person in PERSONS:
                    if token[0].normalized == person.Name:
                        Persons.append(person)
        return Persons


    def __testCoreference(self, tokens):
        self.preCoreference(tokens)
        Ya = frozenset({'1per', 'NPRO', 'sing'})
        Mi = frozenset({'1per', 'NPRO', 'plur'})
        Ti = frozenset({'2per', 'NPRO', 'sing'})
        Vi = frozenset({'2per', 'NPRO', 'plur'})
        On = frozenset({'3per', 'Anph', 'NPRO', 'sing', 'masc'})
        Ona = frozenset({'3per', 'Anph', 'NPRO', 'sing', 'femn'})
        def Moi(token):
            return True if token[0].normalized == 'мой' else False

        Names = []
        with open('first.txt', 'r') as fnames:
            for name in fnames:
                n = name.rstrip()
                Names.append(n)
        NAMES = frozenset(Names)
        numberofline = 0
        PERSONS = self.PERSONS
        PERSONSNAME = []
        for pers in PERSONS:
            PERSONSNAME.append({pers.Name, pers.Sex})

        numberofline = 0
        while numberofline < len(self.text):
            flag = 0
            for nd in self.notdialog:
                if nd.numberoflines.count(numberofline):
                    flag = 1
                    break
            for d in self.dialog:
                if d.numberoflines.count(numberofline):
                    flag = -1
                    numberofdialog = self.dialog.index(d)
                    break

            if tokens.numberoflines.count(numberofline):
                indexoftokens = tokens.numberoflines.index(numberofline)
                for token in tokens.tokens[indexoftokens]:
                    tokenform = token[0].forms[0].grams.values
                    containsid = -1
                    id = -1
                    for p in PERSONS:
                        if p.__contains__(numberofline, token[0].span) != -1:
                            containsid = PERSONS.index(p)
                            id = p.__contains__(numberofline, token[0].span)
                            break
                    """if flag == 1 or flag == 0:
                        if Ya.issubset(tokenform) or Mi.issubset(tokenform) or Moi(token):
                            if PERSONSNAME.count({'автор',''}):
                                if containsid == -1:
                                    PERSONS[PERSONSNAME.index({'автор',''})].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                                else:
                                    if PERSONS[containsid].Name != 'автор':
                                        PERSONS[containsid].delelem(id)
                                        PERSONS[PERSONSNAME.index({'автор', ''})].__add__(token[0].value, token[0].span,numberofline,self.__wordform(token))
                            else:
                                PERSONS.append(Person('автор',''))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                                PERSONSNAME.append({'автор',''})
                            continue
                        if Vi.issubset(tokenform) or Ti.issubset(tokenform):
                            if PERSONSNAME.count({'читатель',''}):
                                if containsid == -1:
                                    PERSONS[PERSONSNAME.index({'читатель',''})].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                                else:
                                    if PERSONS[containsid].Name != 'читатель':
                                        PERSONS[containsid].delelem(id)
                                        PERSONS[PERSONSNAME.index({'читатель', ''})].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                            else:
                                PERSONS.append(Person('читатель',''))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                                PERSONSNAME.append({'читатель',''})
                            continue
                        if On.issubset(tokenform):
                            countofmasc = 0
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == 'masc':
                                        countofmasc += 1
                            if countofmasc != 0:
                                Mascs = []
                                i = 0
                                indexoflastmasc = 0
                                while i < countofmasc:
                                    while True:
                                        if 'masc' in PERSONSNAME[indexoflastmasc]:
                                            break
                                        else:
                                            indexoflastmasc += 1
                                    Mascs.append(PERSONS[indexoflastmasc])
                                    i += 1
                                    indexoflastmasc += 1
                                maxline = 0
                                maxspan = []
                                indexoflastmasc = 0
                                n = []
                                for m in Mascs:
                                    num = -1
                                    if m.lines.count(numberofline):
                                        num = m.lines.index(numberofline)
                                        if m.lines[num] > maxline:
                                            maxline = m.lines[num]
                                            maxspan = m.spans[num]
                                            n = m
                                        else:
                                            if m.lines[num] == maxline:
                                                if maxspan.stop < m.spans[num].start:
                                                    maxline = m.lines[num]
                                                    maxspan = m.spans[num]
                                                    n = m
                                    else:
                                        if m.lines[len(m.lines) - 1] > maxline:
                                            maxline = m.lines[len(m.lines) - 1]
                                            maxspan = m.spans[len(m.spans) - 1]
                                            n = m
                                        else:
                                            if m.lines[len(m.lines) - 1] == maxline:
                                                if maxspan.stop < m.spans[len(m.spans) - 1].start:
                                                    maxline = m.lines[len(m.lines) - 1]
                                                    maxspan = m.spans[len(m.spans) - 1]
                                                    n = m
                                if containsid == -1:
                                    PERSONS[PERSONS.index(n)].__add__(token[0].value, token[0].span, numberofline,self.__wordform(token))
                                else:
                                    if PERSONS[containsid].Name != PERSONS[PERSONS.index(n)].Name:
                                        PERSONS[containsid].delelem(id)
                                        PERSONS[PERSONS.index(n)].__add__(token[0].value, token[0].span,numberofline,self.__wordform(token))
                            else:
                                PERSONS.append(Person('мастер', 'masc'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                                PERSONSNAME.append({'мастер', 'masc'})
                            continue
                        if Ona.issubset(tokenform):
                            countofmasc = 0
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == 'femn':
                                        countofmasc += 1
                            if countofmasc != 0:
                                Mascs = []
                                i = 0
                                indexoflastmasc = 0
                                while i < countofmasc:
                                    while True:
                                        if 'femn' in PERSONSNAME[indexoflastmasc]:
                                            break
                                        else:
                                            indexoflastmasc += 1
                                    Mascs.append(PERSONS[indexoflastmasc])
                                    i += 1
                                    indexoflastmasc += 1
                                maxline = 0
                                maxspan = []
                                indexoflastmasc = 0
                                for m in Mascs:
                                    num = -1
                                    if m.lines.count(numberofline):
                                        num = m.lines.index(numberofline)
                                        if m.lines[num] > maxline:
                                            maxline = m.lines[num]
                                            maxspan = m.spans[num]
                                            n = m
                                        else:
                                            if m.lines[num] == maxline:
                                                if maxspan.stop < m.spans[num].start:
                                                    maxline = m.lines[num]
                                                    maxspan = m.spans[num]
                                                    n = m
                                    else:
                                        if m.lines[len(m.lines) - 1] > maxline:
                                            maxline = m.lines[len(m.lines) - 1]
                                            maxspan = m.spans[len(m.spans) - 1]
                                            n = m
                                        else:
                                            if m.lines[len(m.lines) - 1] == maxline:
                                                if maxspan.stop < m.spans[len(m.spans) - 1].start:
                                                    maxline = m.lines[len(m.lines) - 1]
                                                    maxspan = m.spans[len(m.spans) - 1]
                                                    n = m
                                if containsid == -1:
                                    PERSONS[PERSONS.index(n)].__add__(token[0].value, token[0].span,
                                                                      numberofline,
                                                                      self.__wordform(token))
                                else:
                                    if PERSONS[containsid].Name != PERSONS[PERSONS.index(n)].Name:
                                        PERSONS[containsid].delelem(id)
                                        PERSONS[PERSONS.index(n)].__add__(token[0].value, token[0].span,
                                                                          numberofline,
                                                                          self.__wordform(token))
                            else:
                                PERSONS.append(Person('маргарита', 'femn'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline, self.__wordform(token))
                                PERSONSNAME.append({'маргарита', 'femn'})
                            continue
                        if token[0].normalized in NAMES:
                            gender = ''
                            if token[0].forms[0].grams.gender.female:
                                gender = 'femn'
                            if token[0].forms[0].grams.gender.male:
                                gender = 'masc'
                            n = None
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == token[0].normalized:
                                        n = PERSONSNAME.index(p)
                            if n != None:
                                PERSONS[n].__add__(token[0].normalized, token[0].span, numberofline,
                                                                  self.__wordform(token))
                            else:
                                PERSONS.append(Person(token[0].normalized, gender))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].normalized, token[0].span, numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({token[0].normalized, gender})
                            continue"""
                    if flag == -1:
                        owner = self.dialog[numberofdialog].owner[self.dialog[numberofdialog].numberoflines.index(numberofline)]
                        lastowner = ''
                        if len(self.dialog[numberofdialog].owners) > 1:
                            for lown in self.dialog[numberofdialog].owner:
                                if lown != owner:
                                    lastowner = lown
                        if Ya.issubset(tokenform) or Mi.issubset(tokenform) or Moi(token):
                            ind = 0
                            for pers in PERSONSNAME:
                                for p in pers:
                                    if p == owner:
                                        ind = PERSONSNAME.index(pers)
                                        break
                            if 'femn' in PERSONSNAME[ind]:
                                sex = 'femn'
                            else:
                                if 'masc' in PERSONSNAME[ind]:
                                    sex = 'masc'
                                else:
                                    sex = ''
                            if PERSONSNAME.count({owner, sex}):
                                PERSONS[ind].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                            else:
                                PERSONS.append(Person(owner,sex))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                                PERSONSNAME.append({owner, sex})
                            continue
                        if Ti.issubset(tokenform) or Vi.issubset(tokenform):
                            f = 0
                            ind = 0
                            for pers in PERSONS:
                                num = -1
                                if pers.lines.count(numberofline):
                                    num = pers.lines.index(numberofline)
                                elif pers.lines.count(numberofline - 2):
                                    num = pers.lines.index(numberofline - 2)
                                else:
                                    continue
                                if pers.lines[num] == numberofline or pers.lines[num] == numberofline - 2:
                                    if pers.Name != owner:
                                        f = 1
                                        ind = PERSONS.index(pers)
                                        break
                            if f == 1:
                                if 'femn' in PERSONSNAME[ind]:
                                    sex = 'femn'
                                else:
                                    if 'masc' in PERSONSNAME[ind]:
                                        sex = 'masc'
                                    else:
                                        sex = ''
                                PERSONS[ind].__add__(token[0].value, token[0].span, numberofline,self.__wordform(token))
                                continue
                            if  f == 0:
                                for pers in PERSONSNAME:
                                    for p in pers:
                                        if p == lastowner:
                                            ind = PERSONSNAME.index(pers)
                                            break
                                if 'femn' in PERSONSNAME[ind]:
                                    sex = 'femn'
                                else:
                                    if 'masc' in PERSONSNAME[ind]:
                                        sex = 'masc'
                                    else:
                                        sex = ''
                            if PERSONSNAME.count({lastowner, sex}):
                                PERSONS[ind].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                            else:
                                PERSONS.append(Person(lastowner, sex))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value, token[0].span, numberofline, self.__wordform(token))
                                PERSONSNAME.append({lastowner, sex})
                            continue
                        if On.issubset(tokenform):
                            countofmasc = 0
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == 'masc':
                                        countofmasc += 1
                            if countofmasc != 0:
                                Mascs = []
                                i = 0
                                indexoflastmasc = 0
                                while i < countofmasc:
                                    if indexoflastmasc == len(PERSONSNAME):
                                        break
                                    while True:
                                        if indexoflastmasc == len(PERSONSNAME):
                                            break
                                        if 'masc' in PERSONSNAME[indexoflastmasc]:
                                            if owner != PERSONS[indexoflastmasc].Name:
                                                break
                                            else:
                                                indexoflastmasc += 1
                                        else:
                                            indexoflastmasc += 1
                                    if indexoflastmasc < len(PERSONS):
                                        Mascs.append(PERSONS[indexoflastmasc])
                                    i += 1
                                    indexoflastmasc += 1
                                maxline = 0
                                maxspan = []
                                n = []
                                for m in Mascs:
                                    if m.lines[len(m.lines) - 1] > maxline:
                                        maxline = m.lines[len(m.lines) - 1]
                                        maxspan = m.spans[len(m.spans) - 1]
                                        n = m
                                    else:
                                        if m.lines[len(m.lines) - 1] == maxline:
                                            if maxspan.stop < m.spans[len(m.spans) - 1].start:
                                                maxline = m.lines[len(m.lines) - 1]
                                                maxspan = m.spans[len(m.spans) - 1]
                                                n = m

                                PERSONS[PERSONS.index(n)].__add__(token[0].value, token[0].span, numberofline,
                                                                          self.__wordform(token))
                            else:
                                PERSONS.append(Person('мастер', 'masc'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline,self.__wordform(token))
                                PERSONSNAME.append({'мастер', 'masc'})
                            continue
                        if Ona.issubset(tokenform):
                            countofmasc = 0
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == 'femn':
                                        countofmasc += 1
                            if countofmasc != 0:
                                Mascs = []
                                i = 0
                                indexoflastmasc = 0
                                while i < countofmasc:
                                    if indexoflastmasc == len(PERSONSNAME):
                                        break
                                    while True:
                                        if indexoflastmasc == len(PERSONSNAME):
                                            break
                                        if 'femn' in PERSONSNAME[indexoflastmasc]:
                                            if owner != PERSONS[indexoflastmasc].Name:
                                                break
                                            else:
                                                indexoflastmasc += 1
                                        else:
                                            indexoflastmasc += 1
                                    if indexoflastmasc < len(PERSONS):
                                        Mascs.append(PERSONS[indexoflastmasc])
                                    i += 1
                                    indexoflastmasc += 1
                                maxline = 0
                                maxspan = []
                                n = []
                                for m in Mascs:
                                    if m.forms[len(m.forms) - 1] == self.__wordform(token):
                                        if m.lines[len(m.lines) - 1] > maxline:
                                            maxline = m.lines[len(m.lines) - 1]
                                            maxspan = m.spans[len(m.spans) - 1]
                                            n = m
                                        else:
                                            if m.lines[len(m.lines) - 1] == maxline:
                                                if maxspan.stop < m.spans[len(m.spans) - 1].start:
                                                    maxline = m.lines[len(m.lines) - 1]
                                                    maxspan = m.spans[len(m.spans) - 1]
                                                    n = m
                                if n != []:
                                    if n.forms[len(n.forms) - 1] == self.__wordform(token):
                                        PERSONS[PERSONS.index(n)].__add__(token[0].value,token[0].span,numberofline, self.__wordform(token))
                            else:
                                PERSONS.append(Person('маргарита', 'femn'))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].value,token[0].span,numberofline, self.__wordform(token))
                                PERSONSNAME.append({'маргарита', 'femn'})
                            continue
                        if token[0].normalized in NAMES:
                            gender = ''
                            if token[0].forms[0].grams.gender.female:
                                gender = 'femn'
                            if token[0].forms[0].grams.gender.male:
                                gender = 'masc'
                            n = None
                            for p in PERSONSNAME:
                                for c in p:
                                    if c == token[0].normalized:
                                        n = PERSONSNAME.index(p)
                                        break
                            if n != None:
                                PERSONS[n].__add__(token[0].normalized, token[0].span, numberofline,
                                                                  self.__wordform(token))
                            else:
                                PERSONS.append(Person(token[0].normalized, gender))
                                PERSONS[len(PERSONS) - 1].__add__(token[0].normalized, token[0].span, numberofline,
                                                                  self.__wordform(token))
                                PERSONSNAME.append({token[0].normalized, gender})
                            continue







            numberofline += 1
        return PERSONS




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