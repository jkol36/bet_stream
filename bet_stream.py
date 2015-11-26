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
from search_dictionary_for_certain_keys import search_dictionary_for_certain_keys as search_dictionary  #import the library module
import logging
from bovadaAPI.bovadaAPI.api import BovadaApi
from bovadaAPI.bovadaAPI.headers import get_bovada_headers_generic
from bet_placer import PlaceBet
from validate_bet import validate_bet
from mymodels import Match
from connect_to_db import get_session
from kelly import Kelly





def get_bovada_matches():
	print "hang tight, fetching the latest matches from bovada. This can take a while."
	b = BovadaApi()
	b.auth
	soccer_matches = b.soccer_matches
	basketball_matches = b.basketball_matches
	tennis_matches = b.tennis_matches
	rugby_matches = b.rugby_matches
	football_matches = b.football_matches
	baseball_matches = b.baseball_matches


	return {
		"soccer_matches": soccer_matches,
		"basketball_matches": basketball_matches,
		"football_matches": football_matches,
		"rugby_matches": rugby_matches,
		"tennis_matches": tennis_matches,
		"baseball_matches": baseball_matches
	}
def on_edge(data):
	print "number of placed bets {}".format(len(placed_bets))
	bovada_bets = return_bovada_bets(data=data) #parse the data dictonary
	#if bovada_bets: # if any bovada bets are found (checking to see of the bookmaker key's value == "bovada")
	for bet in bovada_bets: # for each bovada bet
		print "got new bovada bet"
		#print "bet odds type: {}".format(bet["odds_type"])
		url = find_url_for_bet(bet)
		if url:
			edge = bet['edge']
			match_id = bet['match_id']
			odds = bet["odds"]
			edgebet_id = bet["edgebet_id"]
			bookmaker_id = bet["bookmaker_id"]
			print "edge {}".format(edge)
			print "odds {}".format(odds)
			if (
				edge >= 1.0 and 
				match_id not in [x.id for x in placed_bets]):
				valid_outcome_object = validate_bet(url, bet) #scrapes the url, parses the response, and returns a new bovadamatch object.
				if valid_outcome_object:
					try:
						b = BovadaApi()
						cookies = b.auth["cookies"]
						headers = get_bovada_headers_generic()
						p = PlaceBet()
						stake = Kelly.get_stake(odds=odds, edge=edge, current_bank_roll=b.balance)
						stake = stake * 100
						print "stake {}".format(stake)
						print valid_outcome_object.outcome_id
						data = p.build_bet_selection(outcomeId=valid_outcome_object.outcome_id, priceId=valid_outcome_object.price_id, stake=stake)
						if stake >= 1:
							just_do_it = p.place(data=json.dumps(data), cookies=cookies, headers=headers)
							print just_do_it
							if just_do_it:
								placed_bets.append(Match(id=match_id, edgebet_id=edgebet_id, bookmaker_id=bookmaker_id, stake=stake))
					except Exception, e:
						print e
				else:
					print "no valid_outcome_object"
					pass

					

			else:
				pass
		else:
			try:
				home_team = bet['home_team']
			except:
				home_team = None
			try:
				away_team = bet['away_team']
			except:
				away_team = None
			try:
				edgebet_id = bet["edgebet_id"]
			except:
				edgebet_id = None

			





def is_bovada_bet(bookmaker):
	if bookmaker.lower()== "bovada":
		return True
	else:
		return False

def find_url_for_bet(bet):
	bet_sport = bet['sport'].lower()
	home_team = bet["home_team"]
	away_team = bet["away_team"]
	if bet_sport.__contains__("soccer"):
		bmatches = bovada_matches['soccer_matches']

	elif bet_sport.__contains__("baseball"):
		bmatches = bovada_matches["baseball_matches"]

	elif bet_sport.__contains__("football"):
		bmatches= bovada_matches['football_matches']

	elif bet_sport.__contains__("basketball"):
		bmatches = bovada_matches['basketball_matches']

	elif bet_sport.__contains__("rugby"):
		bmatches = bovada_matches['rugby_matches']

	elif bet_sport.__contains__("tennis"):
		bmatches = bovada_matches['tennis_matches']


	else:
		return None
	
	for bmatch in bmatches:
		try:
			if bmatch.home_team_full_name in home_team:
				return bmatch.game_link

			if bmatch.away_team_full_name in away_team or away_team in bmatch.away_team_full_name:
				return bmatch.game_link

			if bmatch.home_team_short_name in home_team or home_team in bmatch.home_team_short_name:
				return bmatch.game_link

			if bmatch.away_team_short_name in away_team or away_team in bmatch.away_team_short_name:
				return bmatch.game_link

			if bmatch.home_team_abbreviation in home_team or home_team in bmatch.home_team_abbreviation:
				return bmatch.game_link

			if bmatch.away_team_abbreviation in away_team or away_team in bmatch.away_team_abbreviation:
				return bmatch.game_link


			if home_team in bmatch.game_link or away_team in bmatch.game_link:
				return bmatch.game_link
			else:
				pass
		except Exception, e:
			pass

				

		

	


	


