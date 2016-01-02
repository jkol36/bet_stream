from django.db import models


class Bet(models.Model):
	"""
	the base class for both BovadaBets and Edgebets and perhaps bets
	from other bookmakers in the future. All attributes defined in the 
	init method are used for comparing an edgebet to a bovadabet to see if
	a particular bovada bet is indeed a edgebet. Or that an edgebet is indeed a bovada bet.

	example:
		instantiate a bovada bet by passing in the home team, away team, sport,
		odds_type, odds, handicap, and outcome_type. And do the same for the edgebet.
		then call the assertOddsEqual() method on either the BovadaBet object or the edgebet obj
		and pass in the other instance your trying to compare odds types with. If odds types match,
		the function will return True, else False.
	"""
	
	home_team = models.CharField(
		max_length = 250, 
		null = True,
		blank = True
		)
	away_team = models.CharField(
		max_length = 250, 
		null = True,
		blank = True
		)
	sport = models.CharField(
		max_length = 250, 
		null = True,
		blank = True
		)

	odds_type = models.IntegerField(
		null = True,
		blank = True
		)

	odds = models.FloatField(
		null = True,
		blank = True
		)

	handicap = models.FloatField(
		null = True,
		blank = True
		)
	outcome_type = models.CharField(
		max_length = 250, 
		null = True,
		blank = True
		)

	date_added = models.DateTimeField(
		null=True,
		auto_now = True
		)

	is_placed = models.BooleanField(default=False)

	win = models.BooleanField(default=False)

	stake = models.FloatField(null=True, blank=True)

	recieved_date = models.DateTimeField(auto_now=True, null=True)

	start_time = models.DateTimeField(null=True)



	def homeOrAwayMatch(self, other_instance):
		"reformat home and away team so both are lowercase and one word."
		self.home_team = "".join(x for x in self.home_team.split(" ")).lower()
		self.away_team = "".join(x for x in self.away_team.split(" ")).lower()
		other_instance.home_team = "".join(other_instance.home_team.split(" ")).lower()
		other_instance.away_team = "".join(other_instance.away_team.split(" ")).lower()
		
		"""
		return true if the home team or away team in either instance is equal to the home team
		or away team in the corresponding instance. Additionally, return true if either home team or away team
		appears in the corresponding instance. 
		Example:
			will return true:
			eagles in philadelphiaeagles
		""" 
		if (
				self.home_team in other_instance.home_team or
				self.away_team in other_instance.away_team or 
				self.home_team == other_instance.home_team or
				self.away_team == other_instance.away_team or
				other_instance.away_team in self.away_team or
				other_instance.away_team == self.away_team or 
				other_instance.home_team == self.home_team or
				other_instance.home_team in self.home_team
			):
			return True


		""" 
		split the home_team and away_team into seperate words at the space.
		return True if any of those words appear in the corresponding object. 

		"""
		self.home_team_split = self.home_team.split(" ")
		self.away_team_split = self.away_team.split(" ")
		self.match = False
		for word in self.home_team_split:
			if (
				word.lower() in other_instance.home_team.lower() or
				word.lower() in other_instance.away_team.lower()
			):
				self.match = True
			pass

		for word in self.away_team_split:
			if (
				word.lower() in other_instance.away_team.lower() or 
				word.lower() in other_instance.home_team.lower()

			):
				self.match = True
			pass
		return self.match

	
	
	
	def __eq__(self, other_instance):

		if not (
			self.homeOrAwayMatch(other_instance) and
			str(self.outcome_type.lower()) == str(other_instance.outcome_type.lower())
		):
			return False
		else:
			if int(self.odds_type) == 4:
				return (
					int(other_instance.odds_type) == 4 and
					float(other_instance.handicap) == self.handicap
					)

			elif int(self.odds_type) == 1:
				return (
					int(other_instance.odds_type) == 1
				)

			elif int(self.odds_type) == 3:
				return (
					int(other_instance.odds_type) == 3 and
					float(self.handicap) == float(other_instance.handicap)
				)

			elif int(self.odds_type) == 0:
				return int(other_instance.odds_type) == 0

			else:
				print "got a different odds type"
				print type(self.odds_type), type(other_instance.odds_type)
				print self.odds_type, other_instance.odds_type




