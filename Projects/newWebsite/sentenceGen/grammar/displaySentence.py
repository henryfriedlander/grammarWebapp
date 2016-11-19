# events-example2a.py
# Moves a square using arrows

from Tkinter import *
from getSentence import *
from POSObjects import *
from NounFunctions import *
import time
import tkFont


def mousePressed(event):
    print canvas.data.boxes
    print canvas.data.isClicked
    for i in xrange(len(canvas.data.boxes)):
                word = canvas.data.boxes[i]
        if word[0][0]<=event.x<=word[1][0]\
           and word[0][1]<=event.y<=word[1][1]:
            canvas.data.isClicked[i] = not canvas.data.isClicked[i]


def generateQuestions():
    isClicked=canvas.data.isClicked
    if isClicked.count(True)==1:
        questions = canvas.data.sentence[isClicked.index(True)].getQA()
        for questionDict in questions:
            for question in questionDict:
                answer = questionDict[question]
                yield [question,answer]
        

def identify(pos):
    increase(pos)
    score = 0
    maxScore = 0
    for i in xrange(10):
        # wait until the button is pressed and then check if the
        # all of the pos were clicked on
        scores = getScore(i)
        score += scores[0]
        maxScore += scores[1]
        init()
    output=''
    if score==maxScore:
        output+='Perfection! '
    if score/maxScore>=0.9:
        output+='Well Done! '
    output += 'You got: ' + str(score) +' out of '+str(maxScore)

def checkThis():
    canvas.data.numSent += 1
    if canvas.data.numSent == 1:
        increaseFreq(canvas.data.pos)
        canvas.data.score = 0
        canvas.data.maxScore = 0
    if canvas.data.numSent <= 10:
        # wait until the button is pressed and then check if the
        # all of the pos were clicked on
        scores = getScore(i)
        canvas.data.score += scores[0]
        canvas.data.maxScore += scores[1]
    canvas.data.checkSent.pack_forget()
    canvas.data.done.pack()
    if canvas.data.numSent == 10:
        output=''
        if score==maxScore:
           output+='Perfection! '
        if score/maxScore>=0.9:
            #If score is higher than 90%
            output+='Well Done! '
        output += 'You got: ' + str(score) +' out of '+str(maxScore)
        canvas.data.finished = True
        canvas.data.output = output

def nxtSent():
    canvas.data.done.pack_forget()
    if canvas.data.numSent == 10:
        canvas.data.backToTitle.pack()
    else:
        initSentence()
        canvas.data.checkSent.pack()

def getScore(i):
    score=0
    maxScore=0
    for index in xrange(len(canvas.data.sentence)):
        if canvas.data.sentence[index] == pos:
            if canvas.isClicked[index]:
                score+=1
            maxScore+=1
            canvas.data.isClicked=True
    return score, maxScore
def backTo0():
    canvas.data.e.pack_forget()
    canvas.data.backToTitle.pack_forget()
    canvas.data.b.pack()
    canvas.data.screen=0

def toScreen1():
    canvas.data.b.pack_forget()
    canvas.data.startTest.pack()


def startT():
    canvas.data.pos=canvas.data.e.get()
    canvas.data.startTest.pack_forget()
    canvas.data.checkSent.pack()
    canvas.data.screen=2

def timerFired():
    redrawAll()
    delay = 250 # in milliseconds
    canvas.after(delay, timerFired) # pause, then call timerFired again
        

def drawHelp():
    titleX=canvas.data.canvasWidth/2
    titleY = canvas.data.canvasHeight/2
    canvas.create_text(titleX,titleY,\
                            text=\
                            'Input the part of speech'+\
                            ' you want to test yourself on.')
    canvas.data.e.pack()
    

def redrawAll():
    canvas.delete(ALL)
    if canvas.data.screen == 0:
        drawTitle()
    if canvas.data.screen == 1:
        drawHelp()
    if canvas.data.screen == 2:
        drawSentence()
        
    #drawSentence()


def drawTitle():
    #(x0, y0) = (-10,-10)
    #(x1, y1) = (canvas.data.canvasWidth+10, canvas.data.canvasHeight+10)
    #canvas.create_rectangle(x0, y0, x1, y1, fill = "peach puff")
    titleX=canvas.data.canvasWidth/2
    titleY = canvas.data.canvasHeight/2
    authorY=titleY+titleY/2
    canvas.create_text(titleX,titleY,text='Grammar',
                       font='Arial 70 bold',fill='pink')
    canvas.create_text(titleX,authorY,text='by Henry Friedlander',
                       font = 'ComicSansMS 30 italic',anchor='center')
    
    
def init():
    initSentence()
    canvas.data.numSent = 0
    canvas.data.widthPixel = 10
    canvas.data.heightPixel = 10
    canvas.data.boxes=[]
    canvas.data.fontSize = 24
    canvas.data.screen = 0

def initSentence():
    canvas.data.sentence = getSentence()
    canvas.data.isClicked = [False]*len(canvas.data.sentence)

def sent():
    subj=Subject('James')
    verb=ActionVerb('runs','present',isMainVerb=True)
    subj.setVerb(verb)
    verb.setSubject(subj)
    return [subj,verb]

def drawSentence():
    startX = 100
    startY = 100
    curX = startX
    curY = startY
    canvas.data.boxes=[]
    for i in xrange(len(canvas.data.sentence)):
        isClicked=canvas.data.isClicked[i]
        if isClicked:
            color='red'
        else:
            color='black'
        curX, curY = updatePOS(curX,curY,color,i,startX)
        
def updatePOS(curX,curY,color,i,startX):
    w = canvas.data.sentence[i].getWord()
    family = "times"
    size = canvas.data.fontSize
    font = tkFont.Font(family=family, size=size)
    (lenW,height) = (font.measure(w),font.metrics("linespace"))
    if curX + lenW > canvas.data.canvasWidth-startX:
        curX=100
        curY+=height+5
        canvas.create_text(curX,curY,text=w,anchor='nw',fill=color)
        canvas.data.boxes.append([(curX,curY),(curX+lenW,curY+height)])
        curX += lenW
    else:
        canvas.create_text(curX,curY,text=w,anchor='nw',fill=color)
        canvas.data.boxes.append([(curX,curY),(curX+lenW,curY+height)])
        curX += lenW
    #curX+=font.measure(' ')
    return curX,curY

def toScreen1():
    canvas.data.screen=1
    canvas.data.b.pack_forget()
    canvas.data.startTest.pack()
    
    

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvas = Canvas(root, width=500, height=400)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.canvasWidth = 500
    canvas.data.canvasHeight = 400
    init()

    
    e = Entry(root)
    canvas.data.e = e
    


    b = Button(root, text="mode1", width=10, command = toScreen1)

    canvas.data.b = b
    b.pack()

    startTest = Button(root, text = 'start test',width=10,command=startT)
    canvas.data.startTest=startTest
    
    checkSent = Button(root, text = "check", width = 10, command = checkThis)
    canvas.data.checkSent = checkSent

    done = Button(root, text = 'next sentence', width=10, command=nxtSent)
    canvas.data.done = done



    backTo1 = Button(root, text = 'back to title',width=10, command=backTo0)
    canvas.data.backTo0 = backTo0
    
    # set up event handlers
    root.bind("<Button-1>", mousePressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
