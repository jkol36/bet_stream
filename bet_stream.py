#Script Name 	:bet_stream.py
#Author 		: Jon Kolman

#Created 		:October 15th, 2015

#Last Modified : October 22, 2015

#Version  	: 1.0


# description : Listens for new edgebets, checks to see if they're from Bovada returns the url if the bet is indeed on bovada


import os
import sys
import pusherclient #import the library module
import time #import the library module
import json #import the library module
from utils import search_dictionary_for_certain_keys as search_dictionary, get_val  #import the library module
import logging
from get_bovada_matches import get_bovada_matches
from bovadaAPI.bovadaAPI.api import BovadaApi
from bovadaAPI.bovadaAPI.headers import get_bovada_headers_generic
from bet_placer import PlaceBet
from mymodels import Match
from validate_bet import validate_bet, find_outcome
from kelly import Kelly








def on_edge(data):
	bovada_bets = return_bovada_bets(data=data) 

	for edgebet in bovada_bets: # for each bovada bet
		edge = get_val(edgebet, "edge")
		match_id = get_val(edgebet, "match_id")
		bookmaker_id = get_val(edgebet, "bookmaker_id")
		sport = get_val(edgebet, "sport")
		home_team = get_val(edgebet, "home_team")
		away_team = get_val(edgebet, "away_team")
		odds = get_val(edgebet, "odds")
		odds_type = get_val(edgebet, "odds_type")
		total_value = get_val(edgebet, "total_value")
		total_line = get_val(edgebet, "total_line")
		spread_value = get_val(edgebet, "spread_value")
		spread_line = get_val(edgebet, "spread_line")
		moneyline = get_val(edgebet, "moneyline")
		edgebet_id = get_val(edgebet, "edgebet_id")
		
		
		if(
			edge and
			match_id and
			edgebet_id and
			bookmaker_id and
			sport and
			home_team  and
			away_team  and
			odds  and
			odds_type  and
			edge >= 1.0 and 
			match_id in [x.id for x in placed_bets] and
			edgebet_id not in [x.edgebet_id for x in placed_bets] or
			match_id not in [x.id for x in placed_bets]
		):
			try:
				valid_outcome_object = validate_bet(edgebet, bovada_matches)
			except Exception, e:
				print e
				print "validate bet failed"
				pass
			else:
				try:
					b = BovadaApi()
					cookies = b.auth["cookies"]
					headers = get_bovada_headers_generic()
					p = PlaceBet()
					stake = Kelly.get_stake(odds=odds, edge=edge, current_bank_roll=b.balance)
					data = p.build_bet_selection(outcomeId=valid_outcome_object.outcome_id, priceId=valid_outcome_object.price_id, stake=stake)
					if stake >= 1:
						print "placing bet"
						just_do_it = p.place(data=json.dumps(data), cookies=cookies, headers=headers)
						if just_do_it:
							placed_bets.append(Match(id=match_id, edgebet_id=edgebet_id, bookmaker_id=bookmaker_id, stake=stake))
					else:
						print "stake to small"
				except Exception, e:
					print e
		else:
			print "fuck"
			pass




			

			



#check if the edgebet is a bovada bet
def return_bovada_bets(data):
	bets = json.loads(data) # loads the bets as a json object
	new_edgebets = [edgebet for edgebet in bets['new_edges']] #create a new list of just the items inside the new_edges list
	bovada_bets = [] #our variable where we will store any bovada_bets that are found
	for new_edge in new_edgebets:
		try:
			edge = float(new_edge['edge']) #check if the edgebet has an edge. I put this in a try/except so i can catch any key error that may arise.
		except (IndexError, ValueError, KeyError):
			edge = None #if we can't convert the edge to a float, or a valueerror/keyerror is raised (no edge is present), we'll set the edge to None. and we will just pass on it. 
		output = new_edge['output']
		offer = new_edge['o2']['offer'] 
		odds_type = get_odds_type(offer['odds_type'])
		bookmaker = new_edge["o2"]["offer"]["bookmaker"]["name"]
		bookmaker_id = int(new_edge["o2"]["offer"]["bookmaker"]["id"])
		time = search_dictionary("time", offer)
		match_id = search_dictionary("match", offer)["id"]
		sport = search_dictionary("sport", offer)['name']
		start_time = search_dictionary("start_time", offer)
		edgebet_id = search_dictionary("id", offer)
		home_team = search_dictionary("hteam", offer)['name']
		away_team = search_dictionary("ateam", offer)['name']
		odds = float(new_edge['o2']['o1'])

		try:
			handicap = float(new_edge["o2"]["o3"])
		except KeyError, e:
			handicap = None

		
		#new_edge.output not to be confused with something else
		if output == 1:
			outcome_type = "H" if "moneyline" in odds_type.lower() else "H" if "spread" in odds_type.lower() else "O" 
			

		elif output == 2:
			outcome_type = "D" if "moneyline" in odds_type.lower() else "A" if "spread" in odds_type.lower() else "U"
			

		elif output == 3:
			outcome_type = "A"
		
			


		if bookmaker == "Bovada":
			bovada_bets.append(
			{"home_team": home_team, 
			"away_team": away_team, 
			"odds": odds,
			"handicap": handicap,
			"bookmaker_id": bookmaker_id,
			"match_id": match_id,
			"time": time,
			"start_time": start_time,
			"odds_type": odds_type,
			'edge': edge,
			'sport': sport,
			"edgebet_id": edgebet_id})
		elif testing == True:
			bovada_bets.append({
				"home_team": home_team, 
				"away_team": away_team, 
				"odds": odds,
				"bookmaker_id":bookmaker_id,
				"match_id": match_id,
				'edge': edge,
				'sport': sport,
				"odds_type": odds_type,
				"edgebet_id": edgebet_id,
				"time": time,
				"start_time": start_time}
			)
	return bovada_bets

			
			
			
		

		


	


def get_odds_type(num):
	if num == 5:
		return "handicap"
	if num == 4:
		return "Total"

	elif num == 3:
		return "PointSpread"

	elif num == 1:
		return "Moneyline"

	elif num == 0:
		return "3-WayMoneyline" #threeway money line



def connection_handler(data):
	print "binding"
	channel = pusher.subscribe("edgebets")
	channel.bind("edge_changes", on_edge)

def run():
	print "running"
	global bovada_matches
	log = logging.getLogger()
	log.addHandler(logging.FileHandler("betstream.log"))
	bovada_matches = get_bovada_matches()
	global pusher #make pusher a global variable so it's accessible throughout the script
	global placed_bets
	global testing
	testing = False
	placed_bets = []
	appkey = "c11ef000e51c34bac2fc"
	pusher = pusherclient.Pusher(appkey)
	pusher.connection.bind('pusher:connection_established', connection_handler)
	pusher.connect()
	checker = time.time()
	while True:
		if checker - time.time() > 2000:
			print "refetching bovada matches"
			bovada_matches = get_bovada_matches()
		log.log(logging.INFO, sys.stdout)


run()