class Bovadabet(Bet):

	match_id = models.IntegerField(
		null = True,
		blank = True,
		)
	price_id = models.IntegerField(
		null = True,
		blank = True
		)
	outcome_id = models.IntegerField(
		null = True,
		blank = True
		)
	match_url = models.CharField(
		max_length = 250,
		null = True,
		blank = True
		)

	def __unicode__(self):
		return unicode(self.match_id)

	
	@classmethod
	def create(cls, BovadaMatch, already_added):
		for outcome in BovadaMatch.outcomes:
			home_team = BovadaMatch.home_team_full_name.lower()
			away_team = BovadaMatch.away_team_full_name.lower()
			match_id = BovadaMatch.game_id
			sport = BovadaMatch.sport
			start_time = BovadaMatch.startTime
			match_url = BovadaMatch.game_link
			odds_type = outcome.odds_type
			odds = outcome.odds
			handicap = outcome.handicap

			if odds_type == "Point Spread" or "Spread" in odds_type:
				odds_type = 3
			elif odds_type == "Moneyline" or odds_type == "Runline":
				odds_type = 1
			elif odds_type == "Total" or "Total" in "".join(odds_type.split(" ")):
				odds_type = 4
			elif odds_type == "3-Way Moneyline":
				odds_type = 0
			

			if (
				outcome.outcome_id and 
				outcome.outcome_id not in already_added
			):

				obj = cls.objects.create(
					match_id= match_id,
					outcome_id=outcome.outcome_id,
					home_team=home_team,
					away_team=away_team,
					price_id=outcome.price_id,
					outcome_type=outcome.outcome_type,
					sport = sport,
					odds_type = odds_type,
					handicap=outcome.handicap,
					odds = outcome.odds,
					match_url = match_url
				)

				obj.save()
				yield obj
		



class Edgebet(Bet):

	edgebet_id = models.IntegerField(
		null = True,
		blank = True
		)
	edge = models.FloatField(
		null = True,
		blank = True
		)

	sibling = models.ForeignKey(Bovadabet, null=True)

	
	
	@classmethod
	def create(cls, edgebet):
		""" returns a new instance of an Edgebet given a dictionary with 
		key, values"""

		sport = edgebet["o2"]["offer"]["match"]["minorgroup"]["mastergroup"]["sport"]["name"].lower()
		if sport == "us football":
			sport = "football"

		try:
			output = int(edgebet["output"])
		except (KeyError, ValueError):
			raise 
		edgebet_id = int(edgebet["o2"]["offer"]["id"])
		edge = float(edgebet["edge"])
		handicap = float(edgebet["o2"]["o3"])
		match_id = int(edgebet["o2"]["offer"]["match"]["id"])
		odds_type = int(edgebet["o2"]["offer"]["odds_type"])
		if isinstance(odds_type, tuple):
			odds_type = odds_type[0]
		else:
			pass
		home_team = edgebet["o2"]["offer"]["match"]["hteam"]["name"]
		away_team = edgebet["o2"]["offer"]["match"]["ateam"]["name"]
		start_time = edgebet["o2"]["offer"]["match"]["start_time"]

		if int(output) == 1:
			#point spread
			if odds_type == 3:
				outcome_type = "H"

			#total
			if odds_type == 4:
				outcome_type = "O"

			#moneyline
			if odds_type == 1:
				outcome_type = "H"

			#3waymoneyline
			if odds_type== 0:
				outcome_type = "H"
		
		elif output == 2:

			#point spread
			if odds_type == 3:
				outcome_type = "A"

			#total
			if odds_type == 4:
				outcome_type = "U"

			#moneyline

			if odds_type == 1:
				outcome_type == "A"

			#3waymoneyline
			if odds_type == 0:
				outcome_type = "D"


		elif output == 3:
			outcome_type = "A"

		else:
			print "output", output
			print type(output)
			outcome_type = None




		odds = (
			edgebet["o2"]["o1"] if output == 1 else
			edgebet["o2"]["o2"] if output == 2 else
			edgebet["o2"]["o3"] if output == 3 else
			None
			)

		if "unicode" in str(type(odds)):
			print "odds is of type unicode. Changing that..."
			odds = str(odds)
			print type(odds)
		
		if "unicode" in str(type(edge)):
			edge = str(edge)

		if "unicode" in str(type(handicap)):
			handicap = str(handicap)


		print "creating edgebet object from blueprint..."
		print (
			"edgebet_id", edgebet_id,
			"edge", edge,
			"home_team", home_team,
			"away_team", away_team,
			"sport", sport,
			"odds_type", odds_type,
			"handicap", handicap,
			"outcome_type", outcome_type,
			"odds", odds,
			"start_time", start_time
			)
		obj =  cls.objects.create(
			edgebet_id = int(edgebet_id),
			edge = float(edge),
			home_team = unicode(home_team),
			away_team = unicode(away_team),
			sport = str(sport),
			odds_type = int(odds_type),
			handicap = float(handicap),
			outcome_type = str(outcome_type),
			odds = float(odds),
			start_time = start_time
		)

		obj.save()
		return obj
	
			
			
		





