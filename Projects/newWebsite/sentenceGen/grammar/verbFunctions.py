from POSObjects import *
from QAHelper import *


class ActionVerb(Verb):
    def __init__(self, w, tense, subject = None,
                 isSingular = True, isCompleted = True,
                 isActive = True, isMainVerb = False):
        super(ActionVerb,self).__init__(w,'action verb', tense, subject,
                                        isSingular, isCompleted,
                                        isActive, isMainVerb)
    def getQA(self):
        QAs = []
        QAs.append(self.getSubjQA())
        return super(ActionVerb, self).getQA().append(QAs)
    def getSubjQA(self):
        return QASpecificWordResponse('What is the subject of ' + self.getWord() + '?',\
         self.getSubject(), ['This verb has no subject'], self.getWord())
class helpingVerb(Verb):
    def __init__(self, w, tense, helped):
        self.helped=helped
        super(helpingVerb, self).__init__(w,'helping verb',tense, isSingular=None)

    def getHelped(self): return self.helped

    def getQA(self):
        questions={'Which verb is this verb helping?':self.verb}
        return super().getQA().append(questions)
        
