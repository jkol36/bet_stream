import os
import requests
from bovadaAPI.bovadaAPI.was_successful import was_successful
from bovadaAPI.bovadaAPI.headers import get_bovada_headers_generic
from bovadaAPI.bovadaAPI.Parser import BovadaMatch, OutCome
from bovadaAPI.bovadaAPI.search_dictionary_for_certain_keys import search_dictionary_for_certain_keys as search_dictionary




def find_outcome(edgebet_obj, bovada_matches):
	print "finding outcome"
	sport = edgebet_obj["sport"]
	
	if sport == "soccer":
		bmatches = bovada_matches["soccer_matches"]
	elif sport == "basketball":
		bmatches = bovada_matches["basketball_matches"]

	elif sport == "football" or sport == "us football":
		bmatches = bovada_matches["football_matches"]

	elif sport == "baseball":
		bmatches = bovada_matches["baseball_matches"]

	elif sport == "rugby":
		bmatches = bovada_matches["rugby_matches"]

	else:
		print "got something else for sport %s" % sport
		bmatches = []

	for match in bmatches:
		match_home_team_1 = match.home_team_full_name.split(" ")[0].lower()
		match_home_team_2  = match.home_team_full_name.split(" ")[1].lower()
		match_away_team_1 = match.away_team_full_name.split(" ")[0].lower()
		match_away_team_2 = match.away_team_full_name.split(" ")[1].lower()
		match.home_team_full_name = "".join(x for x in match.home_team_full_name.split(" ")).lower()
		match.away_team_full_name = "".join(x for x in match.away_team_full_name.split(" ")).lower()
		edgebet_obj["home_team"] = "".join(x for x in edgebet_obj["home_team"].split(" ")).lower()
		edgebet_obj["away_team"] = "".join(x for x in edgebet_obj["away_team"].split(" ")).lower()
		home_team_1 =  edgebet_obj["home_team"].lower().split(" ")[0].lower()
		home_team_2 = edgebet_obj["home_team"].lower().split(" ")[1].lower()
		away_team_1 = edgebet_obj["away_team"].lower().split(" ")[0].lower()
		away_team_2 = edgebet_obj["away_team"].lower().split(" ")[1].lower()
		if (
			match.home_team_full_name in edgebet_obj["home_team"] or 
			match.home_team_full_name in home_team_1 or 
			home_team_1 in match.home_team_full_name or 
			match.home_team_full_name in home_team_2 or
			home_team_2 in match.home_team_full_name or
			match.away_team_full_name in edgebet_obj["away_team"] or
			match.away_team_full_name in away_team_1 or 
			away_team_1 in match.away_team_full_name or 
			match.away_team_full_name in away_team_2 or
			away_team_2 in match.away_team_full_name or
			edgebet_obj["home_team"] in match.home_team_full_name or
			edgebet_obj["away_team"] in match.away_team_full_name or
			edgebet_obj["home_team"] == match.home_team_full_name or
			edgebet_obj["away_team"] == match.away_team_full_name or
			match_home_team_1 in home_team_1 or
			match_home_team_1 == home_team_1 or
			home_team_1 in match_home_team_1 or
			home_team_1 == match_home_team_1 or 
			home_team_1 in match_home_team_2 or 
			home_team_1 == match_home_team_2 or
			match_home_team_2 in home_team_1 or
			match_home_team_2 == home_team_1 or
			home_team_1 in match_home_team_2 or
			home_team_1 == match_home_team_2 or
			match_home_team_2 == home_team_2 or
			match_home_team_2 in home_team_2 or
			home_team_2 in match_home_team_2 or 
			match_home_team_2 == home_team_2 or
			match_home_team_2 == home_team_1 or
			match_home_team_2 in home_team_1 or
			match_away_team_1 in away_team_1 or
			match_away_team_1 == away_team_1 or
			away_team_1 in match_away_team_1 or
			away_team_1 == match_away_team_1 or
			away_team_1 in match_away_team_2 or
			match_away_team_2 in away_team_1 or 
			away_team_1 == match_away_team_2 or
			match_away_team_2 == away_team_1 or
			match_away_team_2 == away_team_2 or
			match_away_team_2 in away_team_2 or
			away_team_2 in match_away_team_2

			):
			for outcome in match.outcomes:
				outcome.odds_type = "".join(x for x in outcome.odds_type.split(" ")).lower()
				edgebet_obj["odds_type"] = edgebet_obj["odds_type"].lower()
				if (
					outcome.odds_type in edgebet_obj["odds_type"] or
					outcome.odds_type == edgebet_obj["odds_type"] and
					outcome.odds == edgebet_obj["odds"]
					):
					if (
						"spread" in edgebet_obj["odds_type"] or
						"total" in edgebet_obj["odds_type"] and
						outcome.handicap != edgebet_obj["handicap"]
						
					):
						pass
					else:
						return outcome

	




			


def validate_bet(edgebet_obj, bovada_matches):
	return find_outcome(edgebet_obj, bovada_matches)


			