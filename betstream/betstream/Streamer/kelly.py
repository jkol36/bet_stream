




class Kelly(object):

	@classmethod
	def get_stake(cls, odds, edge, current_bank_roll):
		win_rate = Kelly.get_win_rate(odds, edge)
		odds = odds - 1
		percent_of_bank_roll = (((odds*win_rate - (1 - win_rate))/ odds))
		return "%.f" %(current_bank_roll * percent_of_bank_roll * 1.5 * 100)

	@classmethod
	def get_win_rate(cls, odds, edge):
		edge = edge/100
		return 1 / (odds / (1 + edge))





