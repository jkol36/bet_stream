from django.db import models
from cached_property import cached_property
from django.contrib.auth.models import AbstractUser
from betstream.bovadaAPI.bovadaAPI.api import BovadaApi
from random import random





class BovadaProfile(models.Model):
	bovada_username = models.CharField(max_length=250, null=True, blank=True)
	bovada_password = models.CharField(max_length=250, null=True, blank=True)
	is_valid = models.BooleanField(default=False)
	checked_for_validity = models.BooleanField(default=False)

	def __unicode__(self):
		return self.bovada_username

	@cached_property
	def _auth(self):
		self.b = BovadaApi()
		self.b.auth({"username": self.bovada_username, "password": self.bovada_password})
		return self.b

	@property
	def balance(self):
		return self.b.balance

	@property
	def summary(self):
		return self.b.summary

	@property
	def bet_history_24_hours(self):
		return self.b.bet_history_24_hours

	@property
	def bet_history(self):
		return self.b.bet_history

	@property
	def bet_history_3_days(self):
		return self.b.bet_history_3_days











class Profile(AbstractUser):
	BovadaAccounts = models.ForeignKey(BovadaProfile, null=True)
	pass

	








