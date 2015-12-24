import unittest
import json
from betstream.bovadaAPI.bovadaAPI.api import BovadaApi
from betstream.Streamer.streamer_exceptions import StreamerException
from betstream.Streamer.bet_stream import BetStream
from betstream.Streamer.models import Bet, Edgebet, Bovadabet
from datetime import datetime, timedelta
from betstream.Streamer.compare_times import time_difference
from django.utils import timezone
#b = BovadaApi()
#b.auth

#from bovadaAPI.bovadaAPI.api import BovadaApi


data_dump = json.dumps({"event":"edge_changes","data":"{\"new_edges\": [{\"id\": 18420123, \"o1\": {\"id\": 396287933, \"o1\": \"1.787\", \"o2\": \"2.070\", \"o3\": \"55.500\", \"o4\": \"0.000\", \"offer\": {\"id\": 381601627, \"last_verified\": \"2015-12-05T19:30:44Z\"}}, \"o2\": {\"id\": 395745053, \"offer\": {\"id\": 382598316, \"bookmaker\": {\"id\": 234, \"name\": \"5 dimes / Island Casino\", \"url\": \"http://www.5dimes.eu/\"}, \"match\": {\"id\": 3441772, \"minorgroup\": {\"id\": 25167, \"mastergroup\": {\"sport\": {\"name\": \"us football\"}, \"country\": {\"id\": 367, \"name\": \"NCAA\"}}, \"name\": \"NCAA Division I FBS > Regular Season\"}, \"hteam\": {\"name\": \"Southern California Trojans\"}, \"ateam\": {\"name\": \"Stanford Cardinal\"}, \"start_time\": \"2015-12-06T00:45:00Z\"}, \"odds_type\": 4, \"last_verified\": \"2015-12-05T19:20:25Z\"}, \"time\": \"2015-12-05T16:12:24Z\", \"o1\": \"1.725\", \"o2\": \"2.180\", \"o3\": \"55.500\", \"o4\": \"0.000\"}, \"output\": 2, \"edge\": \"1.010\"}, {\"id\": 18420124, \"o1\": {\"id\": 396287928, \"o1\": \"2.100\", \"o2\": \"1.781\", \"o3\": \"59.000\", \"o4\": \"0.000\", \"offer\": {\"id\": 380618257, \"last_verified\": \"2015-12-05T19:30:44Z\"}}, \"o2\": {\"id\": 396049587, \"offer\": {\"id\": 382407301, \"bookmaker\": {\"id\": 567, \"name\": \"Bovada\", \"url\": \"http://www.bovada.lv/\"}, \"match\": {\"id\": 3441772, \"minorgroup\": {\"id\": 25167, \"mastergroup\": {\"sport\": {\"name\": \"us football\"}, \"country\": {\"id\": 367, \"name\": \"NCAA\"}}, \"name\": \"NCAA Division I FBS > Regular Season\"}, \"hteam\": {\"name\": \"Southern California Trojans\"}, \"ateam\": {\"name\": \"Stanford Cardinal\"}, \"start_time\": \"2015-12-06T00:45:00Z\"}, \"odds_type\": 4, \"last_verified\": \"2015-12-05T19:29:24Z\"}, \"time\": \"2015-12-05T17:50:38Z\", \"o1\": \"1.909\", \"o2\": \"1.909\", \"o3\": \"59.000\", \"o4\": \"0.000\"}, \"output\": 2, \"edge\": \"1.033\"}], \"deleted_edges\": [18418734, 18419977, 18419546, 18419480, 18419475, 18419979, 18419682, 18419365, 18419976, 18419479, 18419364, 18418867, 18420120, 18419975, 18418868]}","channel":"edgebets"})
data = json.loads(data_dump)["data"]




class OutcomeFinder(object):
	

	def assertMatchTypeIsValid(self, match_type):
		try:
			endswith_matches = match_type.split("_")[1]
		except IndexError:
			raise Exception("invalid match_type", match_type)
		else:
			if endswith_matches == "matches":
				return True
			else:
				raise Exception("invalid match type ", match_type )

	def assertOutComeAttributeIsNotNone(self, outcome_obj, outcome_attribute):
		return outcome_obj.__getattribute__(outcome_attribute) != None

	def assertOutComeAttributeIsEqualTo(self, outcome_obj=None, outcome_attribute=None, value=None):
		return outcome_obj.__getattribute__(outcome_attribute if outcome_attribute else self.outcome_attribute) == value
	
	def run(self, match_type):
		if self.assertMatchTypeIsValid(match_type):
			pass
		else:
			raise Exception("invalid match_type", match_type)
		for match in b.__getattribute__(match_type):
			for outcome in match.outcomes:
				yield {"match": match, "outcome": outcome}

		




