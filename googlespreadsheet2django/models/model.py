import os
from googlespreadsheet2django.models.field import *
from googlespreadsheet2django.models.abstract_model import *

class Model(object):

	FIELDS_STARTROW = 3

	def __init__(self, modelLoader, name, worksheet, answers):
		self._modelLoader = modelLoader
		self._name = name
		self._answers = answers
		self._fields = []

		self._application 			= worksheet.cell(0, 0).value.lower()
		self._verbose_name 			= worksheet.cell(0, 1).value
		self._verbose_name_plural 	= worksheet.cell(0, 2).value
		self._permissions 			= worksheet.cell(0, 3).value

		self.__load(worksheet, answers)


	def __load(self, worksheet, answers):
		self._orderedTables = []
		self._tables = {}

		for row in range(self.FIELDS_STARTROW, worksheet.nrows):
			tab 	= worksheet.cell(row, 2).value
			group 	= worksheet.cell(row, 3).value

			key = "%s - %s" % (tab, group)

			if key not in self._tables:
				
				abstractModel = AbstractModel(tab, group)
				self._tables[key] = abstractModel
				self._orderedTables.append( abstractModel )

			field = Field(self._tables[key], answers, tab, group, worksheet, row)
			self._tables[key].addField(field)
			self._fields.append(field)


	def addField(self, field): self._fields.append(field)

	@property
	def model_unicode(self):
		fs = []
		for f in sorted(self._fields, key=lambda a: a._useonname):
			if f._useonname: fs.append('str(self.'+f._column+')')
		if len(fs)>0:
			return """\n\tdef __unicode__(self): return %s\n""" % "+' - '+".join(fs)
		else:
			return ''

	def __unicode__(self):
		res =  "from django.db import models\n"
		res += "from django.contrib.auth.models import User\n"
		res += "from django.core.validators import MaxValueValidator, MinValueValidator\n"
		#res += '\n'.join(self.foreignModels2Import)
		res += '\n\n'
		res += str( self._answers.codeFor(self.answers) )+"\n\n"


		for model in self._tables.values(): res += "%s\n" % str(model)

		res += '\nclass Abstract%s(%s):' % (self._name, ',\n\t'.join([ model.tablename for model in self._tables.values() ]))
		res += '\n\t%s' % self.model_unicode
		res += '\n\n\tclass Meta:'
		res += '\n\t\tabstract = True'
		res += '\n\t\tverbose_name = "%s"' % self._verbose_name
		res += '\n\t\tverbose_name_plural = "%s"\n' % self._verbose_name_plural

		res += """
			|	def ShowHideIf(self, checkingField, rules):
			|		values, listOfFields = rules
			|		values = values.split(';')
			|		if str(self.__dict__[checkingField]) in values:
			|			for field in listOfFields:
			|				if not self.__dict__[checkingField]!=None: return False
			|		return True
				"""

		res += """
			|	def ShowHideIfManyToMany(self, checkingField, rules):
			|		values, listOfFields = rules
			|		values = values.split(';')
			|		
			|		selected = getattr(self,checkingField).all()
			|		active = False
			|		for v in selected:
			|			if v in values: 
			|				active=True
			|				break
			|		if active:
			|			for field in listOfFields:
			|				if self.__dict__[checkingField]==None: return False
			|		return True
				"""

		
		used_fields = []
		is_complete = []

		
		for field, values, fields2show in self.dependencies.values():
			used_fields += list(values)
			if self[field].fieldtype=='ManyToManyField':
				is_complete.append( "self.ShowHideIfManyToMany('{0}','{1}',{2})".format(field, values, fields2show) )
			else:
				is_complete.append( "self.ShowHideIf('{0}','{1}', {2})".format(field, values,fields2show) )
		
		for field in self._fields:
			if field.fieldname not in used_fields and field.fieldtype!=None and field._visible==True:
				is_complete.append("getattr(self,'{0}')!=None".format( field.fieldname) )

		res +="""
			|	def is_complete(self):
			|		return {0}
			|	is_complete.short_description="Complete"
			|	is_complete.boolean = True
			""".format( ' and \\\n\t\t\t'.join(is_complete), )
		
		res = res.replace('\n\t\t\t|', '\n')

		return res

	@property
	def model(self):
		res = "##### auto:start:%s #####\n" % self._name
		res += "from abstractmodels.%s import Abstract%s\n" % (self._name, self._name)
		res += '\n'
		res += "class %s(Abstract%s):" % (self._name, self._name)
		res += '\n\tpass\n'
		res += "\t##### auto:end:%s #####\n" % self._name
		return res

	@property
	def modelAdmin(self):
		res = """##### auto:start:{0} #####
			from models import {0}
			from admins.{0}Admin import *

			class {0}Admin({0}AdminAbstract):
				pass
				
				##### auto:end:{0} #####\n""".format( self._name)

		res = res.replace('\t\t\t', '')
		return res


	def __str__(self): return self.__unicode__()

	def __strip(self, string):
		for x in [' ','.','-','_']:
			string = string.replace(x, '')
		return string

	@property 
	def foreignModels2Import(self):
		models_to_import = [x.choices for x in self._fields if x._type=='Foreign key' or x._type=='Multiple choice']
		res = []
		for m in models_to_import:
			model = self._modelLoader.getModel(m)
			if model:
				res.append("""from %s.models import %s""" % (model._application, model._name) )
		return res


		


	@property
	def tablename(self): 
		firstfield = self._fields[0]
		return firstfield._column.split('_')[0].title()

	@property
	def list_display(self):
		l = [(x._showinlist, x.fieldname) for x in self._fields if x._showinlist!='']
		l = sorted(l, key=lambda x: x[0])
		return ["'%s'" % x[1] for x in l]

	@property
	def list_filter(self): return [ "'%s'" % x.fieldname for x in self._fields if x._filterby]

	@property
	def search_list(self): return [ "'%s'" % x.fieldname for x in self._fields if x._searchby]

	@property
	def createdByUserField(self):
		for x in self._fields:
			if x._type=='Created by user': return x.fieldname
		return None

	@property
	def answers(self): return [x._choices for x in self._fields if x._choices and x.fieldtype=='CharField']
		
	@property
	def foo(self):
	    return self._foo
	
	@property
	def tab(self): 
		tab = self.__strip(self._tab).replace('\\','')
		return tab.lower()

	@property
	def readonlyFields(self):
		res = []
		for row in self._orderedTables:
			for field in row._fields:
				if field._type in ['Creation date and time','Update date and time','Number of identification','Created by user', 'Function']:
					res.append("'%s'" % field.fieldname)
		return res


	@property
	def admin(self):
		res = "from %s.models import %s\n" % ( self._application, self._name )
		res += "from django.forms import Textarea, CheckboxSelectMultiple\n"
		res += "from django.contrib import admin\n"
		res += "from django.db import models\n\n"

		list_display = ''
		if len(self.list_display)>0:
			list_display = """list_display = (%s,)""" % ','.join(self.list_display)

		list_filter = ''
		if len(self.list_filter)>0:
			list_filter = """list_filter = (%s,)""" % ','.join(self.list_filter)

		search_fields = ''
		if len(self.search_list)>0:
			search_fields = """search_fields = [%s,]""" % ','.join(self.search_list)

		readonly_fields = ''
		if len(self.readonlyFields)>0:
			readonly_fields = "readonly_fields = (%s,)\n" % ", ".join(self.readonlyFields)

		include_tfieldsets = False
		res = "fieldsets = ["
		for x in self._orderedTables:
			if len(x.fieldsList)==0: continue
			include_tfieldsets = True
			fields = "'"+"','".join(x.fieldsList)+"'"
			res += "\n\t\t('%s',{" % x._group.capitalize()
			res += "\n\t\t\t'classes': ('suit-tab suit-tab-%s',)," % x.tab
			res += "\n\t\t\t'fields': [%s]\n\t\t}" % fields
			res += "),"
		res += "\n\t]"

		fieldsets = res if include_tfieldsets else ''

		include_tsuit_form_tabs = False
		listoftabs = []
		res = ''
		for x in self._orderedTables:
			if len(x.fieldsList)==0: continue
			if str((x.tab,x._tab)) not in listoftabs:
				include_tsuit_form_tabs = True
				listoftabs.append( str((x.tab,x._tab)) )

		res += "suit_form_tabs = [\n\t\t"
		res += ",".join(listoftabs)
		res += "\n\t]\n\n"

		tsuit_form_tabs = res if include_tsuit_form_tabs else ''
		
		fields = []
		for x in self._tables.values():
			for f in x._fields:
				if f._choices and f.fieldtype=='CharField':
					if f._size == 'Horizontal disposition':
						fields.append( "\t\t'%s': admin.HORIZONTAL" % f.fieldname )
					else:
						fields.append( "\t\t'%s': admin.VERTICAL" % f.fieldname )

		radio_fields = ''
		if len(fields)>0:
			radio_fields = "radio_fields = {\n"
			radio_fields += ",\n".join(fields)
			radio_fields += "\n\t}"
		
		#### Restrict access ##########################################################
		createdby = ''
		if self._permissions != 'All data is accessible to users' and self.createdByUserField!=None:
			createdby  = """def save_model(self, request, obj, form, change):\n"""
			createdby += """\t\tif obj.pk==None: obj.%s = request.user\n""" % self.createdByUserField
			createdby += """\t\tsuper(%sAdminAbstract, self).save_model(request, obj, form, change)\n\n""" % self._name

			createdby += '\tdef queryset(self, request):\n'
			createdby += '\t\tqs = super(%sAdminAbstract, self).queryset(request)\n' % self._name
			if self._permissions == 'Restrict data access by the creator':
				createdby += '\t\tqs = qs.filter( %s = request.user )\n' % self.createdByUserField

			if self._permissions == 'Restrict data access by the creator group':
				createdby += "\t\tgroups = request.user.groups.all()\n"
				createdby += '\t\tqs = qs.filter( %s__groups = groups ).distinct()\n' % self.createdByUserField
		
			createdby += '\t\treturn qs\n'	
		###############################################################################
			
		res = """
			|from {6}.models import {0}
			|from django.forms import Textarea, CheckboxSelectMultiple
			|from django.forms.models import ModelMultipleChoiceField
			|from django.utils.translation import ugettext as _
			|from django.contrib import admin
			|from django.conf import settings
			|from django.db import models
			|from common.admintools import export_xlsx, printable_html

			|class {0}AdminAbstract(admin.ModelAdmin):

			|	change_form_template = 'admin/my_change_form.html'

			|	{2}
			|	{4}
			|	{5}
			|	{7}
			|	{8}
			|	{9}
			|	{10}

			|	actions = [export_xlsx,]
				
			|	formfield_overrides = dict((
			|		(models.TextField,dict((( 'widget',Textarea(attrs=dict(rows=5, cols=120,style='width: 600px;') )),) )),
			|		(models.ManyToManyField,dict((('widget',CheckboxSelectMultiple),)))
			|	),)

			|	class Media:
			|		css = dict(all=['generic.css','fixadmin.css'])
			|		js = ('generic.js','models/{1}.js')

			|	{3}

			|	def get_actions(self, request):
			|		actions = super({0}AdminAbstract, self).get_actions(request)

			|		user = request.user
			|		#if not user.groups.filter(name=settings.HTML_EXPORTER_PROFILE_GROUP).exists(): del actions['printable_html']
			|		if not user.groups.filter(name=settings.EXCEL_EXPORTER_PROFILE_GROUP).exists(): del actions['export_xlsx']
			|		return actions
			
			|	def construct_change_message(self, request, form, formsets):
			|		message = super({0}AdminAbstract, self).construct_change_message(request, form, formsets)
			|		change_message = []
			|		if form.changed_data:
			|			values = []
			|			for x in form.changed_data:
			|				field   = form.fields[x]
			|				initial = form.initial[x]
			|				value 	= form.cleaned_data[x]
			|				if isinstance(field, ModelMultipleChoiceField): 
			|					value 	= [int(y.pk) for y in value]
			|					initial = [int(y) for y in initial]

			|				values.append( _("<b>%s</b>: <span style='color:#4682B4' >%s</span> -> <span style='color:#00A600' >%s</span>" % (x, str(initial), str(value)) ) )
			|			change_message.append( '<ul><li>%s</li></ul>' % '</li><li>'.join(values) )
			|			message += ' '.join(change_message)
			|		return message

				""".format(
					self._name, self._name.lower(), list_display,
					createdby, list_filter, search_fields, self._application,
					readonly_fields, fieldsets, tsuit_form_tabs, radio_fields )

		res = res.replace('\n\t\t\t|', '\n')
		return res

	@property
	def dependencies(self):
		"""return a dictionary of fields dependencies configuration"""
		showhide = {}
		for table in self._orderedTables:
			for field in table._fields:
				if field._columnDependency!='':
					k = self[field._columnDependency]

					key = "{0}-{1}".format( k.fieldname, field._valuesDependency )
					if key not in showhide: showhide[key]=(k.fieldname, field._valuesDependency,[])
					showhide[key][2].append(str(field.fieldname))

		return showhide
		

	@property 
	def js(self):
		showhide = self.dependencies

		res = '(function($){ $(document).ready(function(){\n\n'
		for key, values, columns in showhide.values():
			res += "\tShowHideIf( '%s', '%s', %s, true );\n" % (key,values, columns)

		res += '\n\n }); }(Suit.$));'
		return res

	def __getitem__(self, key):
		for row in self._orderedTables:
			for field in row._fields:
				name = field.fieldname
				if name == key: return field

		return None

	def __findModelInFile(self, infile):
		infile.seek(0)
		start, end = None, None
		for i, line in enumerate(infile):
			if start==None and ('auto:start:%s' % self._name) in line: start = i
			if start!=None and ('auto:end:%s' % self._name) in line: 
				end = i
				return start, end
		
		return None

	def __findModelAdminRegistration(self, infile):
		infile.seek(0)
		for i, line in enumerate(infile):
			word = 'admin.site.register(%s, %sAdmin)' % (self._name,self._name)
			if word in line: return i
		return None

	











	def saveAdmin(self, parentPath):
		app_path = os.path.join(parentPath, self._application)
		if not os.path.isdir(app_path): os.mkdir(app_path)

		init_filename = os.path.join(app_path, '__init__.py')
		if not os.path.isfile(app_path):
			outfile = open(init_filename, 'w'); outfile.close()

		admins_path = os.path.join(app_path, 'admins')
		if not os.path.isdir(admins_path): os.mkdir(admins_path)

		init_filename = os.path.join(admins_path, '__init__.py')
		if not os.path.isfile(init_filename):
			outfile = open(init_filename, 'w'); outfile.close()

		admin_filename = os.path.join(admins_path, self._name+'Admin'+'.py')
		outfile = open(admin_filename, 'w')
		outfile.write( self.admin )
		outfile.close()

	def saveJs(self, parentPath):
		static_path = os.path.join(parentPath, 'static')
		if not os.path.isdir(static_path): os.mkdir(static_path)
		js_path = os.path.join(static_path,'js')
		if not os.path.isdir(js_path): os.mkdir(js_path)
		js_path = os.path.join(js_path,'models')
		if not os.path.isdir(js_path): os.mkdir(js_path)

		js_filename = os.path.join(js_path, self._name.lower()+'.js')
		outfile = open(js_filename, 'w')
		outfile.write( self.js )
		outfile.close()

	def saveModel(self, parentPath):
		app_path = os.path.join(parentPath, self._application)
		if not os.path.isdir(app_path): os.mkdir(app_path)

		init_filename = os.path.join(app_path, '__init__.py')
		if not os.path.isfile(app_path):
			outfile = open(init_filename, 'w'); outfile.close()

		models_path = os.path.join(app_path, 'abstractmodels')
		if not os.path.isdir(models_path): os.mkdir(models_path)

		init_filename = os.path.join(models_path, '__init__.py')
		if not os.path.isfile(init_filename):
			outfile = open(init_filename, 'w'); outfile.close()

		model_filename = os.path.join(models_path, self._name+'.py')
		print model_filename
		outfile = open(model_filename, 'w')
		outfile.write( str(self) )
		outfile.close()


	def updateModel(self, parentPath):
		app_path = os.path.join(parentPath, self._application)
		if not os.path.isdir(app_path): os.mkdir(app_path)
		model_filename = os.path.join(app_path, 'models.py')
		if not os.path.isfile(model_filename): open(model_filename, 'w').close()

		infile = open(model_filename, 'r+a')
		position = self.__findModelInFile(infile)
		if position==None: 
			infile.write(self.model)
			
		else:
			infile.seek(0)
			start, end = position
			tmp_filename = os.path.join(app_path, 'tmp.py')
			outfile = open(tmp_filename, 'w')
			for i, line in enumerate(infile):
				if i<start: outfile.write(line)
				if i==start: outfile.write(self.model)
				if i>end: outfile.write(line)
			outfile.close()
			os.rename(tmp_filename, model_filename)
		infile.close()


	def updateAdmin(self, parentPath):


		app_path = os.path.join(parentPath, self._application)
		if not os.path.isdir(app_path): os.mkdir(app_path)
		model_filename = os.path.join(app_path, 'admin.py')
		if not os.path.isfile(model_filename): open(model_filename, 'w').close()

		infile = open(model_filename, 'r+a')
		position = self.__findModelInFile(infile)
		if position==None: 
			infile.write(self.modelAdmin)
			
		else:
			infile.seek(0)
			start, end = position
			tmp_filename = os.path.join(app_path, 'tmp.py')
			outfile = open(tmp_filename, 'w')
			for i, line in enumerate(infile):
				if i<start: outfile.write(line)
				if i==start: outfile.write(self.modelAdmin)
				if i>end: outfile.write(line)
			
			
			adminRegistrationLine = self.__findModelAdminRegistration(infile)
			if adminRegistrationLine==None: 
				outfile.write( 'admin.site.register(%s, %sAdmin)\n' % (self._name,self._name) )

			outfile.close()
			os.rename(tmp_filename, model_filename)


		
		infile.close()
