import tweepy
from bitly_api import Connection
bitly_auth_token = "6ee1cb452e51feec5c0f584cd78ee6762398adc8"
bitly = Connection(api_key=bitly_auth_token, access_token=bitly_auth_token)

api_objs = []
a, b, c, d = "HQDJz4CqmJGxhe6wikPxUFo7l", "rOeYaSGenfLx42o1VfTt5PkcMKfQJSx89riIMue1eGRIROcHa6", "258627515-MhwSWj0RXwMUD4PYT5xbCWkKzkc9V6SlmSyhjBiY", "yvlHSyo1CG22eFbAafrJUCHOMVergfKkJziwfrKtmZhjA"
auth = tweepy.OAuthHandler(a, b)
auth.set_access_token(c, d)
api = tweepy.API(auth)
api_objs.append(api)
a, b, c, d = "mVP71pUya8skr8rHgdcV7g6hi", "uL8hm2t6hi1HYsV32KVxJDERyqtAVbH3f7G0gPzrSzH1Losizs", "4875953380-fp7deRPXTtlTKsbrWbpYxeAbh9Sj2QZoAOuNx0K", "TWyghgmisSYLDw7tVDYPTptgtGwy6CyZcU9Gx0jSOs5zI"
auth = tweepy.OAuthHandler(a, b)
auth.set_access_token(c, d)
api = tweepy.API(auth)
api_objs.append(api)

def build_tweet(edgebet, stake):
		home_team = edgebet.home_team
		away_team = edgebet.away_team
		odds = edgebet.odds
		edge = edgebet.edge
		odds_type = edgebet.odds_type
		outcome_type = edgebet.outcome_type
		handicap = edgebet.handicap
		stake = "$" + stake
		match_url = bitly.shorten(edgebet.sibling.match_url)["url"]
		outcomeType = "Home" if outcome_type == "H" else "Away" if outcome_type == "A" else "Draw" if outcome_type == "D" else "Over" if outcome_type == "O" else "Under"
		oddsType = "Point Spread" if odds_type == 3 else "Total" if odds_type == 4 else "Moneyline" if odds_type == 0 else "3 Way Moneyline"
		if odds_type == 3:
			tweet_1 = "New #Edgebet: {}\n {} {} {}\n odds: {} \n odds should be: {} \n I placed {} ".format(match_url, outcomeType, oddsType, handicap, odds, odds/edge, stake)

		elif odds_type == 0:
			tweet_1 = "New #Edgebet: {}\n {} to Win \n odds: {} \n odds should be: {} \n I placed {}".format(match_url, outcomeType, odds, odds/edge, stake)

		elif odds_type == 1:
			tweet_1 = "New #Edgebet: {}\n {} to win \n odds: {} \n odds should be: {} \n I placed {}".format(match_url, outcomeType, odds, odds/edge, stake)

		elif odds_type == 4:
			tweet_1 = "New #Edgebet: {}\n {} {} \n odds: {} \n odds should be: {} \n I placed {}".format(match_url, outcomeType, handicap, odds, odds/edge, stake)

		return tweet_1


def tweet(message):
	for api in api_objs:
		try:
			api.update_status(message)
		except Exception, e:
			print e
		else:
			print "successfully updated status"