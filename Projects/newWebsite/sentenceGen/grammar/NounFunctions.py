# import POSObjects
from POSObjects import *
from QAHelper import *

class Subject(Noun): #a subject must have a verb
    def __init__(self, w, isSingular = True,
                 isPronoun = False, isGerund = False,
                 verb = None, name = False):
        super(Subject,self).__init__(w, 'subject', isSingular,
                                     isPronoun, isGerund)
        self.verb = verb
    def setVerb(self, verb):
        self.verb = verb
    def getVerb(self):
        return self.verb
    def getQA(self):
        QAs = []
        QAs.append(self.getSubjOfQA())
        return super(Subject, self).getQA().extend(QAs)

    def getSubjOfQA(self):
        return QASpecificWordResponse('What is ' + self.getWord() + ' the subject of?',\
         self.verb, [], self.getWord())

class DO(Noun): #direct object of a verb
    #def __init__(self, w, isPronoun=False,isSingular=True,name = False, verb = None):
    
    def __init__(self, w, isPronoun, isSingular=True,name = False, verb = None,
                 isGerund=False):
        super(DO,self).__init__(w, ['direct object','do'], isSingular,
                                     isPronoun, isGerund)
        self.verb = verb
    def setVerb(verb):
        self.verb = verb
        '''
    def getQA(self):
        questions={'This word is the object of which word?':self.verb}
        return super(DO,self).getQA().append(questions)
    '''
    
class IO(Noun): #indirect order
    def __init__(self, isSingular = False,
                 isPronoun = False, verb = None, name = False):
        super(IO,self).__init__(w, ['indirect object','io'], isSingular,
                                     isPronoun, isGerund=False,name=name)
        
class OP(Noun):
    # Object of preposition
    # can't have a verb
    def __init__(self, isSingular = True, isPronoun = False,
                 name=False):
        super(OP,self).__init__(w, ['object of the preposition','op','oop'],
                                isSingular, isPronoun, prep, isGerund=False,
                                name=name)
    def setInPrep(isInPrep): self.inPrepPhrase = isInPrep
    def getIsInPrep(): return self.isInPrepPhrase
