import random
from verbFunctions import *
from NounFunctions import *
from POSObjects import *
from pattern.en import conjugate

# no modifiers on gerunds
# singular pural for determiners

# def displaySentence():
#     sentence=getSentence()
#     strSent=getStrSent(sentence)
#     print strSent
#     for i in xrange(len(sentence)):
#         word=sentence[i]
#         print 'Questions about the ith word.'
#         qs=word.getQA().keys()
#         ans=word.getQA().values()
#         print qs
#         for i in xrange(len(qs)):
#             question=qs[i]
#             inp=input(question)
#             if inp==ans[i]:
#                 print 'CORRECT'
#             else:
#                 print 'INCORRET'
#                 print 'CORRECT ANSWER '+ans[i]
        
        
#     print sentence

def getStrSent(sentence):
    w=sentence[0]
    word=w.getWord()
    w.setWord(word[0].upper()+word[1:])
    strSent=''
                 
    for word in sentence:
        if type(word)==str and word==",":
            strSent=strSent[:-1]+word+' '
        elif type(word) == str:
            strSent=strSent + word + ' '
        else: 
            w=word.getWord()
            strSent=strSent + w + ' '

    if strSent[-1] == ",":
        strSent = strSent[:-1]
    strSent = strSent[:-1] + '.'
    return strSent
    

    
def getSentence():
    init()
    '''
    if freq.doFreq and not prob(4):
        getBase(index=1)
    elif freq.ioFreq and not prob(4):
        getBase(index=2)
    '''
    return addDescriptors(getBase())

def getBase():
    sing = randBool()
    subject = getRandSubject(sing=sing)
    actionVerb = getRandActVerb(sing=sing)
    do = getRandDO()
    pa = getRandAdjective()
    # get random linking verb 
    
    bases = [
        [subject, actionVerb],
        [subject, actionVerb, do]
        ]

    index = random.randint(0,len(bases)-1) # get the index of a random base
    indexOfActionVerb = -1
    if actionVerb in bases:
        indexOfActionVerb = bases[index].index(actionVerb) # REMOVE THE HARDCODE
    print "indexOfActionVerb: " + str(indexOfActionVerb)
    makeRels(bases, index)

    print "action verb tense: " + str(actionVerb.getTense())
    base = bases[index]
    if indexOfActionVerb != -1:
        base = addHelpingVerbs(bases[index], indexOfActionVerb)
    #there are no words in base just line numbers of the file
    print "base: " + str(base)
    return base

def addHelpingVerbs(base, indexOfActionVerb):
    actionVerb = base[indexOfActionVerb]
    helpingVerbs = actionVerb.getHelpingVerbs()
    if helpingVerbs != []:
        while helpingVerbs != []:
            base.insert(indexOfActionVerb, helpingVerbs.pop())
    return base
def makeRels(bases, index):
    if index==1:
        makeRels1(bases[index])
    if index == 2:
        makeRels1(bases[index][:2])
        makeRels2(bases[index])
    if index == 3:
        makeRels1(bases[index][:2])
        makeRels3(bases[index])

def makeRels1(base):
    base[0].setVerb(base[1])
    base[1].setSubject(base[0])

def makeRels2(base):
    base[2].setVerb(base[1])
def makeRels3(base):
    base[2].setModifies(base[0])

def addDescriptors(base):
    #should I add the words in this function?
    sentence = [] #final sentence descriptors
    for word in base:
        print word.getWord(),
        # the car OF Jonah
        if word == 'noun' or word == 'pronoun':
            sentence += addDescriptorsNoun(word)
        if word == 'verb':
            sentence += addDescriptorsVerb(word)
        print "after word: ", sentence
    for w in sentence:
        print repr(w)
    print sentence
    print 'hi'
    return sentence

def init():
    class Struct: pass
    global freq
    freq = Struct()
    freq.relProFreq=False
    freq.adjFreq=False
    freq.adverbFreq=False
    freq.doFreq=False
    freq.ioFreq=False
    freq.participleFreq=False #add participles
    freq.gerundFreq=False
    
def increaseRelProFreq():
    freq.relProFreq=True
    
def increaseAdverbFreq():
    freq.adverbFreq=True

def increaseDOFreq():
    freq.doFreq=True

def increaseParticipleFreq():
    freq.participleFreq=True

def increaseGerundFreq():
    freq.gerundFreq=True

