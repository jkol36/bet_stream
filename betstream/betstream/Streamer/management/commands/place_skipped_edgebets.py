from django.core.management.base import BaseCommand, CommandError
from betstream.Streamer.models import Edgebet, Bovadabet
from betstream.bovadaAPI.bovadaAPI.api import BovadaApi
from betstream.bovadaAPI.bovadaAPI.headers import get_bovada_headers_generic
from betstream.Streamer.kelly import Kelly
import json
from betstream.Streamer.bet_placer import PlaceBet
import time
import itertools
import random


class Command(BaseCommand):
	help = "Starts the streamer"

	def handle(self, *args, **kwargs):
		placed_bets = [x.outcome_id for x in Bovadabet.objects.filter(is_placed=True)] + [i.edgebet_id for i in Edgebet.objects.filter(is_placed=True)]
		
		for edgebet in Edgebet.objects.filter(is_placed=False).order_by("-recieved_date"):
			if (edgebet.edgebet_id in placed_bets):
				pass
			else:
				for bovadabet in Bovadabet.objects.filter(is_placed=False).order_by("-date_added"):
					if bovadabet.outcome_id in placed_bets:
						pass
					else:
						try:
						
							equal = edgebet == bovadabet
						except TypeError, e:
							pass
						else:
							if equal:
								print "found it"
								try:
									api = BovadaApi()
									cookies = api.auth["cookies"]
									headers = get_bovada_headers_generic()
									placebet = PlaceBet()
									odds = bovadabet.odds
									edge = edgebet.edge
									p = Kelly.get_p(odds) + (edge - 1)
									q = Kelly.get_q(p)
									b = Kelly.get_b(odds)
									percent_of_bank_roll = Kelly.get_percent_of_bank_roll(b, p, q)
									percent_of_bank_roll = percent_of_bank_roll * 100
									stake = "%.f" % (Kelly.get_stake(percent_of_bank_roll, api.balance))
									print "_________start____________________________"
									print "the odds are {}".format(odds)
									print "the probability of success with the edge is {}".format(p)
									print "the probability of failure with edge is {}".format(q)
									print "the edge is {}".format(edge)
									print "you should bet {} with the edge".format(percent_of_bank_roll)
									print "the best wager for you with edge is {}".format(stake)
									print "____________________________________"
									return
									data = placebet.build_bet_selection(outcomeId=bovadabet.outcome_id, priceId=bovadabet.price_id, stake=stake)
									if stake >= 1:
										cha_ching = placebet.place(data=json.dumps(data), cookies=cookies, headers=headers)
										if cha_ching:
											bovadabet.is_placed = True
											edgebet.is_placed = True
											bovadabet.stake = stake
											edgebet.stake = stake
											bovadabet.save()
											edgebet.save()
											placed_bets.append(bovadabet.outcome_id)
											placed_bets.append(edgebet.edgebet_id)
								except Exception, e:
									print e
								time.sleep(random.randint(0,20))
								break


			# for bovadabet in Bovadabet.objects.filter(is_placed=False):
			# 	if (
			# 		edgebet == bovadabet and
			# 		edgebet.edgebet_id not in placed_bets and
			# 		bovadabet.outcome_id not in placed_bets
			# 		):
			# 		try:
			# 			b = BovadaApi()
			# 			cookies = b.auth["cookies"]
			# 			headers = get_bovada_headers_generic()
			# 			p = PlaceBet()
			# 			try:
			# 				stake = Kelly.get_stake(odds=bovadabet.odds, edge=edgebet.edge, current_bank_roll=100)
			# 			except Exception, e:
			# 				print "something went wrong trying to get the stake amount ", e
			# 			data = p.build_bet_selection(outcomeId=bovadabet.outcome_id, priceId=bovadabet.price_id, stake=stake)
			# 			if stake >= 1:
			# 				cha_ching = p.place(data=json.dumps(data), cookies=cookies, headers=headers)
			# 				if cha_ching:
			# 					bovadabet.is_placed = True
			# 					edgebet.is_placed = True
			# 					bovadabet.stake = stake
			# 					edgebet.stake = stake
			# 					bovadabet.save()
			# 					edgebet.save()
			# 					placed_bets.append(bovadabet.outcome_id)
			# 					placed_bets.append(edgebet.edgebet_id)
			# 		except Exception, e:
			# 			print e


			# 		time.sleep(random.randint(0,50))
			# 	else:
			# 		pass

		