from rest_framework import serializers
from betstream.Streamer.models import Edgebet





class EdgebetSerializer(serializers.ModelSerializer):

	class Meta:
		model = Edgebet
