from betstream.bovadaAPI.bovadaAPI.api import BovadaApi

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