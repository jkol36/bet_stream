from rest_framework import serializers
from .models import BovadaProfile, Profile





class BovadaProfileSerializer(serializers.ModelSerializer):

	class Meta:
		model = BovadaProfile



class ProfileSerializer(serializers.ModelSerializer):

	class Meta:
		model = Profile

