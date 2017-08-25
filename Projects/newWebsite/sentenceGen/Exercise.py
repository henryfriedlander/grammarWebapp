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