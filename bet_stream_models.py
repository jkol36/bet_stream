


class Bet(object):
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
	def __init__(
		self, 
		home_team=None,
		away_team=None,
		sport=None,
		odds_type=None,
		odds=None,
		handicap=None,
		outcome_type=None,
		*args, 
		**kwargs
		):
		self.home_team = str(home_team)
		self.away_team = str(away_team)
		self.sport = str(sport)
		try:
			self.odds_type = int(odds_type)
		except TypeError:
			pass
		try:
			self.odds = float(odds)
		except TypeError:
			pass
		try:
			self.handicap = float(handicap)
		except TypeError:
			pass
		try:
			self.outcome_type = str(outcome_type)
		except TypeError:
			pass
		return super(Bet, self).__init__(*args, **kwargs)

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
		other_instance.home_team = "".join(x for x in other_instance.home_team.split(" ")).lower()
		other_instance.away_team = "".join(x for x in other_instance.away_team.split(" ")).lower()
		
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
				other_instance.home_team == self.home_team
			)


	def handicapsEqual(self, other_instance):
		return self.handicap == other_instance.handicap

	def oddsEqual(self, other_instance):
		return self.odds == other_instance.odds

	
	def oddsTypeEqual(self, other_instance):
		return (
			self.oddsTypeIsMoneyline and 
			other_instance.oddsTypeIsMoneyline or
			self.oddsTypeIsPointSpread and
			other_instance.oddsTypeIsPointSpread or
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
			else:
				return False





class Bovadabet(Bet):
	def __init__(
		self,
		match_id=None,
		outcome_id=None,
		price_id=None,
		*args, 
		**kwargs
		):
		self.match_id = match_id
		self.outcome_id = outcome_id
		self.price_id = price_id
		return super(Bovadabet, self).__init__()
	
	@classmethod
	def create(cls, BovadaMatch):
		home_team = BovadaMatch.home_team_full_name.lower()
		away_team = BovadaMatch.away_team_full_name.lower()
		match_id = BovadaMatch.game_id
		sport = BovadaMatch.sport
		startTime = BovadaMatch.startTime
		match_url = BovadaMatch.game_link
		for outcome in BovadaMatch.outcomes:
			yield cls(
					match_id= int(match_id) if match_id else None,
					outcome_id=int(outcome.outcome_id) if outcome.outcome_id else None,
					home_team=unicode(home_team) if home_team else None,
					away_team=unicode(away_team) if away_team else None,
					price_id=int(outcome.price_id) if outcome.price_id else None,
					outcome_type=str(outcome.outcome_type) if outcome.outcome_type else None,
					sport = str(sport) if sport else None,
					odds_type = (
						3 if "spread" in "".join(outcome.odds_type.split(" ")).lower() else
						3 if "spread" == outcome.odds_type.lower() else
						1 if "moneyline" == "".join(outcome.odds_type.split(" ")).lower() else
						1 if "moneyline" == outcome.odds_type.lower() else
						1 if "moneyline" in outcome.odds_type.lower() and
						"3way" not in outcome.odds_type.lower() else
						0 if "3way" in "".join(outcome.odds_type.split("-")) else
						0 if "3way" in outcome.odds_type.lower() else
						4 if "total" == "".join(outcome.odds_type.split(" ")).lower() else
						4 if "total" in outcome.odds_type.lower() else
						None
						),
					handicap=float(outcome.handicap) if outcome.handicap else None,
					odds = float(outcome.odds) if outcome.odds else None,
					match_url = str(match_url) if match_url else None
				)


class Edgebet(Bet):
	def __init__(
		self,
		edgebet_id=None,
		edge=None,
		*args, 
		**kwargs
		):
		self.edgebet_id = edgebet_id
		self.edge = edge
		return super(Edgebet, self).__init__(*args, **kwargs)

	@classmethod
	def create(cls, edgebet):
		""" returns a new instance of an Edgebet given a dictionary with 
		key, values"""

		sport = edgebet["o2"]["offer"]["match"]["minorgroup"]["mastergroup"]["sport"]["name"].lower()
		if sport == "us football":
			sport = "football"
		output = edgebet["output"]
		odds_type = edgebet["o2"]["offer"]["odds_type"]
		edgebet_id = edgebet["o2"]["offer"]["id"]
		edge = edgebet["edge"]
		handicap = edgebet["o2"]["o3"]
		match_id = edgebet["o2"]["offer"]["match"]["id"],
		odds_type = edgebet["o2"]["offer"]["odds_type"],
		home_team = edgebet["o2"]["offer"]["match"]["hteam"]["name"],
		away_team = edgebet["o2"]["offer"]["match"]["ateam"]["name"],
		outcome_type = (
			"H" if odds_type == 1 and output == 1 else
			"H" if odds_type == 3 and output == 1 else
			"O" if odds_type == 4 and output == 1 else
			"D" if odds_type == 1 and output == 2 else
			"A" if odds_type == 3 and output == 2 else
			"U" if odds_type == 4 and output == 2 else
			"A" if output == 3 else 
			None

			)
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





