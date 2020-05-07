from __init__ import *

lines = []
txt =[]
with open ('text.txt') as file:
    for line in file:
        l = line.rstrip()
        lines.append(l)

txt = ' '.join(lines)
text = []
sentences = sent_tokenize(txt,'russian')
for sentence in sentences:
    text.append(sentence)

t = 0
while t < len(text):
    for l in lines:
        if text[t] in l:
            if text[t][0] == '–' and text[t + 1][0] != '–':
                while True:
                    newt = text[t] + ' ' + (text[t + 1])
                    if newt in l:
                        text[t] = newt
                        text.pop(t + 1)
                    else:
                        break
    if ', –' in text[t]:
        c = text[t].rfind(', –') + 1
        nt = text[t][c + 1: len(text[t]): 1]
        text[t] = text[t][0: c: 1]
        text.insert(t + 1, nt)
        continue
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
        pass

    def addline(self, line, numberofline):
        self.line.append(line)
        self.numberoflines.append(numberofline)

    def lines(self):
        return  self.numberoflines

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

    def __init__(self, text, persons = None):
        self.text = text
        if persons != None:
            self.Persons = persons


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

    numberofline = 0
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









