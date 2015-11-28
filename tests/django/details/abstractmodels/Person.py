from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


GENDER = (
	('F',"""Female"""),
	('M',"""Male"""),
)

GENDER = (
	('M',"""Make"""),
	('F',"""Female"""),
)



class Person(models.Model):
	person_id = models.AutoField("Person ID", primary_key=True)
	person_creationDate = models.DateTimeField("Created on", auto_now_add=True)
	person_updateDate = models.DateTimeField("Updated on", auto_now=True)
	person_user = models.ForeignKey(User, verbose_name="Created by", related_name="created_by_user")

	class Meta: abstract = True

class Demographics(models.Model):
	demographics_gender = models.CharField("""Gender""", choices=GENDER, max_length=10)
	demographics_age = models.IntegerField("Age", max_length=3)
	demographics_weight = models.DecimalField("Weight", max_digits=5, decimal_places=3, validators=[MinValueValidator(20.000000),MaxValueValidator(200.000000)])
	demographics_weight = models.ForeignKey("Country", verbose_name="Country")

	class Meta: abstract = True


class AbstractPerson(Person,
	Demographics):
	
	def __unicode__(self): return str(self.person_id)+' - '+str(self.demographics_gender)+' - '+str(self.demographics_age)


	class Meta:
		abstract = True
		verbose_name = "Person"
		verbose_name_plural = "People"

	def ShowHideIf(self, checkingField, rules):
		values, listOfFields = rules
		values = values.split(';')
		if str(self.__dict__[checkingField]) in values:
			for field in listOfFields:
				if not self.__dict__[checkingField]!=None: return False
		return True
				
	def ShowHideIfManyToMany(self, checkingField, rules):
		values, listOfFields = rules
		values = values.split(';')
		
		selected = getattr(self,checkingField).all()
		active = False
		for v in selected:
			if v in values: 
				active=True
				break
		if active:
			for field in listOfFields:
				if self.__dict__[checkingField]==None: return False
		return True
				
	def is_complete(self):
		return getattr(self,'demographics_gender')!=None and \
			getattr(self,'demographics_age')!=None and \
			getattr(self,'demographics_weight')!=None and \
			getattr(self,'demographics_weight')!=None
	is_complete.short_description="Complete"
	is_complete.boolean = True
			