from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator




class Country(models.Model):
	country_name = models.CharField("Name", max_length=50)

	class Meta: abstract = True

class Country(models.Model):
	country_id = models.AutoField("Id", primary_key=True)

	class Meta: abstract = True


class AbstractCountry(Country,
	Country):
	
	def __unicode__(self): return str(self.country_name)


	class Meta:
		abstract = True
		verbose_name = "Country"
		verbose_name_plural = "Countries"

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
		return getattr(self,'country_id')!=None and \
			getattr(self,'country_name')!=None
	is_complete.short_description="Complete"
	is_complete.boolean = True
			