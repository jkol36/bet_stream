




class Kelly(object):

	@classmethod
	def get_stake(cls, odds, edge, current_bank_roll):
		win_rate = Kelly.get_win_rate(odds, edge)
		percent_of_bank_role = (win_rate * (odds +1) -1) / odds
		return current_bank_roll * percent_of_bank_role


	@classmethod
	def get_win_rate(cls, odds, edge):
		return (1 / (odds /( 1 + edge/100)))





