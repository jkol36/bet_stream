from django.core.management.base import BaseCommand
from betstream.Streamer.models import Edgebet, Bovadabet
from betstream.Streamer.track_game import TrackGame
from betstream.Streamer.compare_times import seconds_until_event
import threading
import time



class Command(BaseCommand):
	help = "creates a new thread for each game that needs tracking"

	def fetch_matches_to_track(self):
		print "called"
		for match in Edgebet.objects.filter(is_placed=True, tracked=False).order_by("-start_time"):
			if match.start_time is not None:
				if (
					seconds_until_event(match.start_time) >= -10000 and match.sibling is not None
				):
					if seconds_until_event(match.start_time) < self.closest_match:
						self.closest_match = seconds_until_event(match.start_time)
					x = TrackGame(match)
					self.trackers.append(x)
					match.tracked = True
					match.save()

	def handle(self, *args, **kwargs):
		self.trackers = []
		self.checker = time.time()
		self.closest_match = 100000
		self.fetch_matches_to_track()
		print "closest match starts in {}".format(self.closest_match)
		for tracker in self.trackers:
			tracker.start()
		while True:
			if len(self.trackers) == 0:
				print "no trackers to track"
				time.sleep(1000)
			elif time.time() - self.checker >= 100:
				print "checking if there are new matches to track"
				self.exclude = [x for x in self.trackers]
				self.fetch_matches_to_track()
				self.checker = time.time()
				for tracker in self.trackers:
					if tracker not in self.exclude:
						tracker.start()


			else:
				for tracker in self.trackers:
					if tracker.isAlive() == False:
						self.trackers.remove(tracker)
				print "currently tracking {} matches".format(len(self.trackers))
				scoreboard = [tuple(tracker.current_score) for tracker in self.trackers]
				print scoreboard
				
				time.sleep(self.closest_match if self.closest_match > 0 else 10)





