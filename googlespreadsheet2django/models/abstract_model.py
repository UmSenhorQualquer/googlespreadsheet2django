from googlespreadsheet2django.models.field import *

class AbstractModel(object):
	def __init__(self, tab, group):
		self._tab = tab
		self._group = group
		self._fields = []

	def addField(self, field):
		self._fields.append(field)

	
	def __unicode__(self):
		res = "class %s(models.Model):\n" % self.tablename
		res += '\n'.join( map( str, self._fields ) )
		res += '\n\n\tclass Meta: abstract = True\n'
		return res

	def __str__(self): return self.__unicode__()

	def __strip(self, string):
		for x in [' ','.','-','_']:
			string = string.replace(x, '')
		return string

	@property
	def fieldsList(self): 
		return [x.fieldname for x in self._fields if x._visible ]

	@property
	def tablename(self): 
		firstfield = self._fields[0]
		return firstfield._column.split('_')[0].title()

	@property
	def tab(self): 
		tab = self.__strip(self._tab).replace('\\','')
		return tab.lower()
