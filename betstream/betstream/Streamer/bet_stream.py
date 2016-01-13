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
import logging
import itertools
from django.conf import settings
from get_bovada_matches import get_bovada_matches
from betstream.bovadaAPI.bovadaAPI.api import BovadaApi
from betstream.bovadaAPI.bovadaAPI.headers import get_bovada_headers_generic
from betstream.Streamer.compare_times import seconds_until_event
from track_game import TrackGame
from bet_placer import PlaceBet
from models import Bovadabet, Edgebet
from kelly import Kelly




class BetStream(object):
	
	def __init__(self, min_edge=1.01, place_bet=True):
		self.key = "c11ef000e51c34bac2fc"
		self.min_edge = min_edge
		self.place_bet = place_bet
		
	

	def connection_handler(self, data):
		print "connected to edgebet"
		channel = self.pusher.subscribe("edgebets")
		channel.bind("edge_changes", self.on_edge)

	



	def save_matches(self):
		already_added_outcome_ids = [x.outcome_id for x in Bovadabet.objects.all()]
		self.bovada_bets = []
		for match in itertools.chain(
			self.bovada_matches["basketball_matches"],
			self.bovada_matches["baseball_matches"],
			self.bovada_matches["soccer_matches"],
			self.bovada_matches["tennis_matches"],
			self.bovada_matches["rugby_matches"],
			self.bovada_matches["football_matches"]
			):

			for bovadabet in Bovadabet.create(match, already_added_outcome_ids):
				pass
			
		
		return True

	def remove_stale_matches(self):
		print "removing stale matches"
		for match in Bovadabet.objects.filter(is_placed=False):
			match.delete()
		return True
	def on_edge(self, data):
		self.edgebets = json.loads(data)
		self.new_edgebets = [edgebet for edgebet in self.edgebets["new_edges"]]
		for edgebet in self.new_edgebets:
			self.placed_edgebet = False
			#check the bookmaker see if the bookmaker is equal to bovada
			#if the bookmaker is equal to bovada,
			#call self_and_create() passing in the raw
			#json object which (should) return a new edgebet obj
			#that is now saved in the database
			#if we don't get back a edgebet obj instance (either because an)
			#error is raised or because the bookmaker name isn't == bovada
			#we pass and check the next bet
			#otherwise, I attempt to find the bovada bet that should match
			#our edgebet object exactly. If we find it, 
			#we place the bet. Otherwise, we pass and move onto the next bet,
			#finally if the place bet is successful, we log it, 
			#which essentially means that we change the is_placed attribute on the edgebet
			#and bovadabet to True
			try:
				self.bookmaker = edgebet["o2"]["offer"]["bookmaker"]["name"].lower()
			except (KeyError):
				print "can't find bookmaker attribute"
				self.bookmaker = None

			try:
				self.edge = edgebet["edge"]
			except (KeyError):
				print "can't find the edge attribute"
				self.edge = None

			finally:
				if (
					not self.bookmaker or 
					not self.edge
					):
					pass
				elif (
					self.bookmaker.lower() == "bovada" and
					self.edge >= self.min_edge
					):
					self.edgebet_obj = Edgebet.create(edgebet)
				else:
					self.edgebet_obj = None
			
			if self.edgebet_obj is not None:
				self.bovada_bet_for_edgebet = self.find_bovada_bet_for(self.edgebet_obj)
				if (
					self.bovada_bet_for_edgebet is not None
				):
					self.edgebet = self.bovada_bet_for_edgebet[1]
					self.bovadabet = self.bovada_bet_for_edgebet[0]
					
					self.place_the_bet = self.place_bet_on_bovada(
						bovada_bet=self.bovadabet,
						edgebet=self.edgebet
					)
					if self.place_the_bet:
						print "successfully placed {} vs {} outcome_type {}, odds_type {}".format(
							self.edgebet_obj.home_team, 
							self.edgebet_obj.away_team, 
							self.edgebet_obj.outcome_type,
							self.edgebet_obj.odds_type
						)

				else:
					print "I could not find a bovada bet for this edgebet object", self.edgebet_obj.edgebet_id
					print self.bovada_bet_for_edgebet
				

			



	def find_bovada_bet_for(self, edgebet):
		available_sports = settings.SPORTS_TO_BET_ON
		if sport not in available_sports:
			print "skipping this bet based on sport"
			return None
		as
		home_team = " ".join(edgebet.home_team.split(",")).lower()
		away_team = " ".join(edgebet.away_team.split(",")).lower()
		for bet in Bovadabet.objects.filter(is_placed=False, home_team__icontains=edgebet.home_team, away_team__icontains=edgebet.away_team).order_by("-date_added"):
			try:
				equal = bet == edgebet
			except Exception, e:
				print e
				equal = False
			finally:
				if equal == True:
					return [bet, edgebet]
					
				

	
		print "could not find outcome"
		return None
			


	


	def place_bet_on_bovada(self, bovada_bet, edgebet):
		self.placed_bets = [x.outcome_id for x in Bovadabet.objects.filter(is_placed=True)] + [i.edgebet_id for i in Edgebet.objects.filter(is_placed=True)]
		if self.place_bet == False:
			return False

		if (
			bovada_bet.outcome_id in self.placed_bets or
			edgebet.edgebet_id in self.placed_bets
		):
			print "already placed this bet"
			return False
		
		elif (
			edgebet.start_time == None
		):
			print "don't know when this game starts"
			return False
		
		elif (
			int(seconds_until_event(edgebet.start_time)) > 0 and
			int(seconds_until_event(edgebet.start_time)) > 10800
		):
			print "this game isn't for another {} seconds".format(seconds_until_event(edgebet.start_time))
			return False


		api = BovadaApi()
		cookies = api.auth["cookies"]
		headers = get_bovada_headers_generic()
		placebet = PlaceBet()
		p = Kelly.get_p(odds=bovada_bet.odds) + (edgebet.edge - 1)
		q = Kelly.get_q(p)
		b = Kelly.get_b(odds=bovada_bet.odds)
		percent_of_bankroll_to_bet = Kelly.get_percent_of_bank_roll(
			b,
			p,
			q
		)
		print "probability of you winning {}".format(p)
		print "probability of you losing {}".format(q)
		print "percent_of_bankroll_to_bet {}".format(percent_of_bankroll_to_bet)
		stake = "%.f" %(Kelly.get_stake(percent_of_bankroll_to_bet, api.balance) * 100)
		print "stake {}".format(stake)
		data = placebet.build_bet_selection(outcomeId=bovada_bet.outcome_id, priceId=bovada_bet.price_id, stake=stake)
		if stake >= 1 and data:
			cha_ching = placebet.place(data=json.dumps(data), cookies=cookies, headers=headers)
			if cha_ching:
				bovada_bet.is_placed = True
				edgebet.is_placed = True
				bovada_bet.stake = stake
				edgebet.stake = stake
				edgebet.sibling = bovada_bet
				bovada_bet.save()
				edgebet.save()
				self.placed_bets.append(bovada_bet.outcome_id)
				self.placed_bets.append(edgebet.edgebet_id)
				return True
			return False
		else:
			print "stake to low"
			return False

	def run(self):
		""" setup our logging and bind our pusher client to
		our on_edge function. Also fetch the bovada matches. Then create a new
		special object based on it's properties. """
		self.pusher = pusherclient.Pusher(self.key)
		self.log = logging.getLogger()
		self.log.addHandler(logging.FileHandler("betstream.log"))
		self.pusher.connection.bind('pusher:connection_established', self.connection_handler)
		self.remove_stale_matches()
		#fetches bovada matches from bovada
		self.bovada_matches = get_bovada_matches()
		self.save_matches()
		self.pusher.connect()
		self.checker = time.time()
		
		while True:
			if time.time() - self.checker >= 1000:
				self.pusher.disconnect()
				print "disconnected"
				break
			
			self.log.log(logging.INFO, sys.stdout)
			time.sleep(01)







