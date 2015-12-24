from django.core.management.base import BaseCommand, CommandError
from betstream.Streamer.bet_stream import BetStream
from betstream.Streamer.models import Edgebet
from betstream.Streamer.compare_times import hours_until_event

class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		time_until_next_bet = None
		bet_obj = None
		for edgebet in Edgebet.objects.filter(is_placed=True).order_by("-start_time").order_by("-edge"):
			if edgebet.start_time == None:
				#print "start time none"
				continue

			elif edgebet.start_time != None: 
				hrs_till_event = int(hours_until_event(edgebet.start_time))
				if hrs_till_event < 0:
					continue
				if time_until_next_bet == None:
					time_until_next_bet = hrs_till_event
					bet_obj = edgebet
				elif time_until_next_bet != None and time_until_next_bet > hrs_till_event:
					time_until_next_bet = hrs_till_event
					bet_obj = edgebet
		print "your next bet is {} vs {} ({}) and it starts in {} hours. {}". format(bet_obj.home_team, bet_obj.away_team, bet_obj.sport, time_until_next_bet)