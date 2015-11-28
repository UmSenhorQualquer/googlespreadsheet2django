from googlespreadsheet2django.models.field import *
from googlespreadsheet2django.models.model import *

class ModelsLoader(object):

	def __init__(self, workbook, answers):
		self._models = []

		for worksheetName in workbook.sheet_names():
			if worksheetName.startswith('Table_'):
				worksheet = workbook.sheet_by_name(worksheetName)

				modelname = worksheetName[6:]
				model = Model(self, modelname, worksheet, answers)
				self._models.append( model )

	def getModel(self, name):
		for m in self._models:
			if m._name == name: return m
		return None

	def saveModel(self, path):
		for model in self._models: model.saveModel(path)

	def updateModel(self, path):
		for model in self._models: model.updateModel(path)

	def updateAdmin(self, path):
		for model in self._models: model.updateAdmin(path)

	def saveAdmin(self, path):
		for model in self._models: model.saveAdmin(path)

	def saveJs(self, path):
		for model in self._models: model.saveJs(path)

	@property
	def applications(self):
		res = []
		for m in self._models:
			res.append(m._application)
		return list(set(res))