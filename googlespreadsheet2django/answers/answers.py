from googlespreadsheet2django.answers.choice import *

class Answers(object):
	def __init__(self, name):
		self._name = name
		self._choices = []

	def __unicode__(self):
		res = '%s = (\n' % self._name
		res += ",\n".join( map( str, self._choices ) )+','
		res += '\n)\n'

		return res
	def __str__(self): return self.__unicode__()



	def addChoice(self, code, label):
		choice = Choice(code, label)
		self._choices.append( choice )



	@property
	def name(self): return self._name

	@property
	def columnSize(self): return max( [len(x._code) for x in self._choices] )
	
	