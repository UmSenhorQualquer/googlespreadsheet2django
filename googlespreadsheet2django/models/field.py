# -*- coding: utf-8 -*-
import os

class Field(object):
	CHOICES_ABBR_LEN = 10 # Number of characters in each answer abbreviation (choice)

	def __init__(self, model, answers, tab, group, worksheet, row):

		self._answers 			= answers
		self._model 			= model
		self._tab 				= tab
		self._group 			= group
		self._column 			= worksheet.cell(row, 1).value
		self._label 			= worksheet.cell(row, 0).value
		self._help 				= worksheet.cell(row, 10).value
		self._type 				= worksheet.cell(row, 4).value
		self._size 				= worksheet.cell(row, 5).value
		self._choices 			= worksheet.cell(row, 6).value
		self._mandatory 		= worksheet.cell(row, 7).value=='Yes'
		self._columnDependency 	= worksheet.cell(row, 8).value
		self._valuesDependency 	= worksheet.cell(row, 9).value
		self._visible			= worksheet.cell(row, 11).value=='Yes'
		self._showinlist		= worksheet.cell(row, 12).value
		self._filterby			= worksheet.cell(row, 13).value=='Yes'
		self._searchby			= worksheet.cell(row, 14).value=='Yes'
		self._useonname			= worksheet.cell(row, 15).value
		self._unique			= worksheet.cell(row, 16).value=='Yes'
		self._default			= worksheet.cell(row, 17).value

	def __str__(self): return self.__unicode__()
	def __unicode__(self):
		if self.fieldtype==None: 
			function = '\n\tdef %s(self): pass\n' % self._column
			function += '\t%s.short_description="%s"\n' % (self._column, self._label)
			function += '\t%s.allow_tags=True' % (self._column, )
			return function

		return "\t%s = models.%s(%s)" % ( self.fieldname, self.fieldtype, ", ".join(self.parameters) )
	

	@property
	def choices(self):
		if 'range' in self._type:
			data = self._choices.replace('[','').replace(']','').split(';')
			return map( float, data )
		else:
			return self._choices

	@property
	def size(self):
		if self._type=='Decimal number' or self._type=='Decimal numbers range':
			vals = ("%s" % self._size).split('.')
			return len(vals[0]), len(vals[1])
		if self._type=='Integer' or self._type=='Integers range':
			return len("%d" % self._size)
		else:
			return self._size

	@property
	def fieldname(self): return self._column

	@property
	def label(self): return self._label

	@property
	def help(self): return self._help.replace('\n','')

	

	@property
	def fieldtype(self):

		if self._type=='Created by user': 
			return 'ForeignKey'
		elif self._type=='Creation date and time':
			return 'DateTimeField'
		elif self._type=='Date':
			return 'DateField'
		elif self._type=='Date time':
			return 'DateTimeField'
		elif self._type=='Decimal number':
			return 'DecimalField'
		elif self._type=='Decimal numbers range':
			return 'DecimalField'
		elif self._type=='Drop down list':
			return 'CharField'
		elif self._type=='Email':
			return 'EmailField'
		elif self._type=='File':
			return 'FileField'
		elif self._type=='Foreign key':
			return 'ForeignKey'
		elif self._type=='Function field':
			return None
		elif self._type=='Integer':
			return 'IntegerField'
		elif self._type=='Integers range':
			return 'IntegerField'
		elif self._type=='Multiple choice':
			return 'ManyToManyField'
		elif self._type=='Number of identification':
			return 'AutoField'
		elif self._type=='Radio buttons list':
			return 'CharField'
		elif self._type=='Small text':
			return 'CharField'
		elif self._type=='Slug':
			return 'SlugField'
		elif self._type=='Text':
			return 'TextField'
		elif self._type=='Update date and time':
			return 'DateTimeField'
		elif self._type=='Updated by user':
			return 'ForeignKey'
		elif self._type=='Boolean':
			return 'BooleanField'
		return None
	
	





	@property
	def parameters(self):
		params = []

		if self._type=='Created by user': 
			params.append('User')
			params.append('verbose_name="%s"' % self.label)
			params.append('related_name="{0}_created_by_user"'.format(self.fieldname))

		elif self._type=='Creation date and time':
			params.append('"%s"' % self.label)
			params.append('auto_now_add=True')

		elif self._type=='Date':
			params.append('"%s"' % self.label)

		elif self._type=='Date time':
			params.append('"%s"' % self.label)

		elif self._type=='Decimal number':
			params.append('"%s"' % self.label)
			params.append( "max_digits=%s, decimal_places=%s" % self.size )

		elif self._type=='Decimal numbers range':
			params.append('"%s"' % self.label)
			params.append( "max_digits=%s, decimal_places=%s" % self.size )
			params.append( "validators=[MinValueValidator(%f),MaxValueValidator(%f)]" % tuple(self.choices) )
			
		elif self._type=='Drop down list':
			params.append('"%s"' % self.label)
			
		elif self._type=='Email':
			params.append('"%s"' % self.label)
			params.append( "max_length=100" )

		elif self._type=='File':
			params.append('"%s"' % self.label)
			params.append( "max_length=255" )
			upload_path = os.path.join('uploads', self._model.tablename.lower() )
			params.append( "upload_to='{0}'".format(upload_path) )
		elif self._type=='Foreign key':
			params.append('"%s"' % self._choices)
			params.append('verbose_name="%s"' % self._label)

		elif self._type=='Function field':
			params.append('"%s"' % self.label)
			

		elif self._type=='Integer':
			params.append('"%s"' % self.label)
			params.append( "max_length=%s" 	% self.size )

		elif self._type=='Integers range':
			params.append('"%s"' % self.label)
			params.append( "max_length=%s" 	% self.size )
			params.append( "validators=[MinValueValidator(%d),MaxValueValidator(%d)]" % tuple(self.choices) )
			
		elif self._type=='Multiple choice':
			params.append('"%s"' % self._choices)
			params.append('related_name="%s"' % self.fieldname)
			params.append('verbose_name="%s"' % self.label)
			
		elif self._type=='Number of identification':
			params.append('"%s"' % self.label)
			params.append('primary_key=True')

		elif self._type=='Radio buttons list':
			params.append('"""%s"""' % self.label)

		elif self._type=='Small text':
			params.append('"%s"' % self.label)
			params.append( "max_length=%d" 	% self._size )

		elif self._type=='Slug':
			params.append('"%s"' % self.label)
			params.append( "max_length=%d" 	% self._size )

		elif self._type=='Text':
			params.append('"%s"' % self.label)

		elif self._type=='Boolean':
			params.append('"%s"' % self.label)

		elif self._type=='Update date and time':
			params.append('"%s"' % self.label)
			params.append('auto_now=True')

		elif self._type=='Updated by user':
			params.append('User')
			params.append('verbose_name="Created by user"')
			params.append('related_name="updated_by_user"')

		if self._choices and self.fieldtype=='CharField': 
			params.append( "choices=%s" 	% self._choices )
			#params.append( "max_length=%d" 	% self._answers[self._choices].columnSize )
			params.append( "max_length=%d" 	% Field.CHOICES_ABBR_LEN )

		if self._help: params.append( 'help_text="""%s"""' 	% self.help )
		
			
		if not self._mandatory and self._type!='Number of identification': 
			params.append('null=True,blank=True')

		if self._unique and self._type!='Number of identification': 
			params.append('unique=True')

		if self._default!='':
			default = '"""%s"""' % self._default if isinstance(self._default, basestring) else self._default==1
			params.append( 'default={0}'.format(default) )
		
		return params
