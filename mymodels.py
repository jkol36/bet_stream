from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float
Base = declarative_base()



class Match(Base):
	__tablename__ = "matches"
	id = Column(Integer, primary_key=True)
	edgebet_id = Column(Integer, primary_key=False)
	stake = Column(Float)
	bookmaker_id = Column(Integer, primary_key=False)
	def __unicode__(self):
		return "match_id: %d, edgebet_id: %d, bookmaker_id: %d, stake: %f" %(self.id, self.edgebet_id, self.bookmaker_id, self.stake)


 


