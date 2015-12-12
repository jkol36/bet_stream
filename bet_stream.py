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
from get_bovada_matches import get_bovada_matches
from bovadaAPI.bovadaAPI.api import BovadaApi
from bovadaAPI.bovadaAPI.headers import get_bovada_headers_generic
from bet_placer import PlaceBet
from bet_stream_models import Bovadabet, Edgebet
from kelly import Kelly







class BetStream(object):
	def __init__(self, min_edge=1.0, place_bet=True):
		self.key = "c11ef000e51c34bac2fc"
		self.min_edge = min_edge
		self.place_bet = place_bet
		self.pusher = pusherclient.Pusher(self.key)
		return super(BetStream, self).__init__()
	
	



	def __enter__(self, *args, **kwargs):
		""" setup our logging and bind our pusher client to
		our on_edge function. Also fetch the bovada matches. Then create a new
		special object based on it's properties. Finally return our class instance """
		self.log = logging.getLogger()
		self.log.addHandler(logging.FileHandler("betstream.log"))
		self.pusher.connection.bind('pusher:connection_established', self.connection_handler)
		self.bovada_matches = get_bovada_matches()
		self.bovadabets = []
		self.placed_bets = []
		for match in itertools.chain(
			self.bovada_matches["basketball_matches"],
			self.bovada_matches["baseball_matches"],
			self.bovada_matches["soccer_matches"],
			self.bovada_matches["tennis_matches"],
			self.bovada_matches["rugby_matches"],
			self.bovada_matches["football_matches"]
			):
			for bovadabet in Bovadabet.create(match):
				self.bovadabets.append(bovadabet)
		print "there are {} possible bovadabets to bet on.".format(len(self.bovadabets))
		self.checker = time.time()
		self.pusher.connect() 
		return self

	def __exit__(self, *args, **kwargs):
		"""this is where we'll save the bets we've made to a database if the script stops suddenly"""
		return True

	def connection_handler(self, data):
		print "connected to edgebet"
		channel = self.pusher.subscribe("edgebets")
		channel.bind("edge_changes", self.on_edge)

	def on_edge(self, data):
		self.edgebets = json.loads(data)
		self.new_edgebets = [edgebet for edgebet in self.edgebets["new_edges"]]
		for edgebet in self.new_edgebets:
			valid_bet = self.is_valid(edgebet)
			if valid_bet:
				try:
					self.edge = float(edgebet["edge"])
				except TypeError:
					print "cant convert edge to float"

				try:
					b = BovadaApi()
					cookies = b.auth["cookies"]
					headers = get_bovada_headers_generic()
					p = PlaceBet()
					try:
						stake = Kelly.get_stake(odds=valid_bet.odds, edge=self.edge, current_bank_roll=b.balance)
					except Exception, e:
						print "something went wrong trying to get the stake amount ", e
					data = p.build_bet_selection(outcomeId=valid_bet.outcome_id, priceId=valid_bet.price_id, stake=stake)
					if stake >= 1:
						cha_ching = p.place(data=json.dumps(data), cookies=cookies, headers=headers)
						if cha_ching:
							self.placed_bets.append(valid_bet.outcome_id)
				except Exception, e:
					print e



	
	def is_valid(self, edgebet):
		"""this is valid function checks to see if the edgebet's bookmaker attribute
			attribute is equal to bovada. If it is, then it checks the sport attribute to
			see if the sport is us football (the only sport type we get back that isn't one word)
			for some reason. After all of that logic, 
			we instantiate a new Edgebet object and compare it against all our outcome objects
			and return on a successful match.
		"""

		if edgebet["o2"]["offer"]["bookmaker"]["name"].lower() != "bovada":
			return False
		elif edgebet["edge"] < self.min_edge:
			return False

		else:
			#create our edgebet object and compare it with each any every possible outcome
			try:
				edgebet = Edgebet.create(edgebet)
			except Exception, e:
				print e

			print edgebet.odds_type
			print edgebet.odds
			print edgebet.away_team
			print edgebet.home_team
			print edgebet.sport
			print edgebet.outcome_type
			print edgebet.handicap
			for bovadabet in self.bovadabets:
				if (edgebet == bovadabet and
					bovadabet.outcome_id not in self.placed_bets
					):
					print "found it"
					if self.place_bet == False:
						return False
					return bovadabet
				else:
					pass
			print "could not find outcome"


				


	def run(self):
		while True:
			if time.time() - self.checker >= 1000:
				self.bovada_matches = get_bovada_matches()
				self.checker = time.time()
			self.log.log(logging.INFO, sys.stdout)




s = BetStream(place_bet=True)
with s:
	print s.run()



