from django.shortcuts import render
from betstream.Streamer.models import Edgebet, Bovadabet
from betstream.Streamer.serializers import EdgebetSerializer
from betstream.Profiles.serializers import BovadaProfileSerializer, ProfileSerializer
from betstream.Profiles.models import BovadaProfile, Profile
from rest_framework import viewsets







class EdgebetViewSet(viewsets.ModelViewSet):
	queryset = Edgebet.objects.filter(is_placed=True)
	serializer_class = EdgebetSerializer


	class Meta:
		model = Edgebet


class BovadaProfileViewSet(viewsets.ModelViewSet):
	queryset = BovadaProfile.objects.all()
	serializer_class = BovadaProfileSerializer

	class Meta:
		model  = BovadaProfile


class ProfileViewSet(viewsets.ModelViewSet):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

	class Meta:
		model  = Profile





# Create your views here.



def Home(request):
	print "got the request"
	return render(request, 'app.html')
