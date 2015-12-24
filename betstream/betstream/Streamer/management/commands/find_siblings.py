from django.core.management.base import BaseCommand, CommandError
from betstream.Streamer.models import Bovadabet, Edgebet

class Command(BaseCommand):
	help = "Starts the streamer"

	def handle(self, *args, **kwargs):
		for edgebet in Edgebet.objects.filter(is_placed=True):
			for bovadabet in Bovadabet.objects.filter(is_placed=True):
				try:
					equal = edgebet == bovadabet or bovadabet == edgebet
				except Exception, e:
					equal = False
				finally:
					if equal:
						edgebet.sibling = bovadabet
						edgebet.save()
						break