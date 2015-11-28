##### auto:start:Person #####
from models import Person
from admins.PersonAdmin import *

class PersonAdmin(PersonAdminAbstract):
	pass
	
	##### auto:end:Person #####
##### auto:start:Country #####
from models import Country
from admins.CountryAdmin import *

class CountryAdmin(CountryAdminAbstract):
	pass
	
	##### auto:end:Country #####
