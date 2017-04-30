from Exercise import *

class ExerciseFactory(object):
	def getExercise(self, exerciseID):
		streID = str(exerciseID)
		if streID == '0':
			return WhoOrWhomExercise()
		else:
			print "bad exerciseID"
			return "exerciseID out of range"