from django.core.management.base import BaseCommand, CommandError
from betstream.Streamer.models import Edgebet, Bovadabet
from betstream.Streamer.track_outcomes import track
from django.utils import timezone


class Command(BaseCommand):
	help = "instantiates a new socket connection for each pending game"


	def handle(self, *args, **kwargs):
		for bovadabet in Bovadabet.objects.filter(is_placed=True):
			track(bovadabet.match_id)