#check if the bet is a bovada bet
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
		spread_line = None
		spread_value = None
		total_line = None
		total_value = None
		odds_type = get_odds_type(offer['odds_type'])
		bookmaker = search_dictionary("bookmaker", offer)['name']
		bookmaker_id = int(search_dictionary("bookmaker", offer)["id"])
		time = search_dictionary("time", offer)
		match_id = search_dictionary("match", offer)["id"]
		


		if output == 1:
			put_on = "Home"
			spread_line  = "Over"
			total_line = "Home"
			spread_value = float(new_edge["o2"]["o3"])
			total_value = float(new_edge["o2"]['o3'])
			odds = float(new_edge['o2']['o1'])
			away_team = search_dictionary("hteam", offer)['name']
			home_team = search_dictionary("ateam", offer)['name']
			sport = search_dictionary("sport", offer)['name']
			start_time = search_dictionary("start_time", offer)
			edgebet_id = search_dictionary("id", offer)
		elif output == 2:
			put_on = "Draw"
			spread_line = "Under"
			total_line = "Away"
			spread_value = float(new_edge["o2"]["o3"])
			total_value = float(new_edge["o2"]["o3"])
			odds = float(new_edge['o2']['o2'])
			away_team = search_dictionary("hteam", offer)['name']
			home_team = search_dictionary("ateam", offer)['name']
			sport = search_dictionary("sport", offer)['name']
			start_time = search_dictionary("start_time", offer)
			edgebet_id = search_dictionary("id", offer)
		elif output == 3:
			away_team = search_dictionary("hteam", offer)['name']
			home_team = search_dictionary("ateam", offer)['name']
			put_on = "Away"
			odds = float(new_edge['o2']['o3'])
			sport = search_dictionary("sport", offer)['name']
			start_time = search_dictionary("start_time", offer)
			edgebet_id = search_dictionary("id", offer)



		if is_bovada_bet(bookmaker):
			bovada_bets.append(
			{"home_team": home_team, 
			"away_team": away_team, 
			"odds": odds,
			"bookmaker_id": bookmaker_id,
			"match_id": match_id,
			"time": time,
			"start_time": start_time,
			"spread_line": spread_line,
			"total_line": total_line,
			"spread value": spread_value,
			"total_value": total_value,
			"spread_value": spread_value,
			"odds_type": odds_type,
			'edge': edge,
			'put_on': put_on,
			'sport': sport,
			"edgebet_id": edgebet_id})
		elif testing == True:
			bovada_bets.append({"home_team": home_team, 
			"away_team": away_team, 
			"odds": odds,
			"bookmaker_id":bookmaker_id,
			"match_id": match_id,
			"spread_line": spread_line,
			"total_line": total_line,
			"total_value": total_value,
			"spread_value": spread_value,
			"odds_type": get_odds_type(odds_type),
			'edge': edge,
			'put_on': put_on,
			'sport': sport,
			"edgebet_id": edgebet_id})
	return bovada_bets

			
			
			
		

		


	


def get_odds_type(num):
	if num == 5:
		return "handicap"
	if num == 4:
		return "Total"

	elif num == 3:
		return "Point Spread"

	elif num == 1:
		return "Moneyline"

	elif num == 0:
		return "3-Way Moneyline" #threeway money line



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
	session = get_session()
	while True:
		if time.time() - checker > 2000 and len(placed_bets) > 0:
			print "adding all placed bets to db"
			session.add_all(placed_bets)
			session.commit()
			checker = time.time()

		time.sleep(1)
		log.log(logging.INFO, sys.stdout)

		

run()
