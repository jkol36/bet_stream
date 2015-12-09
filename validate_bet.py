import os
import requests
from bovadaAPI.bovadaAPI.headers import get_bovada_headers_generic
from bovadaAPI.bovadaAPI.Parser import BovadaMatch, OutCome




def validate_bet(edgebet_obj, bovada_matches):
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

	elif sport == "tennis":
		bmatches = bovada_matches["tennis_matches"]

	else:
		print "got something else for sport %s" % sport
		bmatches = []

	for match in bmatches:
		match.home_team_full_name = "".join(x for x in match.home_team_full_name.split(" ")).lower()
		match.away_team_full_name = "".join(x for x in match.away_team_full_name.split(" ")).lower()
		edgebet_obj["home_team"] = "".join(x for x in edgebet_obj["home_team"].split(" ")).lower()
		edgebet_obj["away_team"] = "".join(x for x in edgebet_obj["away_team"].split(" ")).lower()
		
		if (
			match.home_team_full_name in edgebet_obj["home_team"] or 
			match.away_team_full_name in edgebet_obj["away_team"] or
			edgebet_obj["home_team"] in match.home_team_full_name or
			edgebet_obj["away_team"] in match.away_team_full_name 
			):
			print "found home team and away_team"
			#create a new outcome object based on the edgebet
			#compare the outcome object with the bovadamatches outcome object.
			our_ideal_outcome = OutCome(
				odds_type = edgebet_obj["odds_type"],
				outcome_type = edgebet_obj["outcome_type"],
				odds = edgebet_obj["odds"],
				handicap = edgebet_obj["handicap"]

				)
			print "created ideal_outcome object"
			for outcome in match.outcomes:
				#create an identical outcome object minus the name 
				#and price id and outcome_id
				#we'll return the actual object though, not the copy
				copied_outcome = OutCome(
					odds_type = outcome.odds_type,
					outcome_type = outcome.outcome_type,
					odds = outcome.odds,
					handicap = outcome.handicap
					)
				print "created copied outcome object"
				print copied_outcome == our_ideal_outcome
				if copied_outcome != our_ideal_outcome:
					print our_ideal_outcome.odds_type
					print copied_outcome.odds_type
					print our_ideal_outcome.outcome_type
					print copied_outcome.outcome_type
					print our_ideal_outcome.odds
					print copied_outcome.odds
					print our_ideal_outcome.handicap
					print copied_outcome.handicap
				else:
					print "copied_outcome and ideal outcome equal"

						


	


			
