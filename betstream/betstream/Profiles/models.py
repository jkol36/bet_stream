from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from random import random



class ApiKey(models.Model):

	value = models.BigIntegerField()
	is_valid = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now=True)

	def __int__(self):
		return self.value
	@property
	def create_key(self):
		self.value = random.randint(1239102391230192312, 123812938129381231212312)
		return self







class Profile(AbstractBaseUser):

	API_KEY = models.OneToOneField(ApiKey)
	bovada_username = models.CharField(max_length=250, null=True, blank=True)
	bovada_password = models.CharField(max_length=250, null=True, blank=True)


	def __unicode__(self):
		return self.username if self.username else self.email

	@property
	def create_api_key(self):
		self.API_KEY = random.randint(1239102391230192312, 123812938129381231212312)

	








