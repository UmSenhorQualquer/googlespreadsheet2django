
from details.models import Person
from django.forms import Textarea, CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.conf import settings
from django.db import models
from common.admintools import export_xlsx, printable_html

class PersonAdminAbstract(admin.ModelAdmin):

	change_form_template = 'admin/my_change_form.html'

	list_display = ('person_id','demographics_gender','demographics_age','person_creationDate','person_updateDate','person_user',)
	list_filter = ('demographics_gender','demographics_age',)
	search_fields = ['person_id',]
	readonly_fields = ('person_id', 'person_creationDate', 'person_updateDate', 'person_user',)

	fieldsets = [
		('Demographics',{
			'classes': ('suit-tab suit-tab-2demographics',),
			'fields': ['demographics_gender','demographics_age','demographics_weight','demographics_weight']
		}),
	]
	suit_form_tabs = [
		(u'2demographics', u'2. Demographics')
	]


	radio_fields = {
		'demographics_gender': admin.VERTICAL
	}

	actions = [export_xlsx,]
				
	formfield_overrides = dict((
		(models.TextField,dict((( 'widget',Textarea(attrs=dict(rows=5, cols=120,style='width: 600px;') )),) )),
		(models.ManyToManyField,dict((('widget',CheckboxSelectMultiple),)))
	),)

	class Media:
		css = dict(all=['generic.css','fixadmin.css'])
		js = ('generic.js','models/person.js')

	def save_model(self, request, obj, form, change):
		if obj.pk==None: obj.person_user = request.user
		super(PersonAdminAbstract, self).save_model(request, obj, form, change)

	def queryset(self, request):
		qs = super(PersonAdminAbstract, self).queryset(request)
		groups = request.user.groups.all()
		qs = qs.filter( person_user__groups = groups ).distinct()
		return qs


	def get_actions(self, request):
		actions = super(PersonAdminAbstract, self).get_actions(request)

		user = request.user
		#if not user.groups.filter(name=settings.HTML_EXPORTER_PROFILE_GROUP).exists(): del actions['printable_html']
		if not user.groups.filter(name=settings.EXCEL_EXPORTER_PROFILE_GROUP).exists(): del actions['export_xlsx']
		return actions
			
	def construct_change_message(self, request, form, formsets):
		message = super(PersonAdminAbstract, self).construct_change_message(request, form, formsets)
		change_message = []
		if form.changed_data:
			values = []
			for x in form.changed_data:
				field   = form.fields[x]
				initial = form.initial[x]
				value 	= form.cleaned_data[x]
				if isinstance(field, ModelMultipleChoiceField): 
					value 	= [int(y.pk) for y in value]
					initial = [int(y) for y in initial]

				values.append( _("<b>%s</b>: <span style='color:#4682B4' >%s</span> -> <span style='color:#00A600' >%s</span>" % (x, str(initial), str(value)) ) )
			change_message.append( '<ul><li>%s</li></ul>' % '</li><li>'.join(values) )
			message += ' '.join(change_message)
		return message

				