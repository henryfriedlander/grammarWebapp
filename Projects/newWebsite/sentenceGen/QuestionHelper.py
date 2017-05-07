from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import random
from . import forms
from models import Quiz, Question, Word, Teacher

from grammar import getSentence

questionNumber = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]

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

def makeRandQuestion(input = 0):
    # get random question type
    # if 0, get random mode
    # if 1, 
    # changes the function getQA so that it return a list of the possWords with the correct answer at index 0
    # if the type of the value inside the dictionary return by getQA is not a list,
    # then get random words from the sentence
    questionPK = ""
    sentence = getSentence.getSentence()
    numQuestions = 35
    if True in questionNumber[:numQuestions+1]:
        questionType = 36#random.randint(1,numQuestions)
        if not questionNumber[questionType]:
            while not questionNumber[questionType]:
                print "IN WHILE LOOP!!!!!!!"
                questionType = random.randint(1,numQuestions)
    else:
        questionType = 0
    print "questionType " + str(questionType)
    #questionType = 2# random.randrange(0,2)
    print "Question Number " + str(len(questionNumber))
    if questionType == 0:
        modes = getPossibleQuestionModes()
        random_index = random.randrange(0,len(modes))
        random_tuple = modes[random_index]
        mode = random_tuple[1]
        questionPK = makeQuestionPOSID(sentence, mode)
    elif questionType == 1:
        strSentence="Lou Ellen and I bought toilet paper."
        possWords = ["I","me"]
        questionTxt = "Fill in the blank."
        correct_words = "[I]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "I")
    elif questionType == 2:
        strSentence="With whom are you going through the praire?"
        possWords = ["who","whom"]
        questionTxt = "Fill in the blank."
        correct_words = "[whom]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "whom")
        questionPK = makeWhomQuestion()
    elif questionType == 3:
        strSentence="Who is lighter than Evan?"
        possWords = ["Who","Whom"]
        questionTxt = "Fill in the blank."
        correct_words = "[Who]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact ="Who")
    elif questionType == 4:
        strSentence="Juliet who killed the beast very happily cries out."
        possWords = ["cries", "beast", "Juliet", "very"]
        questionTxt = "What is the antecedent of \"who\"."
        correct_words = "[Juliet]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words)
    elif questionType == 5:
        strSentence="Who is the most snide?"
        possWords = ["Who", "Whom"]
        questionTxt = "Fill in the blank."
        correct_words = "[Who]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "Who")
    elif questionType == 6:
        strSentence="Whom should I beat?"
        possWords = ["Who", "Whom"]
        questionTxt = "Fill in the blank."
        correct_words = "[Whom]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "Whom")
    elif questionType == 7:
        strSentence="Who will compute the data with Jacob?"
        possWords = ["Who", "Whom"]
        questionTxt = "Fill in the blank."
        correct_words = "[Who]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "Who")
    elif questionType == 8:
        strSentence="To whom will I give the present?"
        possWords = ["Who", "Whom"]
        questionTxt = "Fill in the blank."
        correct_words = "[Whom]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "whom")
    elif questionType == 9:
        strSentence="The crass banker will build the swimming pool so that he might elect."
        possWords = ["will build", "so that he might elect", "he might elect", "There is no purpose clause"]
        questionTxt = "If there is a purpose clause, identify it."
        correct_words = "[so that he might elect]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 10:
        strSentence="Whom should I beat?"
        possWords = ["Who", "Whom"]
        questionTxt = "Fill in the blank."
        correct_words = "[Whom]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "Whom")
    elif questionType == 11:
        strSentence="To kick the chair, the deaf doctor will complete the task."
        possWords = ["To kick the chair", "deaf doctor", "will complete the task", "There is no purpose clause"]
        questionTxt = "If there is a purpose clause, identify it."
        correct_words = "[To kick the chair]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 12:
        strSentence="In order to run the race, Franklin wondered about the building."
        possWords = ["wondered about", "to run the race", "In order to run the race", "there is no purpose clause"]
        questionTxt = "If there is a purpose clause, identify it."
        correct_words = "[In order to run the race]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 13:
        strSentence="The unhappy leopard had been unable to find its telephone."
        possWords = ["to find its telephone", "had been unable to find its telephone", "find its telephone", "there is no purpose clause"]
        questionTxt = "If there is a purpose clause, identify it."
        correct_words = "[there is no purpose clause]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 14:
        strSentence="They live in a house which is large."
        possWords = ["house", "They", "large"]
        questionTxt = "What is the antecedent of \"which\"."
        correct_words = "[house]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 15:
        strSentence="On the field, the doctor and John win the horse."
        possWords = ["present", "future", "past"]
        questionTxt = "What is the tense of the main verb."
        correct_words = "[present]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 16:
        strSentence="I had been aching on this field with Thomas."
        possWords = ["present", "future", "past"]
        questionTxt = "What is the tense of the main verb."
        correct_words = "[past]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 17:
        strSentence="You feigned shyness toward the Jonathan."
        possWords = ["present", "future", "past"]
        questionTxt = "What is the tense of the main verb."
        correct_words = "[past]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 18:
        strSentence= "After the unfortunate plan was crafted, Erica will be warm."
        possWords = ["present", "future", "past"]
        questionTxt = "What is the tense of the main verb."
        correct_words = "[future]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 19:
        strSentence="The ashes of the building coat the tulips."
        possWords = ["coated", "will coat", "coat", "is coating"]
        questionTxt = "Fill in the blank (the main verb is present)."
        correct_words = "[coat]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "coat")
    elif questionType == 20:
        strSentence="To understand the concepts, Emily walked on the lagoon."
        possWords = ["will walk", "is walking", "walked"]
        questionTxt = "What is the tense of the main verb (the main verb is future)."
        correct_words = "[will walk]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "walked")
    elif questionType == 21:
        strSentence="Connor, the happy man, makes by the machine."
        possWords = ["makes", "is made", "made"]
        questionTxt = "What is the tense of the main verb (the main verb is present)."
        correct_words = "[is made]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "makes")
    elif questionType == 22:
        strSentence="The phone which can call calls Julia."
        possWords = ["called", "calls", "is about to call"]
        questionTxt = "What is the tense of the main verb (the main verb is past)."
        correct_words = "[called]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "calls")
    elif questionType == 23:
        strSentence = "That chair is I in the class."
        possWords = ["I", "me"]
        questionTxt = "Fill in the blank."
        correct_words = "[I]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "I")    
    elif questionType == 24:
        strSentence = "Jeremy kills me."
        possWords = ["I", "me"]
        questionTxt = "Fill in the blank."
        correct_words = "[me]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "me")    
    elif questionType == 25:
        strSentence =  "He gives the present to me."
        possWords = ["I", "me"]
        questionTxt = "Fill in the blank."
        correct_words = "[me]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "me") 
    elif questionType == 26:
        strSentence =  "It had been cutting the tree with John."
        possWords = ["simple", "perfect", "progressive", "perfect progressive"]
        questionTxt = "Identify the aspect of the main verb."
        correct_words = "[perfect progressive]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "") 
    elif questionType == 27:
        strSentence =  "The trees are growing near the field."
        possWords = ["simple", "perfect", "progressive", "perfect progressive"]
        questionTxt = "Identify the aspect of the main verb."
        correct_words = "[progressive]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "") 
    elif questionType == 28:
        strSentence =  "Marcus will talk to Andy."
        possWords = ["simple", "perfect", "progressive", "perfect progressive"]
        questionTxt = "Identify the aspect of the main verb."
        correct_words = "[simple]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "") 
    elif questionType == 29:
        strSentence =  "John has sent the letter."
        possWords = ["simple", "perfect", "progressive", "perfect progressive"]
        questionTxt = "Identify the aspect of the main verb."
        correct_words = "[perfect]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 30:
        strSentence =  "The bland understatement has connected the colorful dots inside the house."
        possWords = ["The", "understatement", "connected", "the", "dots", "inside", "the", "house"]
        questionTxt = "Identify all the nouns."
        correct_words = "[understatement, dots, house]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")   
    elif questionType == 31:
        strSentence =  "Dan will be happier than Jenny."
        possWords = ["positive", "comparative", "superlative"]
        questionTxt = "What is the degree of the adjective in the above sentence."
        correct_words = "[comparative]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 32:
        strSentence =  "The blue chair will try to be faster than Jenny."
        possWords = ["fast", "faster", "fastest"]
        questionTxt = "Fill in the blank."
        correct_words = "[faster]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "faster")
    elif questionType == 33:
        strSentence =  "The lowest rose will signify death."
        possWords = ["positive", "comparative", "superlative"]
        questionTxt = "What is the degree of adjective in the above sentence."
        correct_words = "[superlative]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 34:
        strSentence =  "The bright leaf is about to be floating in the school."
        possWords = ["positive", "comparative", "superlative"]
        questionTxt = "What is the degree of the adjective in the above sentence."
        correct_words = "[positive]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    elif questionType == 35:
        strSentence =  "The hairy dog has been barking."
        possWords = ["hairy", "hairier", "hairiest"]
        questionTxt = "Fill in the blank."
        correct_words = "[hairy, hairiest]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "hairy")
    elif questionType == 36:
        strSentence =  "Chase will be hanging the velvet cloak and the coat."
        possWords = ["Chase", "will", "be", "hanging", "the", "velvet", "cloak", "and", "the", "coat"]
        questionTxt = "Identify all the nouns."
        correct_words = "[Chase, cloak, coat]"
        questionPK = makeAntecedentQuestion(strSentence, questionTxt, possWords, correct_words, redact = "")
    '''
    elif questionType == 2:
        questionPK = makeQuestionHightlight(sentence)
    elif questionType == 3:
        questionPK = makeQuestionRedact(sentence, correctWord, possWords)
    else:
        print "questionType out of range"
    '''
    questionNumber[questionType] = False
    print questionNumber
    if input == 0:
        return questionPK
    else:
        return strSentence
    

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

def makePronounCaseQuestion():
    q = Question(sentence = joinSentenceRedact(\
        "Lou Ellen and I bought toilet paper.", "I"), wordPKs = "")
    q.save()
    updatePKs(getPKsAnswer(["I","me","myself"], q, "pronoun"), q)
    q.text = "Fill in the blank."

    q.correct_words = "[I]"
    q.save()
    return q.pk

def makePronounCaseQuestion():
    q = Question(sentence = joinSentenceRedact(\
        "Lou Ellen and I bought toilet paper.", "I"), wordPKs = "")
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
