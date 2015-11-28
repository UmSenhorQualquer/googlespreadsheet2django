from googlespreadsheet2django.answers.choice import *
from googlespreadsheet2django.answers.answers import *

class AnswersLoader(object):

	def __init__(self, workbook):
		self._answersList = []

		worksheet = workbook.sheet_by_name('Answers')
		
		for line in range(1, worksheet.nrows, 2):
			answersname = worksheet.cell(line, 1).value
			if answersname=='': continue
		
			answers = Answers(answersname)
			self._answersList.append(answers)

			nofCols = worksheet.ncols
			for col in range(2, nofCols):
				answer_code = worksheet.cell(line, col).value
				if answer_code == '': continue
				if isinstance(answer_code, float): answer_code = str(int(answer_code))
				answer_code = answer_code.upper()
				answer_label = worksheet.cell(line+1, col).value
				if isinstance(answer_label, float): answer_label = str(int(answer_label))

				if answer_code=='': continue
				
				answers.addChoice(answer_code, answer_label)
					

	def __unicode__(self):
		res = ""
		for answers in self._answersList:
			res += "%s\n" % str(answers)
		return res

	def codeFor(self, answers):
		res = ""
		for a in self._answersList:
			if a._name in answers:
				res += "%s\n" % str(a)
		return res

	def __str__(self): return self.__unicode__()

	def __getitem__(self, key):
		for row in self._answersList:
			if row._name == key: return row
		return None