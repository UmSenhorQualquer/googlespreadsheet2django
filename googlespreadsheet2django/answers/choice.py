

class Choice(object):
	def __init__(self, code, label):
		self._code = code
		self._label = label

	def __unicode__(self): return "\t('%s',\"\"\"%s\"\"\")" % (self._code, self._label)

	def __str__(self): return self.__unicode__()