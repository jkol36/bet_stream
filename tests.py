import unittest
import json
from bovadaAPI.bovadaAPI.api import BovadaApi
from bet_stream_models import Bet, Edgebet, Bovadabet
#b = BovadaApi()
#b.auth

#from bovadaAPI.bovadaAPI.api import BovadaApi


data = json.dumps({"event":"edge_changes","data":"{\"new_edges\": [{\"id\": 18420123, \"o1\": {\"id\": 396287933, \"o1\": \"1.787\", \"o2\": \"2.070\", \"o3\": \"55.500\", \"o4\": \"0.000\", \"offer\": {\"id\": 381601627, \"last_verified\": \"2015-12-05T19:30:44Z\"}}, \"o2\": {\"id\": 395745053, \"offer\": {\"id\": 382598316, \"bookmaker\": {\"id\": 234, \"name\": \"5 dimes / Island Casino\", \"url\": \"http://www.5dimes.eu/\"}, \"match\": {\"id\": 3441772, \"minorgroup\": {\"id\": 25167, \"mastergroup\": {\"sport\": {\"name\": \"us football\"}, \"country\": {\"id\": 367, \"name\": \"NCAA\"}}, \"name\": \"NCAA Division I FBS > Regular Season\"}, \"hteam\": {\"name\": \"Southern California Trojans\"}, \"ateam\": {\"name\": \"Stanford Cardinal\"}, \"start_time\": \"2015-12-06T00:45:00Z\"}, \"odds_type\": 4, \"last_verified\": \"2015-12-05T19:20:25Z\"}, \"time\": \"2015-12-05T16:12:24Z\", \"o1\": \"1.725\", \"o2\": \"2.180\", \"o3\": \"55.500\", \"o4\": \"0.000\"}, \"output\": 2, \"edge\": \"1.010\"}, {\"id\": 18420124, \"o1\": {\"id\": 396287928, \"o1\": \"2.100\", \"o2\": \"1.781\", \"o3\": \"59.000\", \"o4\": \"0.000\", \"offer\": {\"id\": 380618257, \"last_verified\": \"2015-12-05T19:30:44Z\"}}, \"o2\": {\"id\": 396049587, \"offer\": {\"id\": 382407301, \"bookmaker\": {\"id\": 567, \"name\": \"Bovada\", \"url\": \"http://www.bovada.lv/\"}, \"match\": {\"id\": 3441772, \"minorgroup\": {\"id\": 25167, \"mastergroup\": {\"sport\": {\"name\": \"us football\"}, \"country\": {\"id\": 367, \"name\": \"NCAA\"}}, \"name\": \"NCAA Division I FBS > Regular Season\"}, \"hteam\": {\"name\": \"Southern California Trojans\"}, \"ateam\": {\"name\": \"Stanford Cardinal\"}, \"start_time\": \"2015-12-06T00:45:00Z\"}, \"odds_type\": 4, \"last_verified\": \"2015-12-05T19:29:24Z\"}, \"time\": \"2015-12-05T17:50:38Z\", \"o1\": \"1.909\", \"o2\": \"1.909\", \"o3\": \"59.000\", \"o4\": \"0.000\"}, \"output\": 2, \"edge\": \"1.033\"}], \"deleted_edges\": [18418734, 18419977, 18419546, 18419480, 18419475, 18419979, 18419682, 18419365, 18419976, 18419479, 18419364, 18418867, 18420120, 18419975, 18418868]}","channel":"edgebets"})



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





	def runTest(self):
		self.assertCreationOfBetClassWorksWithoutArgs()
		self.assertCreationOfBetClassWorksWithArgs()
		self.assertCreationOfBovadaBetWorksWithOutArgs()
		self.assertCreationOfBovadaBetWorksWithArgs()
		self.assertCanGetEdge()


OF = OutcomeFinder()
def go():
	outcomes = OF.run(match_type="basketball_matches")
	while True:
		try:
			outcome_obj = next(outcomes)
		except StopIteration:
			return False
		else:
			if OF.assertOutComeAttributeIsEqualTo(outcome_obj["outcome"], "odds", 1.909):
				if OF.assertOutComeAttributeIsEqualTo(outcome_obj["outcome"], "odds_type", "Point Spread"):
					if OF.assertOutComeAttributeIsEqualTo(outcome_obj["outcome"], "outcome_type", "A"):
						if OF.assertOutComeAttributeIsEqualTo(outcome_obj["outcome"], "handicap", 13):
							return outcome_obj["match"].home_team_full_name

t = BetStreamTest()
t.runTest()