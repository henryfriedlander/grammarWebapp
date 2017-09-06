import random

def getRandWord(f):
    return random.choice(f.readlines()).rstrip()

def readDB(fileName):
	prefix = "/Users/henry/Projects/grammarWebapp/Projects/newWebsite/sentenceGen/grammar/"
	strRandWords = getRandWord(open(prefix+'POSDB/'+fileName)).split('-')
	if strRandWords[1]=='itrAllWords':
		strRandWords[1]=strRandWords[0][:-1].split(' ') #GET RID OF ALL COMMAS FROM SENTENCE
	else:
		strRandWords[1] = strRandWords[1].split(',') #splits poswords
	strRandWords[3] = strRandWords[3].split(',') #splits poswords
	return strRandWords

def getPronounCaseQuestion():
	fileName = 'VerbIdentificationDB.txt'
	strSentence, possWords, questionTxt, correct_words, redactWord = readDB(fileName)
	print strSentence
	print possWords
	print questionTxt
	print correct_words
	print redactWord

getPronounCaseQuestion()