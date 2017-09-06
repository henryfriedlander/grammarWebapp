import abc
from QuestionHelper import *

class Exercise(object):
	def __init__(self, name, exerciseID):
		self.exerciseID = exerciseID
		self.name = name

	@abc.abstractmethod
	def getQuestion(self):
		return

	@abc.abstractmethod
	def getLesson(self):
		return

	def getExerciseID(self):
		return self.exerciseID
	def getName(self):
		return self.name

class WhoOrWhomExercise(Exercise):
	def __init__(self):
		super(WhoOrWhomExercise, self).__init__("Who or Whom?", 0)
	
	def getQuestion(self):
		return makeWhomQuestion()
	def getLesson(self):
		#READ Lesson from some file
		return "WHO OR WHOM EXERCISE LESSON"

class PronounCaseQuestion(Exercise):
	def __init__(self):
		super(PronounCaseQuestion, self).__init__("Pronoun Case?", 1)
	
	def getQuestion(self):
		return makePronounCaseQuestion()
	def getLesson(self):
		#READ Lesson from some file
		return "Pronoun Exercise EXERCISE LESSON"

class VerbIDExercise(Exercise):
	def __init__(self):
		super(VerbIDExercise, self).__init__("Verb ID", 2)
	
	def getQuestion(self):
		return makeVerbIDQuestion()
	def getLesson(self):
		#READ Lesson from some file
		return "Verb ID Exercise EXERCISE LESSON"

class NounIDExercise(Exercise):
	def __init__(self):
		super(NounIDExercise, self).__init__("Noun ID", 3)
	
	def getQuestion(self):
		return makeNounIDQuestion()
	def getLesson(self):
		#READ Lesson from some file
		return "Verb ID Exercise EXERCISE LESSON"

class CapitalizationExercise(Exercise):
	def __init__(self):
		super(CapitalizationExercise, self).__init__("Capitalization ID", 4)
	
	def getQuestion(self):
		return makeCapitalizationQuestion()
	def getLesson(self):
		#READ Lesson from some file
		return "makeCapitalizationQuestion ID Exercise EXERCISE LESSON"

class CommaListExercise(Exercise):
	def __init__(self):
		super(CommaListExercise, self).__init__("Comma List ID", 5)
	
	def getQuestion(self):
		return makeCommaListQuestion()
	def getLesson(self):
		#READ Lesson from some file
		return "makeCommaListQuestion ID Exercise EXERCISE LESSON"

class CommaSeperatingCoordinatingAdjectiveExercise(Exercise):
	def __init__(self):
		super(CommaSeperatingCoordinatingAdjectiveExercise, self).__init__("Comma Seperating Coordinating Adjectives", 6)
	
	def getQuestion(self):
		return makeCommaSeperatingCoordinatingAdjectiveQuestion()
	def getLesson(self):
		#READ Lesson from some file
		return "makeCommaListQuestion ID Exercise EXERCISE LESSON"
