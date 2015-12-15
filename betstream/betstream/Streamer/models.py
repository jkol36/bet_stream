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
		max_length = 250
		)
	away_team = models.CharField(
		max_length = 250
		)
	sport = models.CharField(
		max_length = 250, 
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
		max_length=1,
		null=True,
		blank=True
		)

	def __init__(self, *args, **kwargs):
		super(Bet, self).__init__(*args, **kwargs)


	@property
	def oddsTypePointSpread(self):
		return self.odds_type == 3

	@property
	def oddsTypeTotal(self):
		return self.odds_type == 4

	@property
	def oddsTypeThreeWayMoneyLine(self):
		return self.odds_type == 0

	

	@property
	def oddsTypeMoneyline(self):
		return self.odds_type == 1

	@property
	def handicapNull(self):
		return self.handicap == None

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
		return (
				self.home_team in other_instance.home_team or
				self.away_team in other_instance.away_team or 
				self.home_team == other_instance.home_team or
				self.away_team == other_instance.away_team or
				other_instance.away_team in self.away_team or
				other_instance.away_team == self.away_team or 
				other_instance.home_team == self.home_team or
				other_instance.home_team in self.home_team
			)


	def handicapsEqual(self, other_instance):
		if type(self.handicap) == type(other_instance.handicap):
			return self.handicap == other_instance.handicap

	def oddsEqual(self, other_instance):
		if type(self.odds) == type(other_instance.odds):
			return self.odds == other_instance.odds
		else:
			try:
				self.odds = float(self.odds)
			except Exception, e:
				return False
			else:
				try:
					other_instance.odds = float(other_instance.odds)
				except Exception, e:
					return False
				return self.odds == other_instance.odds

	
	def oddsTypeEqual(self, other_instance):
		return (
			self.oddsTypeMoneyline and 
			other_instance.oddsTypeMoneyline or
			self.oddsTypePointSpread and
			other_instance.oddsTypePointSpread or
			self.oddsTypeMoneyline and 
			other_instance.oddsTypeMoneyline or
			self.oddsTypeTotal and 
			other_instance.oddsTypeTotal
		)

	def outcomeTypesEqual(self, other_instance):
		return self.outcome_type.lower() == other_instance.outcome_type.lower()
	
	def __eq__(self, other_instance):

		if not (
			self.homeOrAwayMatch(other_instance) and
			self.oddsEqual(other_instance) and
			self.oddsTypeEqual(other_instance) and
			self.outcomeTypesEqual(other_instance)
		):
			return False
		else:
			if self.oddsTypeTotal:
				return (
					other_instance.oddsTypeTotal and
					self.handicapsEqual(other_instance)
					)

			elif self.oddsTypeMoneyline:
				return (
					other_instance.oddsTypeMoneyline
				)

			elif self.oddsTypePointSpread:
				return (
					other_instance.oddsTypePointSpread and
					self.handicapsEqual(other_instance)
				)

			elif self.oddsTypeThreeWayMoneyLine:
				return other_instance.oddsTypeThreeWayMoneyLine
			return False





class Bovadabet(Bet):

	match_id = models.IntegerField(
		null = True,
		blank=True
		)
	outcome_id = models.IntegerField(
		null = True,
		blank = True
		)
	price_id = models.IntegerField(
		null = True,
		blank = True
		)
	match_url = models.URLField(
		max_length=250, 
		null=True
		)
	
	@classmethod
	def create(cls, BovadaMatch, *args, **kwargs):
		for outcome in BovadaMatch.outcomes:
			home_team = BovadaMatch.home_team_full_name.lower()
			away_team = BovadaMatch.away_team_full_name.lower()
			match_id = BovadaMatch.game_id
			sport = BovadaMatch.sport
			start_time = BovadaMatch.startTime
			match_url = BovadaMatch.game_link
			odds_type = outcome.odds_type
			if odds_type == "Point Spread" or "Spread" in odds_type:
				odds_type = 3
			elif odds_type == "Moneyline":
				odds_type = 1
			elif odds_type == "Total":
				odds_type = 4
			elif odds_type == "3-Way Moneyline":
				odds_type = 0
			odds = outcome.odds
			handicap = outcome.handicap

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
			print "saving"
			obj.save()
			yield obj



class Edgebet(Bet):

	edgebet_id = models.IntegerField(
		null = True,
		blank =  True
		)
	edge = models.FloatField(
		null = True,
		blank = True
		)

	recieved_date = models.DateTimeField(
		null = True,
		auto_now=True
	)
	is_placed = models.BooleanField(
		default=False)

	sibling = models.OneToOneField(
		Bovadabet,
		null = True
		)


	
	@classmethod
	def create(cls, edgebet):
		""" returns a new instance of an Edgebet given a dictionary with 
		key, values"""

		sport = edgebet["o2"]["offer"]["match"]["minorgroup"]["mastergroup"]["sport"]["name"].lower()
		if sport == "us football":
			sport = "football"
		output = edgebet["output"]
		edgebet_id = edgebet["o2"]["offer"]["id"]
		edge = edgebet["edge"]
		handicap = edgebet["o2"]["o3"]
		match_id = edgebet["o2"]["offer"]["match"]["id"]
		odds_type = edgebet["o2"]["offer"]["odds_type"]
		if isinstance(odds_type, tuple):
			odds_type = odds_type[0]
		else:
			pass
		home_team = edgebet["o2"]["offer"]["match"]["hteam"]["name"]
		away_team = edgebet["o2"]["offer"]["match"]["ateam"]["name"]
		start_time = edgebet["o2"]["offer"]["match"]["start_time"]
		if output == 1:
			#point spread
			if odds_type == 3:
				outcome_type = "H"

			#total
			elif odds_type == 4:
				outcome_type = "O"

			#moneyline
			elif odds_type == 1:
				outcome_type = "H"

			#3waymoneyline
			elif odds_type== 0:
				outcome_type = "H"
		
		elif output == 2:

			#point spread
			if odds_type == 3:
				outcome_type = "A"

			#total
			elif odds_type == 4:
				outcome_type = "U"

			#moneyline

			elif odds_type == 1:
				outcome_type == "A"

			#3waymoneyline
			elif odds_type == 0:
				outcome_type = "D"

		elif output == 3:
			outcome_type = "A"




		odds = (
			edgebet["o2"]["o1"] if output == 1 else
			edgebet["o2"]["o2"] if output == 2 else
			edgebet["o2"]["o3"] if output == 3 else
			None
			)

		
		
		return cls(
			edgebet_id = int(edgebet_id) if edgebet_id else None,
			edge = float(edge) if edge else None,
			home_team = unicode(home_team) if home_team else None,
			away_team = unicode(away_team) if away_team else None,
			sport = str(sport) if sport else None,
			odds_type = int(odds_type) if odds_type else None,
			handicap = float(handicap) if handicap else None,
			outcome_type = str(outcome_type) if outcome_type else None,
			odds = float(odds) if odds else None
			)





