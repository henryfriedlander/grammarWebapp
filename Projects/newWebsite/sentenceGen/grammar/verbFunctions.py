from POSObjects import *


class ActionVerb(Verb):
    def __init__(self, w, tense, subject = None,
                 isSingular = True, isCompleted = True,
                 isActive = True, isMainVerb = False):
        super(ActionVerb,self).__init__(w,'action verb', tense, subject,
                                        isSingular, isCompleted,
                                        isActive, isMainVerb)
    def getQA(self):
        questions={'What is the subject of this verb?':self.getSubject}
        return super().getQA().append(questions)
class helpingVerb(Verb):
    def __init__(self, w, tense, helped, isSingular=True):
        self.helped=helped
        super(helpingVerb,self).__init__(w,'helping verb',tense,subject)

    def getHelped(self): return self.helped

    def getQA(self):
        questions={'Which verb is this verb helping?':self.verb}
        return super().getQA().append(questions)
        
