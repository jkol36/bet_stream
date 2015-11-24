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
from bet_placer import PlaceBet
from validate_bet import validate_bet


testing = False

placed_bets = []

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
	bovada_bets = return_bovada_bets(data=data) #parse the data dictonary
	#if bovada_bets: # if any bovada bets are found (checking to see of the bookmaker key's value == "bovada")
	for bet in bovada_bets: # for each bovada bet
		print "got new bovada bet"
		#print "bet odds type: {}".format(bet["odds_type"])
		url = find_url_for_bet(bet)
		if url:
			edge = bet['edge']
			edgebet_id = bet['edgebet_id']
			print "edge {}".format(edge)
			if edge >= 1.0 and edgebet_id not in placed_bets:
				v = validate_bet(url, bet) #scrapes the url, parses the response, and returns a new bovadamatch object.
				print v
				if v:
					try:
						b = BovadaApi()
						cookies = b.auth["cookies"]
						headers = get_bovada_headers_generic()
						p = PlaceBet()
						stake = kelly.get_stake(edge=edge, current_bank_roll=b.current_bank_roll)
						print "stake {}".format(stake)
						data = p.build_bet_selection(outcomeId=v.outcome_id, priceId=outcome.price_id, stake=stake)
						print data
					except Exception, e:
						print e

					

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

			print "could not find url for bet {} vs {}, edgebet_id: {}".format(
				home_team if home_team else None, away_team if away_team else None,  edgebet_id if edgebet_id else None
				)





def is_bovada_bet(bookmaker):
	if bookmaker.lower()== "bovada":
		return True
	else:
		return False

def find_url_for_bet(bet):
	print "finding url for bet"
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
		print "cant parse sport"
		return None
	
	for bmatch in bmatches:
		try:
			if bmatch.home_team_full_name in home_team:
				print "bovada home team {}".format(bmatch.home_team_full_name)
				print "bovada away team {}".format(bmatch.away_team_full_name)
				print "edgbet home team {}".format(home_team)
				print "edgebet away_team {}".format(away_team)
				return bmatch.game_link

			if bmatch.away_team_full_name in away_team or away_team in bmatch.away_team_full_name:
				print "bovada home team {}".format(bmatch.home_team_full_name)
				print "bovada away team {}".format(bmatch.away_team_full_name)
				print "edgbet home team {}".format(home_team)
				print "edgebet away_team {}".format(away_team)
				return bmatch.game_link

			if bmatch.home_team_short_name in home_team or home_team in bmatch.home_team_short_name:
				print "bovada home team {}".format(bmatch.home_team_full_name)
				print "bovada away team {}".format(bmatch.away_team_full_name)
				print "edgbet home team {}".format(home_team)
				print "edgebet away_team {}".format(away_team)
				return bmatch.game_link

			if bmatch.away_team_short_name in away_team or away_team in bmatch.away_team_short_name:
				print "bovada home team {}".format(bmatch.home_team_full_name)
				print "bovada away team {}".format(bmatch.away_team_full_name)
				print "edgbet home team {}".format(home_team)
				print "edgebet away_team {}".format(away_team)
				return bmatch.game_link

			if bmatch.home_team_abbreviation in home_team or home_team in bmatch.home_team_abbreviation:
				print "bovada home team {}".format(bmatch.home_team_full_name)
				print "bovada away team {}".format(bmatch.away_team_full_name)
				print "edgbet home team {}".format(home_team)
				print "edgebet away_team {}".format(away_team)
				return bmatch.game_link

			if bmatch.away_team_abbreviation in away_team or away_team in bmatch.away_team_abbreviation:
				print "bovada home team {}".format(bmatch.home_team_full_name)
				print "bovada away team {}".format(bmatch.away_team_full_name)
				print "edgbet home team {}".format(home_team)
				print "edgebet away_team {}".format(away_team)
				return bmatch.game_link


			if home_team in bmatch.game_link or away_team in bmatch.game_link:
				print "bovada home team {}".format(bmatch.home_team_full_name)
				print "bovada away team {}".format(bmatch.away_team_full_name)
				print "edgbet home team {}".format(home_team)
				print "edgebet away_team {}".format(away_team)
				return bmatch.game_link
			else:
				pass
		except Exception, e:
			print e
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
		
		
		


		if output == 1:
			put_on = "Home"
			spread_line  = "Over"
			total_line = "Home"
			spread_value = float(new_edge["o2"]["o3"])
			print "getting spread value"
			print spread_value
			total_value = float(new_edge["o2"]['o3'])
			odds = float(new_edge['o2']['o1'])
			away_team = search_dictionary("hteam", offer)['name']
			home_team = search_dictionary("ateam", offer)['name']
			sport = search_dictionary("sport", offer)['name']
			start_time = search_dictionary("start_time", offer)
			edgebet_id = search_dictionary("id", offer)
			#print offer
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
			#print offer
		elif output == 3:
			away_team = search_dictionary("hteam", offer)['name']
			home_team = search_dictionary("ateam", offer)['name']
			put_on = "Away"
			odds = float(new_edge['o2']['o3'])
			sport = search_dictionary("sport", offer)['name']
			start_time = search_dictionary("start_time", offer)
			edgebet_id = search_dictionary("id", offer)



		if is_bovada_bet(bookmaker):
			print "got new bovada bet"
			print "odds_type {}".format(odds_type)
			print "spread_line {}".format(spread_line)
			print "home_team {}".format(home_team)
			print "away_team {}".format(away_team)
			bovada_bets.append(
			{"home_team": home_team, 
			"away_team": away_team, 
			"odds": odds,
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
	bovada_matches = get_bovada_matches()
	root = logging.getLogger()
	root.setLevel(logging.INFO)
	ch = logging.StreamHandler(sys.stdout)
	root.addHandler(ch)
	global pusher #make pusher a global variable so it's accessible throughout the script
	appkey = "c11ef000e51c34bac2fc"
	pusher = pusherclient.Pusher(appkey)
	pusher.connection.bind('pusher:connection_established', connection_handler)
	pusher.connect()
	while True:
		time.sleep(1)

		

run()