class BetStreamTest(unittest.TestCase):

	def assertOddsOutcomeTypeIsCorrect(self):
		pass

	def assertHandicapEqual(self):
		for match in b.football_matches:
			for outcome in match.outcomes:
				if outcome.handicap == handicap_amount:
					print match.home_team_full_name

	def assertOddsEqual(self):
		pass

	def assert_match_starts_within_two_hours(self, match):
		if match.start_time == None:
			return False
		else:
			#print time_difference(match.start_time)
			return (
				time_difference(match.start_time).seconds <= 7200
				)

	def assertFindMatchWorks(self):
		home_team = "western michigan"
		away_team = "middle tennessee state"
		odds_type = 3
		odds = 1.87
		outcome_type = "H"
		handicap = -4.5
		print Bovadabet.objects.filter(home_team=home_team, away_team=away_team, odds_type=odds_type, odds=odds, outcome_type=outcome_type, handicap=handicap)

	def assertCreationOfBetClassWorksWithoutArgs(self):
		return Bet()

	def assertCreationOfBetClassWorksWithArgs(self):
		return Bet(
			home_team="Test",
			away_team="Test_away",
			sport="basketball",
			odds_type=1,
			odds=1,
			handicap=1,
			outcome_type="H")

	def assertCreationOfBovadaBetWorksWithOutArgs(self):
		return Bovadabet()

	def assertCreationOfBovadaBetWorksWithArgs(self):
		return Bovadabet(
			home_team="Test",
			away_team="Test_away",
			sport="basketball",
			odds_type=1,
			odds=1,
			handicap=1,
			outcome_type="H",
			match_id=12131231,
			outcome_id=123123121,
			price_id=123123123123
			)

	def assertCreationOfEdgebetWorksWithoutArgs(self):
		return Edgebet()

	def assertCreationOfEdgebetWorksWithArgs(self):
		return Edgebet(
			home_team="Test",
			away_team="Test_away",
			sport="basketball",
			odds_type=1,
			odds=1,
			handicap=1,
			outcome_type="H",
			edgebet_id=123123123,
			edge=1.02
			)

	def assertCanGetEdge(self):
		edgebet = self.assertCreationOfEdgebetWorksWithArgs()
		return edgebet.edge


	def assertKellyWorks(self):
		from betstream.Streamer.kelly import Kelly
		api = BovadaApi()
		api.auth
		for edgebet in Edgebet.objects.filter(is_placed=False):
			odds = edgebet.odds
			edge = edgebet.edge
			p_without_edge = Kelly.get_p(odds)
			p_with_edge = p_without_edge + (edge - 1)
			q_without_edge = Kelly.get_q(p_without_edge)
			q_with_edge = Kelly.get_q(p_with_edge)
			b = Kelly.get_b(odds)
			percent_of_bank_roll_without_edge = Kelly.get_percent_of_bank_roll(b, p_without_edge, q_without_edge)
			percent_of_bank_roll_with_edge = Kelly.get_percent_of_bank_roll(b, p_with_edge, q_with_edge)
			stake_without_edge = Kelly.get_stake(percent_of_bank_roll_without_edge, api.balance)
			stake_with_edge = Kelly.get_stake(percent_of_bank_roll_with_edge, api.balance)
			print "_________start____________________________"
			print "the odds are {}".format(odds)
			print "the probability of success without the edge is {}".format(p_without_edge)
			print "the probability of failure without the edge is {}".format(q_without_edge)
			print "the probability of success with the edge is {}".format(p_with_edge)
			print "the probability of failure with edge is {}".format(q_with_edge)
			print "the edge is {}".format(edge)
			print "you should bet {} of your bankroll without the edge".format(percent_of_bank_roll_without_edge)
			print "the best wager for you without edge is {}".format(stake_without_edge)
			print "you should bet {} with the edge".format(percent_of_bank_roll_with_edge)
			print "the best wager for you with edge is {}".format(stake_with_edge)
			print "____________________________________"


	def runTest(self):
		for match in Edgebet.objects.order_by("-start_time"):
			if self.assert_match_starts_within_two_hours(match):
				print "true"
				print match.home_team

	

		#hours_until_event = int(str(t_future - t_now)[0])
		
		
		#date_object = datetime.strptime(future, '%b %d %Y %I:%M%p')


	def assertCanFindMatches(self):
		unmatched_edgebets = []
		for edgebet in Edgebet.objects.filter(
			is_placed=False
			).order_by("-recieved_date"):

			for bovadabet in Bovadabet.objects.filter(is_placed=False).order_by("-date_added"):
				try:
					equal = edgebet == bovadabet or bovadabet == edgebet
				except Exception, e:
					pass
					equal = False
				finally:
					if equal:
						print "found a match"
						break


			unmatched_edgebets.append(edgebet)
		print "number of unmatched edgebets {}".format(len(unmatched_edgebets))
		print "percentage of unmatched_edgebets {}".format(len(unmatched_edgebets / len([x for x in edgebet.objects.all()])))


	def place_edgebets(self):
		for edgebet in Edgebet.objects.all():
			for bovadabet in Bovadabet.objects.all():
				if bovadabet == edgebet:
					print bovadabet.home_team, edgebet.home_team
					print bovadabet.away_team, edgebet.away_team
					print bovadabet.odds_type, edgebet.odds_type
					print bovadabet.outcome_type, edgebet.outcome_type
					print bovadabet.odds, edgebet.odds





t = BetStreamTest()
print t.runTest()