def increaseFreq(pos):
    if pos == 'relative pronoun' or pos == 0:
        increaseRelProFreq()
    if pos == 'adverb' or pos == 1:
        increaseAdverbFreq()
    if pos == 'participle' or pos == 2:
        increaseParticipleFreq()
    if pos == 'gerund' or pos == 3:
        increaseGerundFreq()
    if pos == 'direct object' or pos==4:
        increaseDOFreq()


def testIncreaseFreq():
    init()
    increaseRelFreq('relative pronoun')
    assert(relProFreq==True)
    increaseAdverbFreq()
    assert(adverbFreq==True)
    increaseParticipleFreq()
    assert(participleFreq==True)
    init()


def addDescriptorsVerb(word):
    sentence=[]
    print "sentence before: ", sentence
    if word=='action verb':
        if prob(5):
            adv = getRandAdverb(word)
            if prob(3):
                sentence += [Adverb('very',adv)]
            sentence += [adv]
        sentence += [word]
    print "sentence after: ", sentence
    return sentence

def addDescriptorsNoun(word):
    sentence=[]
    if not word.isPronoun():
        if not word.isName() and not word.isGerund:
            print 'inside'
            sentence += [getRandDeterminer(word)]
            if prob(5) or (freq.adjFreq and not prob(5)): # add an adjective if not a name
                adj=getRandAdjective()
                if prob(5) or (freq.adverbFreq and not prob(5)):
                    sentence += [getRandAdverb(adj)]
                sentence += [adj]
        sentence += [word]
        if prob(3) or (freq.relProFreq and not prob(5)): # add relative clause
            # the clause itself is stored inside the rel pro
            # returns list
            relativePro,nec = getRandRelPro(word)
            sentence += relativePro
            print sentence
            if not nec:
                sentence+=[',']
    else:
        sentence += [getRandSubjPron(word)]
    return sentence

def getRandSubjPron(word):
    pronouns = [['we','they'],['I','you','he','she','it']]
    
    word.setWord(random.choice(pronouns[int(word.isSingular())]))
    w=word.getWord()
    if w == 'we' or w == 'I':
        word.setPerson(1)
    elif w == 'you':
        word.setPerson(2)
    else:
        word.setPerson(3)
    word.setIsPronoun(True)
    return word

def prob(upper):
    return not random.randint(0,upper)

def randBool():
    return bool(random.randint(0,1))

def getRandAdverb(modifies):
    return Adverb("happily", modifies)
    #return Adverb(random.randint(0,1),modifies)

def getRandRelPro(antec):
    nec = randBool()
    index = random.randint(0,1)
    typ = ['object', 'subject'][random.randint(0,1)]
    if antec.isName():
        relPros = ['who','whose']
        '''
        if antec == 'subject':
            relPro[0] = 'whom'
        '''
    else:
        relPros = ['which','that']
        nec = bool(index)
    relPron = relPros[index]
    if relPron == 'whose': typ = 'possessive'
    clause = getClause(typ)
    print "clause: ", clause
    res = [relPro(relPron, antecedent = antec, necessary = nec)]
    res += clause
    if not nec: res=[',']+res #adds commas for unneccessary clauses
    return res,nec

def getClause(typ):
    if typ == 'possessive':
        return getBase()
    elif typ == 'subject':
        base = [getRandActVerb(), getRandObjPP()]
        return addHelpingVerbs(base, 0)
    else:
        base = [getRandSubject(),getRandActVerb()]
        return addHelpingVerbs(base, 1)
#DOES NOT WORK
def getRandDeterminer(modifies):
    
    # that singular
    determiners = [['an' if isVowel(modifies.getWord()[0]) else 'a', 'the'],
                   ['this','that','these','those'],
                   ['my','your','his','her','its','our','their']]
    typ=random.randint(0,len(determiners)-1)
    # randomly choosing demonstrative pronoun article or possessive pronoun
    if typ == 0:
        function = 'article'
        if modifies.isSingular():
            index=2
        else:
            index = random.randint(0,len(determiners[typ])-1)
    elif typ == 1:
        function = 'demonstrative pronoun'
        if modifies.isSingular():
            index = random.randint(0,1)
        else:
            index = random.randint(2,3)
    elif typ == 2:
        function = 'possessive pronoun'
        index = random.randint(0,len(determiners[typ])-1)
    
    print "get determiner: ", determiners[typ][index]
    return Determiner(determiners[typ][index], modifies = modifies,
                      funct = function)

    

def isVowel(ch):
    return ch.lower() in set(['a','e','i','o','u'])

