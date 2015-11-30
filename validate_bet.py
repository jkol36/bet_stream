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
			edgebet_obj["home_team"].__contains__(bovada_match_obj.home_team_full_name) or 
			edgebet_obj["home_team"] == bovada_match_obj.home_team_full_name or 
			bovada_match_obj.home_team_full_name.__contains__(edgebet_obj["home_team"]) or
			bovada_match_obj.home_team_short_name == edgebet_obj["home_team"] or
			bovada_match_obj.home_team_short_name.__contains__(edgebet_obj["home_team"]) or
			edgebet_obj["home_team"].__contains__(bovada_match_obj.home_team_short_name) or
			bovada_match_obj.home_team_abbreviation == edgebet_obj["home_team"] or
			bovada_match_obj.home_team_abbreviation.__contains__(edgebet_obj["home_team"]) or
			edgebet_obj["home_team"].__contains__(bovada_match_obj.home_team_abbreviation)
		)
	
	away_teams_equal = (
		edgebet_obj["away_team"].__contains__(bovada_match_obj.away_team_full_name) or 
		edgebet_obj["away_team"] == bovada_match_obj.away_team_full_name 
		or bovada_match_obj.away_team_full_name.__contains__(edgebet_obj["away_team"]) or
		bovada_match_obj.away_team_short_name == edgebet_obj["away_team"] or
		bovada_match_obj.away_team_short_name.__contains__(edgebet_obj["away_team"]) or
		edgebet_obj["away_team"].__contains__(bovada_match_obj.away_team_short_name) or
		bovada_match_obj.away_team_abbreviation == edgebet_obj["away_team"] or
		bovada_match_obj.away_team_abbreviation.__contains__(edgebet_obj["away_team"]) or
		edgebet_obj["away_team"].__contains__(bovada_match_obj.away_team_abbreviation))

	if not home_teams_equal and not away_teams_equal:
		return None
	



	if edgebet_obj_odds_type == "Total":
		for outcome_obj in bovada_match_obj.outcomes:
			total_value_equal = edgebet_obj["total_value"] == outcome_obj.total_amount
			odds_equal = float(edgebet_obj["odds"]) == float(outcome_obj.price_decimal)
			if odds_equal and total_value_equal:
				return outcome_obj
		return None

	
	

	elif (
		edgebet_obj_odds_type == "Point Spread" or 
		edgebet_obj_odds_type == "Goal Spread" or 
		edgebet_obj_odds_type == "Point Spread --sets"
		):
		for outcome_obj in bovada_match_obj.outcomes:
			spread_value_equal = edgebet_obj["spread_value"] == outcome_obj.spread_amount
			odds_equal = float(edgebet_obj["odds"]) == float(outcome_obj.price_decimal)
			if odds_equal and spread_value_equal:
				return outcome_obj
		return None

	elif edgebet_obj_odds_type == "Moneyline" or edgebet_obj_odds_type.__contains__('Moneyline'):
		for outcome_obj in bovada_match_obj.outcomes:
			name_equal = (
					edgebet_obj["put_on"] == outcome_obj.name or
					edgebet_obj["put_on"].__contains__(outcome_obj.name) or
					outcome_obj.name.__contains__(edgebet_obj["put_on"])
				)
			odds_equal = float(edgebet_obj["odds"]) == float(outcome_obj.price_decimal)
			if odds_equal and name_equal:
				return outcome_obj
		return None




			


def validate_bet(url, edgebet_obj):
	try:
		edgebet_put_on = edgebet_obj["put_on"]
	except KeyError, e:
		return None

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

			