class QASpecificWordResponse(object): #this object represents a word in a sentence
    def __init__(self, questiontxt, correct_words, answer_choices, originWord):
        self.questiontxt = questiontxt
        self.correct_words = correct_words
        self.answer_choices = answer_choices
        self.originWord = originWord

    # ADD GETTERS/SETTERS 
        