def getRandNoun(noun):
    # add singular functionality using patterns.en
    if noun.isGerund():
        f = open('./sentenceGen/grammar/POSLists/actionVerbs.txt')
        return addIng(getRandWord(f))
    else:
        if noun.isName():
            f = open('./sentenceGen/grammar/POSLists/nameList.txt')
        else:
            f = open('./sentenceGen/grammar/POSLists/nounList.txt')
        return getRandWord(f)+('s' if noun.isSingular() else '')
                

def getRandSubject(sing=randBool()):
    subj = Subject('', isSingular=sing,
                   isGerund = prob(5) or (freq.gerundFreq and not prob(5)),
                   isPronoun = prob(5),
                   name = False) #NEED TO CHANGE
    subj.setWord(getRandNoun(subj))
    return subj

def getRandOOP(prep):
    op = OP('',isSingular = randBool(), isGerund = prob(5) or (freq.gerundFreq and not prob(5)),
              isPronoun = prob(5), prep=prep,name = False) #NEED TO CHANGE
    op.setWord(getRandNoun(op))
    return op

def getRandDO():
    isSingular = randBool()
    do = DO('',isPronoun = prob(5),name = False, isSingular = isSingular, isGerund = False)
    
    do.setWord(getRandNoun(do))
    return do

def getRandVerb(verb):
    # gets a random verb according to the predetermined, randomly generated criteria
    if verb.getFunct() == 'action verb':
        f = open('./sentenceGen/grammar/POSLists/ActionVerbs.txt')
        wordtxt = getRandWord(f)
        print "wordtxt: " + wordtxt
        return wordtxt
    else:
        f = open('./sentenceGen/grammar/POSLists/linkingVerbs.txt')
        
def getPA():
    adj=Adjective('',function='predacate adjective')
    adj.setWord(getRandAdj())
    return adj

    
def getRandAdjective():
    f = open('./sentenceGen/grammar/POSLists/adjectives.txt')
    return getRandWord(f)
        
def addIng(verb):
    if type(verb)==str:
        word=verb
    else:
        word = verb.getWord()
    # if the word ends in e and the second to last letter is not o e or y,
    # replace the e
    if word[-1]=='e' and (word[-2]!='o' and word[-2]!='e' and word[-2]!='y'):
        word = word[:-1]+'ing'
    # else just add ing
    else:
        word+='ing'
    if type(verb)==str:
        return word
    verb.setWord(word)

def testAddIng():
    assert(addIng(Verb('walk','action verb','past'))=='walking')
    assert(addIng(Verb('bake','action verb','present'))=='baking')
    assert(addIng(Verb('free','action verb','present'))=='freeing')

def addEd(verb):
    word = verb.getWord()
    word+='ed'
    verb.setWord(word)

def getRandActVerb(sing = randBool(), person = 3):
    actV = ActionVerb('', getRandTense(), isSingular=sing, isCompleted = randBool())
    tense = actV.getTense()
    number = 'singular' if actV.isSingular else 'plural'
    print "tense: " + tense
    if tense == 'future':
        tenseConjugate = 'present'
        will = helpingVerb('will', tense, actV)
        number = 'plural'
        actV.setHelpingVerbs([will])
        print 'will has been added'
    else:
        tenseConjugate = tense
    actV.setWord(str(conjugate(getRandVerb(actV), tense=tenseConjugate, person=person, number=number)))
    print "getRandActVerb: " + actV.getWord()
    print conjugate(getRandVerb(actV), tense=tense, person=person, number=number)
    return actV
#---------------Tenses----------------#

def getPresentContinuous(verb):
    verb.addIng()
    if verb.isSingular():
        if verb.getPerson()==1:
            helpV='am'
        if verb.getPerson()==2:
            helpV='are'
        if verb.getPerson()==3:
            helpV='is'
    else:
        helpV='are'
    
    return helpingVerb(helpV,'present',verb,verb.isSingular)+verb

#def getPastContinuous(verb):

def getRandTense():
    return ['present','future','past'][random.randint(0,2)]

def getRandObjPP():
    #NEEDS TO RETURN OBJECT
    # get random objective personal pronouns
    pps = ['me']*3+['you','him','her','it','us']+3*['them']
    return pps[random.randint(0,len(pps)-1)]

def getRandPrepPhrase():
    f = open('prepList.txt')
    prep = getRandWord(f)
    prepPhrase = addDescriptorsNoun()

def getRandWord(f):
    return random.choice(f.readlines()).rstrip()

print "getSentence: " + str(getSentence())
