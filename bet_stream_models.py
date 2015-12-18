


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
		self.home_team = home_team
		self.away_team = away_team
		self.sport = sport
		self.odds_type = odds_type
		self.odds = odds
		self.handicap = handicap
		self.outcome_type = outcome_type
		
		return super(Bet, self).__init__()

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
		return super(Bovadabet, self).__init__(*args, **kwargs)
	
	@classmethod
	def create(cls, BovadaMatch):
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
			elif odds_type == "Total" or "Total" in "".join(odds_type.split(" ")):
				odds_type = 4
			elif odds_type == "3-Way Moneyline":
				odds_type = 0
			odds = outcome.odds
			handicap = outcome.handicap

			yield cls(
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





