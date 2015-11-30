



class Match(object):
	def __init__(
		self, 
		id,
		edgebet_id,
		stake,
		bookmaker_id,
		):
		self.id = id
		self.edgebet_id = edgebet_id
		self.stake = stake
		self.bookmaker_id = bookmaker_id
		return super(Match, self).__init__()
