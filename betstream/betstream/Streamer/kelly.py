




class Kelly(object):

	@classmethod
	def get_percent_of_bank_roll(cls, b, p, q):
		#b = The decimal odds - 1
		#p probability of success
		#Q = Probability of failure
		return (b*p-q)/b

	@classmethod
	def get_stake(cls, percent_of_bankroll, current_bank_roll):
		return percent_of_bankroll * current_bank_roll

	@classmethod
	def get_p(cls, odds):
		return 1/odds

	@classmethod
	def get_q(cls, p):
		return 1 - p

	@classmethod
	def get_b(cls, odds):
		return odds - 1








