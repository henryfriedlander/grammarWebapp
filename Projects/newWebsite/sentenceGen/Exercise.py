import abc
from QuestionHelper import makeWhomQuestion

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