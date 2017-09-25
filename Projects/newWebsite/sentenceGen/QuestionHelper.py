from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import random
from . import forms
from models import Quiz, Question, Word, Teacher
import os

from grammar import getSentence

used_indices = set([])
settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
XMLFILES_FOLDER = os.path.join(PROJECT_ROOT, 'sentenceGen/grammar/POSDB/')

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

def makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact=""):
    q = Question(sentence = joinSentenceRedact(strSentence, redact), wordPKs = "")
    q.save()
    updatePKs(getPKsAnswer(possWords, q, "pronoun"), q)
    q.text = questionTxt

    q.correct_words = correct_words
    q.save()
    return q.pk    

def makeWhoQuestion():
    q = Question(sentence = joinSentenceRedact(\
        "Who is lighter than Evan?", "Who"), wordPKs = "")
    q.save()
    updatePKs(getPKsAnswer(["Who","Whom"], q, "pronoun"), q)
    q.text = "Fill in the blank."

    q.correct_words = "[Who]"
    q.save()
    return q.pk

def makeWhomQuestion():
    q = Question(sentence = joinSentenceRedact(\
        "With whom are you going through the praire?", "whom"), wordPKs = "")
    q.save()
    updatePKs(getPKsAnswer(["who","whom"], q, "pronoun"), q)
    q.text = "Fill in the blank."

    q.correct_words = "[whom]"
    q.save()
    return q.pk

def makeWhoOrWhomQuestion():
    fileName = 'replacementTestDB.txt'
    return makeGenericQuestion(fileName)   

def makePronounCaseQuestion():
    fileName = 'PronounCaseDB.txt'
    return makeGenericQuestion(fileName)

def makeVerbIDQuestion():
    fileName = 'VerbIdentificationDB.txt'
    return makeGenericQuestion(fileName)

def makeCapitalizationQuestion():
    fileName = 'CapitalizationDB.txt'
    return makeGenericQuestion(fileName)

def makeNounIDQuestion():
    fileName = 'NounIdentificationDB.txt'
    return makeGenericQuestion(fileName)

def makeCommaListQuestion():
    fileName = 'CommaListDB.txt'
    return makeGenericQuestion(fileName)

def makeCommaSeperatingCoordinatingAdjectiveQuestion():
    fileName = 'CommaSepCoordinatingAdjDB.txt'
    return makeGenericQuestion(fileName)

def makeAdverbIDQuestion():
    fileName = 'AdverbIdentificationDB.txt'
    return makeGenericQuestion(fileName)

def makeGenericQuestion(fileName):
    return setPKInfo(fileName)

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
def setPKInfo(fileName):
    strSentence, possWords, questionTxt, correct_words, redactWord = readDB(fileName)
    return makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = redactWord)

def getRandWord(f):
    # get a random number and check if that number is in the array
    # create a random list of the possible questions to check whether it has been done.
    lines = f.readlines()
    pos_indices = set(lines) - used_indices
    print pos_indices
    print len(pos_indices)
    question = random.choice(list(pos_indices))
    used_indices.add(question)
    print question.rstrip()
    return question.rstrip()

def convertArrayToString(arr):
    fomattedStr = '['
    for s in arr:
        fomattedStr += s +','
    fomattedStr = fomattedStr[:-1]+']'
    return fomattedStr

def readDB(fileName):
    strRandWords = filterSentence(getRandWord(open(XMLFILES_FOLDER+fileName))).split('-')
    if not strRandWords[0][-1] == '.':
        strRandWords[0] = strRandWords[0][:-1] + '.'
    if strRandWords[1]=='itrAllWords':
        strRandWords[1]=strRandWords[0][:-1].split(' ') #GET RID OF ALL COMMAS FROM SENTENCE
    else:
        strRandWords[1] = strRandWords[1].split(',') #splits poswords
    strRandWords[3] = strRandWords[3].split(',') #splits poswords
    return strRandWords

def filterSentence(sentence):
    typesOfWords = [
        'Occupations.txt',
        'AdjComp.txt',
        'Entities.txt',
        'Colors.txt',
        'Objects.txt',
        'Places.txt',
        'EmotionAdverbs.txt',
        'PositiveAbstractNouns.txt',
        'PositiveAdjectives.txt',
        'CitiesAndCountries.txt',
        'NegativeAbstractNouns.txt',
    ]
    for typeOfWord in typesOfWords:
        sentence = filterPlaceholders(sentence,typeOfWord)

    return sentence

def filterPlaceholders(sentence, fileName):
    count = 1
    sentenceWord = fileName[:-4]
    while sentenceWord in sentence:
        numericalSentenceWord = sentenceWord+str(count)
        randWord = getRandWord(open(XMLFILES_FOLDER+fileName))
        firstWord = (sentence.split(' ').index(numericalSentenceWord) == 0)
        hasThe = (randWord[:4] == 'the ')
        sentence = sentence.replace(numericalSentenceWord, randWord.capitalize() if firstWord else randWord,1)
        sentence = sentence.replace(numericalSentenceWord, randWord[4:] if hasThe else randWord)
        count+=1

    return sentence
