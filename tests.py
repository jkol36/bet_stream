import unittest
import json
#from bovadaAPI.bovadaAPI.api import BovadaApi


data = json.dumps({"event":"edge_changes","data":"{\"new_edges\": [{\"id\": 18420123, \"o1\": {\"id\": 396287933, \"o1\": \"1.787\", \"o2\": \"2.070\", \"o3\": \"55.500\", \"o4\": \"0.000\", \"offer\": {\"id\": 381601627, \"last_verified\": \"2015-12-05T19:30:44Z\"}}, \"o2\": {\"id\": 395745053, \"offer\": {\"id\": 382598316, \"bookmaker\": {\"id\": 234, \"name\": \"5 dimes / Island Casino\", \"url\": \"http://www.5dimes.eu/\"}, \"match\": {\"id\": 3441772, \"minorgroup\": {\"id\": 25167, \"mastergroup\": {\"sport\": {\"name\": \"us football\"}, \"country\": {\"id\": 367, \"name\": \"NCAA\"}}, \"name\": \"NCAA Division I FBS > Regular Season\"}, \"hteam\": {\"name\": \"Southern California Trojans\"}, \"ateam\": {\"name\": \"Stanford Cardinal\"}, \"start_time\": \"2015-12-06T00:45:00Z\"}, \"odds_type\": 4, \"last_verified\": \"2015-12-05T19:20:25Z\"}, \"time\": \"2015-12-05T16:12:24Z\", \"o1\": \"1.725\", \"o2\": \"2.180\", \"o3\": \"55.500\", \"o4\": \"0.000\"}, \"output\": 2, \"edge\": \"1.010\"}, {\"id\": 18420124, \"o1\": {\"id\": 396287928, \"o1\": \"2.100\", \"o2\": \"1.781\", \"o3\": \"59.000\", \"o4\": \"0.000\", \"offer\": {\"id\": 380618257, \"last_verified\": \"2015-12-05T19:30:44Z\"}}, \"o2\": {\"id\": 396049587, \"offer\": {\"id\": 382407301, \"bookmaker\": {\"id\": 567, \"name\": \"Bovada\", \"url\": \"http://www.bovada.lv/\"}, \"match\": {\"id\": 3441772, \"minorgroup\": {\"id\": 25167, \"mastergroup\": {\"sport\": {\"name\": \"us football\"}, \"country\": {\"id\": 367, \"name\": \"NCAA\"}}, \"name\": \"NCAA Division I FBS > Regular Season\"}, \"hteam\": {\"name\": \"Southern California Trojans\"}, \"ateam\": {\"name\": \"Stanford Cardinal\"}, \"start_time\": \"2015-12-06T00:45:00Z\"}, \"odds_type\": 4, \"last_verified\": \"2015-12-05T19:29:24Z\"}, \"time\": \"2015-12-05T17:50:38Z\", \"o1\": \"1.909\", \"o2\": \"1.909\", \"o3\": \"59.000\", \"o4\": \"0.000\"}, \"output\": 2, \"edge\": \"1.033\"}], \"deleted_edges\": [18418734, 18419977, 18419546, 18419480, 18419475, 18419979, 18419682, 18419365, 18419976, 18419479, 18419364, 18418867, 18420120, 18419975, 18418868]}","channel":"edgebets"})


class TestCreateBovadaMatches(unittest.TestCase):

	def assertOddsOutcomeTypeIsCorrect(self):
		pass

	def runTest(self):
		odds_type = "Moneyline"
		outcome_type = "H" if "moneyline" in odds_type.lower() else "H" if "spread" in odds_type.lower() else "O" 
		
		print outcome_type


t = TestCreateBovadaMatches()
t.runTest()