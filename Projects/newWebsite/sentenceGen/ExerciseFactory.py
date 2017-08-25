from Exercise import *

class ExerciseFactory(object):
	def getExercise(self, exerciseID):
		streID = str(exerciseID)
		if streID == '0':
			return WhoOrWhomExercise()
		if streID == '1':
			return PronounCaseQuestion()
		else:
			print "bad exerciseID"
			return "exerciseID out of range"