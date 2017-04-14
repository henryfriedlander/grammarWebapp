from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import random
from . import forms
from models import Quiz, Question, Word, Teacher

from grammar import getSentence

def joinSentence(sentence):
    realSentence = getSentence.getStrSent(sentence)
    return realSentence

def joinSentenceRedact(sentence, word):
    realSentence = sentence.split()#getSentence.getStrSent(sentence).split()
    for k in xrange(len(realSentence)):
        if stripNonChar(realSentence[k])==word:
            realSentence[k]="_____"
    return " ".join(realSentence)

def stripNonChar(w):
    if w[0].isalnum() and w[-1].isalnum():
        return w
    elif w[0].isalnum():
        return w[0:-1]
    elif w[-1].isalnum():
        return w[1:]
    else:
        return w[1:-1]


def getPartOfSpeech(word): # fix
    if type(word) == str:
        return "punctuation"
    return word.getPOS()#random.choice(["noun"]) #, "adjective", "adverb"])

def getWord(word): # return the string
    # fix
    return word.getWord()

def makeWord(word, question, index):
    part_of_speech = getPartOfSpeech(word)
    word = getWord(word)
    w = Word(question = question, word = word, part_of_speech = part_of_speech, index = index)
    w.save()
    return w.pk

def makeAnswer(wordText, question, POSText, index):
    w = Word(question = question, word = wordText, part_of_speech = POSText, index = index)
    w.save()
    return w.pk

def getPossibleQuestionModes():
    return [(1, 'noun')]#, (2, 'adverb'), (3, 'adjective')]

def makeRandQuestion():
    # get random question type
    # if 0, get random mode
    # if 1, 
    # changes the function getQA so that it return a list of the possWords with the correct answer at index 0
    # if the type of the value inside the dictionary return by getQA is not a list,
    # then get random words from the sentence
    questionPK = ""
    sentence = getSentence.getSentence()
    questionType = 2#random.randrange(0,2)
    if questionType == 0:
        modes = getPossibleQuestionModes()
        random_index = random.randrange(0,len(modes))
        random_tuple = modes[random_index]
        mode = random_tuple[1]
        questionPK = makeQuestionPOSID(sentence, mode)
    elif questionType == 1:
        questionPK = makePronounCaseQuestion()
    elif questionType == 2:
        questionPK = makeQuestionHightlight(sentence)
    elif questionType == 3:
        questionPK = makeQuestionRedact(sentence, correctWord, possWords)
    else:
        print "questionType out of range"

    return questionPK

def makeQuestion(sentence, questionType, mode = "", possWords = [], correctWord = [], boldWord = []):
    # an idntify question is one where the question
    # asks the user to click on all the words of a particular POS
    # find all POS that match the mode
    # return None if there are no POS of the mode type in the sentence
    # populate correct_words field inside the Question model inside this function
    questionPK = ""
    if questionType == 0:
        questionPK = makeQuestionPOSID(sentence, mode)
    elif questionType == 1:
        questionPK = makeQuestionHightlight(sentence, boldWord, possWords)
    elif questionType == 2:
        questionPK = makeQuestionRedact(sentence, correctWord, possWords)
    else:
        print "questionType out of range"

    return questionPK


def makeQuestionHightlight(sentence):
    q = Question(sentence = sentence, wordPKs = "")
    q.save()

    highlightedWord = sentence[random.randrange(0,len(sentence))]
    while type(highlightedWord) == str: 
        ighlightedWord = sentence[random.randrange(0,len(sentence))]
    # while loop until dont get a string
    QAs = highlightedWord.getQA()
    QA = QAs[random.randrange(0,len(QAs))]
    q.text = QA.getQuestionTxt()
    q.correct_words = QA.getCorrectWords()
    possWords = QA.getAnswerChoices()
    if possWords == [] or possWords == ['This verb does not have a subject']:
        possWords.extend(joinSentence(sentence))
        #while possWords <= 5 or limit number of answer choices
    updatePKs(getPKsRedact(possWords, q), q)
    q.save()

    return q.pk

def makeQuestionPOSID(sentence, mode):
    q = Question(sentence = joinSentence(sentence), wordPKs = "")
    q.save()

    updatePKs(getPKs(sentence, mode, q), q)

    modeWords = getModeWords(sentence, mode)

    if modeWords == []:
        return None
    question = {"Identify all the " + str(getPartOfSpeech(modeWords[0])) + "s in the above sentence.": modeWords}
    updateQuestionAnswer(q, question)

    q.save()
    print q.correct_words
    return q.pk

def makeQuestionRedact(sentence, correctWord, possWords):
    q = Question(sentence = joinSentenceRedact(sentence, correctWord), wordPKs = "")
    q.save()

    updatePKs(getPKsRedact(possWords, q), q)

    q.text = "Fill in the word which best complete the following sentence"
    q.correct_words = correctWord
    q.save()

    return q.pk

def makePronounCaseQuestion():
    q = Question(sentence = joinSentenceRedact(\
        "To complete our Egyptian mummy costumes, Lou Ellen and I bought a 12 pack of toilet paper.", "I"), wordPKs = "")
    q.save()
    updatePKs(getPKsAnswer(["I","me","myself"], q, "pronoun"), q)
    q.text = "Fill in the blank."

    q.correct_words = "[I]"
    q.save()
    return q.pk

def getPKsAnswer(possWords, q, POSText):
    index = 0
    wordPKs = ""
    for word in possWords:
        current_pk = makeAnswer(word, q, POSText, index)
        index += 1
        wordPKs = wordPKs + str(current_pk) + ","
    return wordPKs

def updateQuestionAnswer(q, question):
    #i = random.randrange(0,len(modeWords))
    #question = getQuestion(modeWords,questionType)
    dictKeys = question.keys()
    j = random.randrange(0,len(dictKeys))
    text = dictKeys[j]
    q.correct_words = question.get(text)
    q.text = text

def updatePKs(wordPKs, q):
    wordPKs = wordPKs[:-1]
    print("pk "+wordPKs)
    q.wordPKs = wordPKs

def getPKsRedact(possWords, q):
    index = 0
    wordPKs = ""
    for word in possWords:
        current_pk = makeWord(word, q, index)
        index += 1
        wordPKs = wordPKs + str(current_pk) + ","
    return wordPKs

def getPKs(sentence, mode, q):
    index = 0
    wordPKs = ""
    for word in sentence:
        if getPartOfSpeech(word) != "punctuation":
            current_pk = makeWord(word, q, index)
            index += 1
            wordPKs = wordPKs + str(current_pk) + ","
    return wordPKs

def getModeWords(sentence, mode):
    index=0
    modeWords = []
    for word in sentence:
        if getPartOfSpeech(word) == mode:
            modeWords+=[word]
        index += 1
    return modeWords
