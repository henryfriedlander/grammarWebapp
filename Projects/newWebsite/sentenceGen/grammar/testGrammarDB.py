import random


DBprefixes = "./"

def getRandWord(f):
    return random.choice(f.readlines()).rstrip()

def readDB(fileName):
	strRandWords = filterSentence(getRandWord(open(DBprefixes+'POSDB/'+fileName))).split('-')
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
		randWord = getRandWord(open(DBprefixes+'POSDB/'+fileName))
		firstWord = (sentence.split(' ').index(numericalSentenceWord) == 0)
		hasThe = (randWord[:4] == 'the ')
		sentence = sentence.replace(numericalSentenceWord, randWord.capitalize() if firstWord else randWord,1)
		sentence = sentence.replace(numericalSentenceWord, randWord[4:] if hasThe else randWord)
		count+=1

	return sentence

def getPronounCaseQuestion():
	fileName = 'replacementTestDB.txt'
	strSentence, possWords, questionTxt, correct_words, redactWord = readDB(fileName)
	print strSentence
	print possWords
	print questionTxt
	print correct_words
	print redactWord

getPronounCaseQuestion()