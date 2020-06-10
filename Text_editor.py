from __init__ import *

lines = []
txt =[]
with open ('text.txt') as file:
    for line in file:
        l = line.rstrip()
        lines.append(l)

txt = ' '.join(lines)
text = []
l = 0
while l < len(lines):
    line = lines[l]
    if line == '':
        lines.pop(lines.index(line))
        continue
    sentences = sent_tokenize(line,'russian')
    for sentence in sentences:
        text.append(sentence)
    l += 1

t = 0
while t < len(text):
    for l in lines:
        if text[t] in l:
            if text[t][0] == '–' or '«' in text[t]:
                while True:
                    if t == len(text) - 1:
                        break
                    newt = text[t] + ' ' + (text[t + 1])
                    if newt in l:
                        text[t] = newt
                        text.pop(t + 1)
                    else:
                        break
                break
            else:
                break
    if ', –' in text[t]:
        c = text[t].find(', –') + 1
        nt = text[t][c + 1: len(text[t]): 1]
        text[t] = text[t][0: c: 1]
        text.insert(t + 1, nt)
    if '! –' in text[t]:
        c = text[t].find('! –') + 1
        nt = text[t][c + 1: len(text[t]): 1]
        text[t] = text[t][0: c: 1]
        text.insert(t + 1, nt)
    if '? –' in text[t]:
        c = text[t].find('? –') + 1
        nt = text[t][c + 1: len(text[t]): 1]
        text[t] = text[t][0: c: 1]
        text.insert(t + 1, nt)
    if ': –' in text[t]:
        c = text[t].find(': –') + 1
        nt = text[t][c + 1: len(text[t]): 1]
        text[t] = text[t][0: c: 1]
        text.insert(t + 1, nt)
    if ': «' in text[t]:
        c = text[t].find(': «') + 1
        nt = text[t][c + 1: len(text[t]): 1]
        text[t] = text[t][0: c: 1]
        text.insert(t + 1, nt)
    if '» ' in text[t]:
        c = text[t].find('»')
        nt = text[t][c + 2: len(text[t]): 1]
        text[t] = text[t][0: c + 1: 1]
        text.insert(t + 1, nt)
    if '». ' in text[t]:
        c = text[t].find('». ')
        nt = text[t][c + 3: len(text[t]): 1]
        text[t] = text[t][0: c + 2: 1]
        text.insert(t + 1, nt)
    t += 1

class listoft:
    def __init__(self, num):
        self.number = num
        self.line = []
        self.numberoflines = []
        pass

    def lines(self):
        return  self.numberoflines

    def addline(self, line, numberofline):
        self.line.append(line)
        self.numberoflines.append(numberofline)

class listofd:
    def __init__(self, num):
        self.number = num
        self.line = []
        self.numberoflines = []
        self.owner = []
        self.lastowner1 = ''
        self.lastowner2 = ''
        self.owners = []
        pass

    def addline(self, line, numberofline):
        self.line.append(line)
        self.numberoflines.append(numberofline)
        self.owner.append('')

    def delline(self, num):
        self.line.pop(num)
        self.numberoflines.pop(num)
        self.owner.pop(num)

    def lines(self):
        return  self.numberoflines

    def __len__(self):
        return len(self.line)

    def addowner(self, owner):
        if self.owners.count(owner) == 0:
            self.owners.append(owner)
            self.lastowner2 = self.lastowner1
            self.lastowner1 = self.owners[len(self.owners) - 1]

class match:
    lines = []
    names = []

    def __add__(self, line, name):
        self.names.append(name)
        self.lines.append(line)

