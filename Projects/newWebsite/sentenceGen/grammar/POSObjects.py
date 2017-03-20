# reword the sentences so that the answers to the questions are the word


class Word(object): #this object represents a word in a sentence
    def __init__(self, w, pos, funct = None):
        self.word = w #this is the actual word this part of speech represents
        self.POS = pos #this is the string represent the part of speech
        #If this is string only one acceptable function.
        #List means that multiple accepted values.
        #first element of list will always be most complete form of data
        #i.e. Direct Object will have list ['direct object','do']
        self.funct=funct 
        
    #accessor methods
    def getWord(self): return self.word
    #part of speech is i.e. Noun, Verb, Adjective, etc.
    def getPOS(self): return self.POS
    #function is i.e. Subject, Direct Object, etc.
    def getFunct(self): return self.funct
    def __str__(self): return self.__dict__
    def __repr__(self):
        if type(self.word) != str:
            print "HI ERROR:", self.word, self.POS
            return "hi"
        return self.word
    def __eq__(self, word2):
        result = self.POS == word2 or self.funct == word2
        if result == False and word2 == "noun":
            print self.POS,
            print self.funct
        return result

    def setWord(self, w): self.word = w

    def getQA(self):
        return {'What part of speech is the highlighted word?':self.getPOS(),
                'What is the function of this word in the sentence?':\
                self.getFunct()}
    
class Noun(Word): #creates a noun object
    def __init__(self, w, function, isSing = True,
                 isPronoun = False, isGer = False, name = False,person=3):
        if name:
            isSing = True
            isGer = False
        self.name = name
        self.isSing = isSing
        self.isPro = isPronoun
        self.isGer = isGer
        self.person=person
        POS = 'noun'
        if isPronoun:
            POS = 'pronoun'
        super(Noun, self).__init__(w, POS, function)

    #accessor methods
    def isName(self): return self.name
    def isPronoun(self): return self.isPro
    def isSingular(self): return self.isSing
    def isGerund(self): return self.isGer
    def getPerson(self): return self.person
    '''
    def getQA(self):
        return {'What part of speech is this word?',
    '''
    
    #mutator methods
    def setIsPronoun(self, isPronoun): self.isPronoun = isPronoun
    def setPerson(self, person): self.person = person

    def getQA(self):
        questions = {'What is the person of this word?':self.person,
                     'Is this word singular or plural?':self.isSing,
                     'Is this word a pronoun?': self.isPro}
        return [super(Noun,self).getQA(), questions]
    

class Verb(Word):
    def __init__(self, w, function, tense, subject = None,
                 isSingular = True, isCompleted = True,
                 isActive = True, isMainVerb = False):
        self.isSingular = isSingular
        self.isCompleted = isCompleted
        self.isActive = isActive
        self.isMainVerb = isMainVerb
        self.subject = subject
        super(Verb, self).__init__(w,'verb',function)


    def setSubject(self,s):
        self.subject=s
        return self
    def setVoice(self,isActive):
        self.isActive=isActive
        return self
    def getSubject(self): return self.subject
    def getTense(self): return self.tense
    def isSingular(self): return isSingular
    def isCompleted(self): return self.isComplete
    def isActive(self): return self.isActive
    def isMainVerb(self): return isMainVerb

    def getPerson(self):
        return self.subject.getPerson()
    def getQA(self):
        questions={'What is the voice of this verb?':\
                   'active' if self.isActive else 'passive',
                   'Is this verb singular?': self.singular,
                   'What is the tense of this verb?':self.tense,
                   'Is this verb the main verb?':self.isMainVerb}
        return [super(Verb,self).getQA(), questions]

#should I create a modifier object which would help organize my data
    
class Adjective(Word):
    def __init__(self, w, function = 'adjective',
                 isParticiple = False, modifies = None):
        self.modifies = modifies #what the adjective modifies
        super(Adjective, self).__init__(w,'adjective', function)
    def isParticiple(self): return self.isParticiple
    def getModifies(self): return self.modifies
    def setModifies(self,modifies): self.modifies=modifies
    

class Adverb(Word):
    def __init__(self, w, modifies):
        super(Adverb,self).__init__(w, 'adverb')
        self.modifies = modifies
        # what the adverb modifies - is a adjective, adverb, or a verb type
    def modifies(self): return self.modifies

class Preposition(Word):
    def __init__(self, w, function, modifies, phrase): 
        super(Preposition, self).__init__(w,'preposition','preposition phrase')
        self.modifies = modifies
        self.phrase = phrase
    def getModifies(): return self.modifies
    def getPhrase(): return self.phrase

class Conjunction(Word):
    def __init__(self, w, function):
        #function says if it is a coordinating or correlative conjunction
        super(Conjunction, self).__init__(w,'conjunction', function)
        
class relPro(Word): #relative pronoun 
    def __init__(self, w, POS = 'relative pronoun',
                 antecedent = None, necessary = True, typ = None, clause=None):
        super(relPro,self).__init__(w,POS)
        self.antecedent = antecedent
        self.necessary = necessary
        self.type = typ

    def setType(typ): self.type = typ
    def getType(): return self.type
    def setClause(clause): self.clause = clause
    def setAntecedent(self, antecedent): self.antced = antecedent
    def getAntecedent(self): return self.antecedent
    def isNecessary(self): return self.necessary

    def getQA(self):
        questions={'What is the antecedent of this relative pronoun?':\
                   self.anteced,
                   'Is this relative clause necessary to the sentence?':\
                   self.isNecessary,
                   'Is this an objective or subjective relative clause?':\
                   self.typ+'ive clause'}
        return [super(relPro,self).getQA(), questions]

    
class Determiner(Word):
    def __init__(self,w,POS = 'determiner',modifies=None,funct=None):
        
        super(Determiner, self).__init__(w,POS,funct)
        self.modifies = modifies

    def getModifies(): return self.modifies
    #CHECK LATER IF THE FIRST LETTER IS A VOWEL
    # index 0: articles
    # index 1: demonstrative pronouns
    # index 2: possessive pronouns
    # index 3: quantitiy determiner -later
    def getDeterminers():
        return [['a', 'the'],['this','that','these','those'],
                ['my','your','his','her','its','our','their']]

def concatDicts(dicts):
    # concatenate all dictionaries to together by using the update function
    d=dict(dicts[0])
    for dictionary in dicts[1:]:
        d.update(dictionary)
    return d

def testconcatDicts():
    assert(concatDicts({})=={})
    d1 = {'hi':4,'hello':2}
    d2 = {'bye':5, 'byebye':1}
    assert(concatDicts([d1,d2])=={'hi':4,'hello':2,'bye':5, 'byebye':1})
           
