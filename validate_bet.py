import os
import requests
from bovadaAPI.bovadaAPI.was_successful import was_successful
from bovadaAPI.bovadaAPI.headers import get_bovada_headers_generic
from bovadaAPI.bovadaAPI.Parser import BovadaMatch, OutCome
from bovadaAPI.bovadaAPI.search_dictionary_for_certain_keys import search_dictionary_for_certain_keys as search_dictionary



# headers = {"Accept": "application/json", 
# 	"Content-Type":"application/json;charset=utf-8", 
# 	"Connection":"keep-alive", 
# 	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0"}
# response = requests.get("https://sports.bovada.lv/soccer/premier-league/watford-fc-manchester-utd-20151121?json=true", headers=headers)

# for outcome in BovadaMatch.create_from_center_content(response.json()["data"]["regions"]["content_center"]).outcomes:


def find_outcome(edgebet_obj, bovada_match_obj):


	edgebet_obj_odds_type = edgebet_obj["odds_type"]
	
	home_teams_equal = (
			edgebet_obj["home_team"] == bovada_match_obj.home_team_full_name or
			edgebet_obj["home_team"].lower() in bovada_match_obj.home_team_full_name.lower()
		)
	
	away_teams_equal = (
		edgebet_obj["away_team"].lower() in bovada_match_obj.away_team_full_name.lower() or 
		edgebet_obj["away_team"].lower() == bovada_match_obj.away_team_full_name.lower() 
		)
		

	if home_teams_equal == False and away_teams_equal == False:
		return None
	



	if edgebet_obj_odds_type == "Total":
		for outcome_obj in bovada_match_obj.outcomes:
			total_value_equal = edgebet_obj["total_value"] == outcome_obj.total_amount
			outcome_types_equal = edgebet_obj["total_line"] == outcome_obj.outcome_type
			odds_equal = float(edgebet_obj["odds"]) == float(outcome_obj.price_decimal)
			if odds_equal and total_value_equal and outcome_types_equal:
				return outcome_obj
		return None

	
	

	elif (
		edgebet_obj_odds_type == "Point Spread" or 
		edgebet_obj_odds_type == "Goal Spread" or 
		edgebet_obj_odds_type == "Point Spread --sets"
		):
		for outcome_obj in bovada_match_obj.outcomes:
			spread_value_equal = edgebet_obj["spread_value"] == outcome_obj.spread_amount
			outcome_types_equal = edgebet_obj["spread_line"] == outcome_obj.outcome_type
			odds_equal = float(edgebet_obj["odds"]) == float(outcome_obj.price_decimal)
			if odds_equal and spread_value_equal and outcome_types_equal:
				return outcome_obj
			else:
				print "something is not equal"
				
		return None

	elif edgebet_obj_odds_type == "Moneyline" or edgebet_obj_odds_type == "3-Way Moneyline":
		print "moneyline"
		for outcome_obj in bovada_match_obj.outcomes:
			outcome_types_equal = outcome_obj.outcome_type == edgebet_obj["moneyline"]
			odds_equal = float(edgebet_obj["odds"]) == float(outcome_obj.price_decimal)
			print "outcome types equal", outcome_types_equal
			print "odds_equal", odds_equal
			if odds_equal and outcome_types_equal:
				return outcome_obj
		return None




			


def validate_bet(url, edgebet_obj):

	try:
		edgebet_odds_type = edgebet_obj['odds_type']
	except KeyError, e:
		return None

	try:
		edgebet_odds = edgebet_obj["odds"]
	except KeyError, e:
		return None



	#we need all three to continue (put_on, odds, odds_type)
	#if we made it this far without returning....
	response = requests.get(url+"?json=true", headers=get_bovada_headers_generic())
	if was_successful(response):
		bmatch = BovadaMatch.create_from_center_content(response.json()["data"]["regions"]["content_center"])
		if bmatch:
			outcome = find_outcome(edgebet_obj, bmatch)
			return outcome

	else:
		print "validating bet failed"
		print response.reason
		print response.status_code

			