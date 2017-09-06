from Exercise import *

class ExerciseFactory(object):
	def getExercise(self, exerciseID):
		streID = str(exerciseID)
		if streID == '0':
			return WhoOrWhomExercise()
		if streID == '1':
			return PronounCaseQuestion()
		if streID == '2':
			return VerbIDExercise()
		if streID == '3':
			return NounIDExercise()
		if streID == '4':
			return CapitalizationExercise()
		if streID == '5':
			return CommaListExercise()
		if streID == '6':
			return CommaSeperatingCoordinatingAdjectiveExercise()
		else:
			print "bad exerciseID"
			return "exerciseID out of range"