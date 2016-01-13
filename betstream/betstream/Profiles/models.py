from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from random import random





class BovadaProfile(models.Model):
	bovada_username = models.CharField(max_length=250, null=True, blank=True)
	bovada_password = models.CharField(max_length=250, null=True, blank=True)








class Profile(AbstractBaseUser):
	pass

	