class TextEditor:
    text = ""
    newtext = ""
    defiz = eq("–")
    Persons = []
    spansdef = []
    numberoflinedef = []
    numberoflined = []
    startsofdialog = match()
    endsofdialog = []
    dialogs = []
    texts = []
    Names = []
    with open('first.txt', 'r') as fnames:
        for name in fnames:
            n = name.rstrip()
            Names.append(n)
    NAMES = frozenset(Names)

    def __init__(self, text, listofdialog = None, listoftext = None, persons = None):
        self.text = text
        if persons != None:
            self.Persons = persons
        self.listofdialog = listofdialog
        self.listoftext = listoftext


    def split(self,text, listoftext, listofdialog):
        t = 0
        lot = 0
        lod = 0
        while t < len(text):
            if text[t][0] == '–':
                if len(listoftext) != 0:
                    if listoftext[len(listoftext) - 1].number == lot:
                        lot += 1
                if len(listofdialog) == 0:
                    listofdialog.append(listofd(lod))
                    listofdialog[len(listofdialog) - 1].addline(text[t],t)
                else:
                    if listofdialog[len(listofdialog) - 1].number != lod:
                        listofdialog.append(listofd(lod))
                        listofdialog[len(listofdialog) - 1].addline(text[t],t)
                    else:
                        listofdialog[len(listofdialog) - 1].addline(text[t],t)
            else:
                if text[t][0] == '«':
                    if len(listoftext) != 0:
                        if listoftext[len(listoftext) - 1].number == lot:
                            lot += 1
                    if text[t][len(text[t]) - 1] != '»' and text[t][len(text[t]) - 2] != '»':
                        while text[t][len(text[t]) - 1] != '»' and text[t][len(text[t]) - 2] != '»':
                            if len(listofdialog) == 0:
                                listofdialog.append(listofd(lod))
                                listofdialog[len(listofdialog) - 1].addline(text[t], t)
                            else:
                                if listofdialog[len(listofdialog) - 1].number != lod:
                                    listofdialog.append(listofd(lod))
                                    listofdialog[len(listofdialog) - 1].addline(text[t], t)
                                else:
                                    listofdialog[len(listofdialog) - 1].addline(text[t], t)
                            t += 1
                        listofdialog[len(listofdialog) - 1].addline(text[t], t)
                    else:
                        listofdialog.append(listofd(lod))
                        listofdialog[len(listofdialog) - 1].addline(text[t], t)
                    if text[t + 2][0] == '«':
                        t += 1
                        while text[t + 1][0] == '«':
                            listofdialog[len(listofdialog) - 1].addline(text[t], t)
                            listofdialog[len(listofdialog) - 1].addline(text[t + 1], t + 1)
                            t += 2
                else:
                    if len(listofdialog) != 0:
                        if listofdialog[len(listofdialog) - 1].number == lod:
                            lod += 1
                    if len(listoftext) == 0:
                        listoftext.append(listoft(lot))
                        listoftext[len(listoftext) - 1].addline(text[t],t)
                    else:
                        if listoftext[len(listoftext) - 1].number != lot:
                            listoftext.append(listoft(lot))
                            listoftext[len(listoftext) - 1].addline(text[t],t)
                        else:
                            listoftext[len(listoftext) - 1].addline(text[t],t)
            t += 1

        self.dialogs = listofdialog
        self.texts = listoftext

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
        return Form(case,number,gender)

    def __Dismatch(self, PersonForm, TokenForm):
        if PersonForm.gender == TokenForm.gender:
            if PersonForm.number == TokenForm.number:
                return False
            else:
                return True
        else:
            return True

    def __ValueScore(self, PersonForm, TokenForm):
        score = 0
        if PersonForm.gender == TokenForm.gender:
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

    def __Score(self, PersonForm, TokenForm):
        if self.__Dismatch(PersonForm, TokenForm):
            return None
        else:
            return self.__ValueScore(PersonForm, TokenForm)

    def __BestFirst(self, PERSONS, token, numberofline):
        if len(PERSONS) == 1:
            return PERSONS[0]
        CouldPersons = []
        tokenform = self.__wordform(token)

        for person in PERSONS:
            if person.lines[len(person.lines) - 1] == numberofline:
                score = self.__Score(person.forms[len(person.forms) - 1], tokenform)
                if score != None:
                    if person.Name =='NOUN':
                        score -= 10
                    score -= numberofline - person.lines[len(person.lines) - 1]
                    CouldPersons.append([person, score])
        if CouldPersons == []:
            MbPersons = []
            for person in PERSONS:
                score = self.__Score(person.forms[len(person.forms) - 1], tokenform)
                if score != None:
                    if person.Name == 'NOUN':
                        score -= 10
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

    def edit(self):
        parserdef = Parser(rule(self.defiz))
        for line in self.text:
            Mathcesdef = list(parserdef.findall(line))
            Spandef = [_.span for _ in Mathcesdef]
            self.spansdef = self.spansdef + Spandef
            for s in Spandef:
                self.numberoflinedef.append(self.numberofline)
            self.numberofline = self.numberofline + 1

        curd = self.numberoflinedef[0]

        for dn in  self.numberoflinedef:
            for person in self.Persons:
                for l in person.lines:
                    if dn - l <= 2 and dn - l > 0:
                        if len(self.startsofdialog.lines) == 0:
                            self.startsofdialog.lines.append(dn)
                            self.startsofdialog.names.append(person.Name)
                        else:
                            if dn - self.startsofdialog.lines[len(self.startsofdialog.lines) - 1] > 1:
                                if dn - curd > 1:
                                    self.endsofdialog.append(curd)
                                self.startsofdialog.lines.append(dn)
                                self.startsofdialog.names.append(person.Name)
                            else:
                                if dn - self.startsofdialog.lines[len(self.startsofdialog.lines) - 1] == 1:
                                    curd = dn
                    else:
                        if l > dn:
                            break

    def __Nameindialog(self, line):
        flag = False
        if 'говор' in line:
            flag = True
        if 'крик' in line:
            flag = True
        if 'шепт' in line:
            flag = True
        if 'воскли' in line:
            flag = True
        if 'продолж' in line:
            flag = True
        if 'спрос' in line:
            flag = True
        if 'объясн' in line:
            flag = True
        if 'отве' in line:
            flag = True
        if 'рассуж' in line:
            flag = True
        if 'возра' in line:
            flag = True
        if 'говоришь' in line:
            flag = False
        return flag

    def Textwithoutdialogs(self):
        text = copy.copy(self.text)
        listofdialog = self.dialogs
        parser = Parser(NAME)
        for dialog in listofdialog:
            l = 0
            while l < len(dialog):
                if self.__Nameindialog(dialog.line[l]):
                    pass
                else:
                    text[text.index(dialog.line[l])] = ''
                l += 1
        return text

    def NamesDialog(self, numberofdialog, PERSONS):
        currentdialog = None
        pasttext = None
        line = None
        if self.listofdialog != None:
            currentdialog = self.listofdialog[numberofdialog]
            for t in self.listoftext:
                if t.numberoflines.count(currentdialog.numberoflines[0] - 1) != 0:
                    pasttext = t
                    break
            PersonsInPastText = []
            for person in PERSONS:
                if pasttext.numberoflines.count(person.lines[len(person.lines) - 1]) != 0:
                    if person.Name == 'NOUN':
                        continue
                    PersonsInPastText.append(person)
            line = 0
            while line < len(currentdialog):
                if line != len(currentdialog) - 1:
                    if self.__Nameindialog(currentdialog.line[line + 1]):
                        parser = Parser(TEST)
                        match = list(parser.findall(currentdialog.line[line + 1]))
                        tokens = list([_.tokens for _ in match])
                        if tokens != []:
                            owner = ''
                            mbowner = ''
                            for token in tokens:
                                if owner != '':
                                    break
                                else:
                                    if token[0].normalized in self.NAMES:
                                        owner = token[0].normalized
                                        break
                                    for person in PERSONS:
                                        if token[0].normalized == person.Name:
                                            owner = person.Name
                                            break
                                        elif token[0].forms[0].grams.values.issuperset({'3per', 'NPRO', 'nomn'}):
                                            mbowner = self.__BestFirst(PersonsInPastText, tokens[0], currentdialog.numberoflines[0]).Name
                                            break
                            if owner != '':
                                currentdialog.owner[line] = owner
                                if currentdialog.line[line + 1][len(currentdialog.line[line + 1]) - 1] == ',':
                                    currentdialog.owner[line + 2] = owner
                                currentdialog.addowner(owner)
                                currentdialog.delline(line + 1)
                            elif mbowner != '':
                                owner = mbowner
                                currentdialog.owner[line] = owner
                                if currentdialog.line[line + 1][len(currentdialog.line[line + 1]) - 1] == ',':
                                    currentdialog.owner[line + 2] = owner
                                currentdialog.addowner(owner)
                                currentdialog.delline(line + 1)
                line += 1
            if len(currentdialog.owners) == 2:
                while currentdialog.owner.count('') != 0:
                    line = 0
                    while (line <= len(currentdialog) - 1):
                        if currentdialog.owner[line] == '':
                            if line != len(currentdialog) - 1:
                                if currentdialog.owner[line + 1] != '':
                                    indexofowner = currentdialog.owners.index(currentdialog.owner[line + 1])
                                    if indexofowner == 0:
                                        currentdialog.owner[line] = currentdialog.owners[1]
                                    else:
                                        currentdialog.owner[line] = currentdialog.owners[0]
                                elif currentdialog.owner[line - 1] != '':
                                    indexofowner = currentdialog.owners.index(currentdialog.owner[line - 1])
                                    if indexofowner == 0:
                                        currentdialog.owner[line] = currentdialog.owners[1]
                                    else:
                                        currentdialog.owner[line] = currentdialog.owners[0]
                            elif currentdialog.owner[line - 1] != '':
                                indexofowner = currentdialog.owners.index(currentdialog.owner[line - 1])
                                if indexofowner == 0:
                                    currentdialog.owner[line] = currentdialog.owners[1]
                                else:
                                    currentdialog.owner[line] = currentdialog.owners[0]
                        line += 1


    def NamesofDialog(self, listofdialog, listoftext):
        if self.Persons != None:
            PERSONS = self.Persons
        parser = Parser(TEST)
        for dialog in listofdialog:
            dialog.PersonsCouldBeInDialog = []
            if PERSONS:
                for person in PERSONS:
                    for line in person.lines:
                        if len(dialog) == 0:
                            break
                        if dialog.numberoflines.count(line):
                            if dialog.PersonsCouldBeInDialog.count(person):
                                continue
                            else:
                                dialog.PersonsCouldBeInDialog.append(person)
                        if line > dialog.numberoflines[0]:
                            break
                        else:
                            if dialog.numberoflines[0] - line > 2:
                                continue
                            else:
                                if dialog.PersonsCouldBeInDialog.count(person):
                                    continue
                                else:
                                    dialog.PersonsCouldBeInDialog.append(person)
            l = 0
            while l < len(dialog):
                if self.__Nameindialog(dialog.line[l]):
                    match = list(parser.findall(text[dialog.numberoflines[l]]))
                    tokens = list([_.tokens for _ in match])
                    if match != []:
                        for person in PERSONS:
                            if l >= len(dialog):
                                break
                            if person.lines.count(dialog.numberoflines[l]):
                                i = person.lines.index(dialog.numberoflines[l])
                                while i < len(person.lines):
                                    if l >= len(dialog):
                                        break
                                    elif person.lines[i] != dialog.numberoflines[l]:
                                        break
                                    else:
                                        flag = False
                                        for token in tokens:
                                            if person.spans[i] == token[0].span:
                                                flag = True
                                                break
                                        if flag:
                                            dialog.owner[l - 1] = person.Name
                                            if l != len(dialog.line) - 1:
                                                if dialog.line[l][len(dialog.line[l]) - 1] != '.' and dialog.line[l][len(dialog.line[l]) - 1] != ':':
                                                    dialog.owner[l + 1] = person.Name
                                            dialog.addowner(person.Name)
                                            dialog.delline(l)
                                            continue
                                        else:
                                            i += 1
                l += 1
            if dialog.owner.count(''):
                lastspan1 = []
                lastspan2 = []
                for person in dialog.PersonsCouldBeInDialog:
                    for l in person.lines:
                        if person.lines[person.lines.index(l)] <= dialog.numberoflines[0]:
                            if  dialog.numberoflines[0] - person.lines[person.lines.index(l)] > 3:
                                continue
                            if lastspan1 == []:
                                lastspan1 = [person.lines[person.lines.index(l)],person.spans[person.lines.index(l)], person]
                            else:
                                if person.lines[person.lines.index(l)] > lastspan1[0]:
                                    if person != lastspan1[2]:
                                        lastspan2 = lastspan1
                                    lastspan1 = [person.lines[person.lines.index(l)],person.spans[person.lines.index(l)], person]
                                elif person.lines[person.lines.index(l)] == lastspan1[0]:
                                    i = person.lines.index(l)
                                    while i < len(person.spans):
                                        if person.lines[i] != lastspan1[0]:
                                            break
                                        else:
                                            if person.spans[i].start > lastspan1[1].stop:
                                                lastspan1 = [person.lines[i], person.spans[i], person]
                                        i += 1
                                else:
                                    if lastspan2 == []:
                                        lastspan2 = [person.lines[person.lines.index(l)],person.spans[person.lines.index(l)], person]
                                    else:
                                        if person.lines[person.lines.index(l)] > lastspan2[0]:
                                            lastspan2 = [person.lines[person.lines.index(l) - 1], person.spans[person.lines.index(l)], person]
                                        elif person.lines[person.lines.index(l)] == lastspan2[0]:
                                            i = person.lines[person.lines.index(l)]
                                            while i < len(person.spans):
                                                if person.lines[i] != lastspan2[0]:
                                                    break
                                                else:
                                                    if person.spans[i].start > lastspan2[1].stop:
                                                        lastspan2 = [person.lines[i], person.spans[i], person]
                                                i += 1
                        else:
                            break
                if lastspan1 != []:
                    last1 = None
                    last2 = None
                    for person in dialog.PersonsCouldBeInDialog:
                        if person.lines.count(lastspan1[0]) and person.spans.count(lastspan1[1]):
                            if person.lines[person.lines.index(lastspan1[0])] == person.lines[person.spans.index(lastspan1[1])]:
                                if last2:
                                    if last2 != person:
                                        last1 = person
                                else:
                                    last1 = person
                        if lastspan2 != []:
                            if person.lines.count(lastspan2[0]) and person.spans.count(lastspan2[1]):
                                if person.lines[person.lines.index(lastspan2[0])] == person.lines[person.spans.index(lastspan2[1])]:
                                    if last1:
                                        if last1 != person:
                                            last2 = person
                                    else:
                                        last2 = person
                    i = 0
                    if last1 and last2:
                        while i< len(dialog.owner):
                            if dialog.owner[i] == '':
                                if i % 2 == 0:
                                    dialog.owner[i] = last1.Name
                                else:
                                    dialog.owner[i] = last2.Name
                            i += 1
                    elif last1 and not last2:
                        while i< len(dialog.owner):
                            if dialog.owner[i] == '':
                                    dialog.owner[i] = last1.Name
                            i += 1
                    elif last2 and not last1:
                        while i< len(dialog.owner):
                            if dialog.owner[i] == '':
                                    dialog.owner[i] = last2.Name
                            i += 1

        """for dialog in listofdialog:
            if len(dialog.owners) == 0:
                numberofnotdialog = 0
                for text in listoftext:
                    if text.numberoflines.count(dialog.numberoflines[0] - 1):
                        numberofnotdialog = listoftext.index(text)
                        break
                match = list(parser.findall(listoftext[numberofnotdialog].line[len(listoftext[numberofnotdialog].line) - 1]))
                tokens = list([_.tokens for _ in match])
                if tokens != []:
                    dialog.owner[0] = tokens[0][0].normalized
                    dialog.owners.append(tokens[0][0].normalized)"""
        for dialog in listofdialog:
            if len(dialog) > 2:
                if dialog.owner.count(''):
                    n = 0
                    while n < len(dialog):
                        if dialog.owner[n] == '':
                            if n == 0:
                                lastowner = self.__owner(dialog, n)
                            else:
                                lastowner = self.__owner(dialog, n, -1)
                            if lastowner:
                                if lastowner[0] != dialog.lastowner1 and lastowner[0] != 'автор':
                                    dialog.owner[n] = dialog.lastowner1
                                else:
                                    if lastowner[0] != dialog.lastowner2 and lastowner[0] != 'автор':
                                        dialog.owner[n] = dialog.lastowner2
                        n += 1
            if len(dialog.owners) == 1:
                if dialog.owner.count(''):
                    o = 0
                    while o < len(dialog.owner):
                        dialog.owner[o] = dialog.owners[0]
                        o += 1


    def __owner(self, dialog, n, flag = 0):
        newn = ''
        if dialog.owner[n] == '':
            if flag == 0:
                if len(dialog) - n > 1:
                    flag = 1
                else:
                    flag = -1
            if flag == 1:
                if n != len(dialog) - 1:
                    newn = self.__owner(dialog, n + 1, flag)
                return  newn
            if flag == -1:
                if n != 0:
                    newn = self.__owner(dialog, n - 1, flag)
                return newn
        else:
            return [dialog.owner[n], n]

