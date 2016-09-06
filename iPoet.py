# -*- coding: utf-8 -*-
__author__ = "Veaceslav Kunitki"
__copyright__ = "Copyright 2016. Please inform me in case of usage"
__credits__ = ["No credits"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Veaceslav Kuntiki"
__email__ = "tumikosha@gmail.com"
__status__ = "Production"

class Parser:
    text=""
    cursor=0
    stdDelimiters=["???","!!!","!?","?!","'",'"','~','`','!','@','#','&','*','(',')','[',']','+','-','=','/','.',',','?','/','<','>','|','\\',"\n",'\t','\r',' ',";"]
    delimiters=stdDelimiters
    sentenceDelimiters = ['.','?', '!'] # \n ?
    textList=[]
    delimList = []
    textStartPostion=0
    textEndPostion = 0
    delimStartPostion = 0
    delimEndPostion = 0
    currText=""
    currDelim=""
    blockList=[]
    inText=False
    def __init__(self,**kwargs):
        self.delimiters = self.stdDelimiters
        if 'delimiters' in kwargs:
            self.delimiters = kwargs['delimiters']
        self.blockList = []
        self.textList = []
        self.delimList = []
        self.textStartPostion = 0
        self.textEndPostion = 0
        self.delimStartPostion = 0
        self.delimEndPostion = 0
        self.currText = ""
        self.currDelim = ""
        self.blockList = []

        print ("parser initialized")

    def textStartFound(self,startPostion): # called when found start of text seq
        self.textStartPostion = startPostion

    def textEndFound(self,endPostion): # called when found end of text seq
        self.textEndPostion=endPostion
        #self.textList.append({"text": self.text[self.textStartPostion:endPostion], "start": self.textStartPostion, "end": endPostion})

    def delimStartFound(self, startPostion):  # called when found start of text seq
        self.delimStartPostion = startPostion

    def delimEndFound(self, endPostion):  # called when found end of text seq
        self.delimEndPostion = endPostion
        # self.delimList.append(
        #     {"text": self.text[self.textStartPostion:endPostion], "start": self.textStartPostion, "end": endPostion})


    def delimFound(self, position, delim, size): # called when
        if self.inText == True:  # поймали переход со слова на разделитель
            self.textEndFound(position)
            self.delimStartFound(position)
            self.currDelim = delim
            # обработать закрытие последовательности разделителей
            self.textSeqClose(position )
        else:
            self.currDelim = self.currDelim + delim
        self.inText = False
        #print(position, delim, ["x" for x in range(len(delim))])

    def delimSeqClose(self,position):
        self.delimList.append(self.currDelim)
        self.blockList.append({"text": self.currText, "delim": self.currDelim})
        self.delimEndFound(position)
        #print("delimSeqClose:",position,self.currDelim)
    def textSeqClose(self,position):
        #print("textSeqClose:",position,self.currText)
        self.textList.append(
            {"text": self.text[self.textStartPostion:position], "start": self.textStartPostion, "end": position})
        #    {"text": self.currText, "start": self.textStartPostion, "end": position})
        #self.textList.append(self.currText)

    def textCHFound(self, position, ch): # called when found start of delim seq
        if self.inText == False:  # поймали переход со разделителя на слово
            self.delimSeqClose(position)
            self.textStartFound(position)
            self.currText=ch
            # обработать закрытие последовательности разделителей

        else:
            self.currText = self.currText + ch
        self.inText = True

        #print(position, ch, 'O')

    def reconstruct(self):
        out=""
        for rec in self.blockList:
            out=out+rec['text']+rec['delim']
        return out

    def getTexts(self):
        out=[]
        for rec in self.textList:
            out.append(rec['text'])
        return out


    def parse(self, text):
        self.text = text
        i = 0
        inDelims = True
        while i <len(text):
            ch = text[i]
            #print("---",i,"]",ch)
            flag = False
            for delim in self.delimiters:
                chD = text[i:i + len(delim)]
                if chD == delim:
                    inDelims = True
                    flag = True
                    self.delimFound(i, chD, len(delim))
                    i = i + len(delim)
            if flag == False:
                self.textCHFound(i, text[i])
                i = i + 1
        if self.inText:
            self.textSeqClose(i)
            self.blockList.append({"text": self.currText, "delim": ""})
        else:
            self.delimSeqClose(i)
        # need remove first record
        self.blockList.pop(0)
        self.delimList.pop(0)
        return self

def stringTokenizer(text,delimiters):
    parser=Parser(delimiters=delimiters)
    parser.parse(text)
    return parser.getTexts()

if __name__ == "__main__":
    text0="1"
    text1="hello!"
    text2=u"Я - Аборди́рованный,  зовусь я Миша. От меня вам фунт гашиша!"
    text3="  СКИДКИ ДО КОНЦА МЕСЯЦА "
    text4="Привет!   Давай   знакомиться ?! Ты такая   красивая, я не смог пройти мимо! ;))"
    #text4 = "Привет!   Давай   знакомиться ?!"
    text5 = "0123456789"

    p1 = Parser()
    p2 = Parser()
    p3 = Parser()
    p4 = Parser(delimiters=Parser.stdDelimiters+["такая",'?!','!?','?','!','.'])
    p5 = Parser(delimiters=['456'])
    p1.parse(text1)
    p2.parse(text2)
    p3.parse(text3)
    p4.parse(text4)
    p5.parse(text5)
    #
    print("!1>>",p1.blockList)
    print("!2>>",p2.blockList)

    print('# ',Parser(delimiters=["такая",'?!','!?','?','!','.']).parse(text4).textList)
    print("!5b>>", p5.blockList)
    print("!5t>>", p5.textList)
    print("!5d>>", p5.delimList)
    print("!4b>>", p4.blockList)
    print("!4t>>", p4.textList)
    print("!4d>>", p4.delimList)
    print("!4d>>", p4.reconstruct())
    print("!4pl>>", p4.getTexts())
    # for rec in p5.textList:
    #     print (rec)

print (stringTokenizer(text4,["такая",'?!','!?','?','!','.']))