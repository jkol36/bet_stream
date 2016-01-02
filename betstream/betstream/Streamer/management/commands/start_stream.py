from django.core.management.base import BaseCommand, CommandError
from betstream.Streamer.bet_stream import BetStream

class Command(BaseCommand):
	help = "Starts the streamer"

	def handle(self, *args, **kwargs):
		b = BetStream(place_bet=True)
		with b:
			while True:
				b.run()