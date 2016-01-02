from django.shortcuts import render
from betstream.Streamer.models import Edgebet, Bovadabet
from betstream.Streamer.serializers import EdgebetSerializer
from rest_framework import viewsets







class EdgebetViewSet(viewsets.ModelViewSet):
	queryset = Edgebet.objects.filter(is_placed=True)
	serializer_class = EdgebetSerializer

	def __init__(self, *args, **kwargs):
		print "I'm a viewset and ive been initialized"
		print "this is my kwargs"
		print kwargs
		print "this is my args"
		print args
		super(EdgebetViewSet, self).__init__(*args, **kwargs)


	class Meta:
		model = Edgebet




# Create your views here.



def Home(request):
	return render(request, 'app.html')
