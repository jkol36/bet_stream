import sys
import websocket
import logging
from threading import Thread
import time
import json


def search_dictionary_for_certain_keys(key, dictionary):
        for k, value in dictionary.iteritems():
            if k == key or k.__contains__(key) or key.__contains__(k):
                return value
                
            else:
                if isinstance(value, dict):
                    item = search_dictionary_for_certain_keys(key, value)
                    if item is not None:
                        return item
    


class TrackGame(Thread):
    log = logging.getLogger()
    log.addHandler(logging.FileHandler("trackgame2.log"))

    def __init__(self, edgebet, log_level=logging.INFO, daemon=True, reconnect_interval=10):
        self.match_id = edgebet.sibling.match_id
        self.edgebet = edgebet
        self.current_score = edgebet.home_team + ":"+" " + str(0), edgebet.away_team+":"+ " " + str(0)
        self.reconnect_interval = reconnect_interval
        Thread.__init__(self)
        self.daemon = daemon



    def get_game_info(self, message):
        self.x = json.dumps(message.split("|")[1])
        self.message = json.loads(self.x)
        try:
            self.data = json.loads(json.loads(json.dumps(self.message)))
        except Exception, e:
            data = None
        finally:
            if self.data:
                #print data.keys()
                self.points_home = self.data["latestScore"]["home"]
                self.points_away = self.data["latestScore"]["visitor"]
                self.game_state = self.data["gameStatus"]
                self.current_score = self.edgebet.home_team + ":"+" " + str(self.points_home), self.edgebet.away_team+":"+ " " + str(self.points_away)
                return {"home": self.points_home, "away": self.points_away, "game_state": self.game_state}
                
                #elif data == "IN_PROGRESS":



    
    def track_point_spread_home_to_win(self, ws, message):
        print "tracking point spread home to win"
        self.starting_points = self.edgebet.handicap
        print "home team started with {}".format(self.starting_points)
        self.home_point_count = self.get_game_info(message)["home"]
        self.away_point_count = self.get_game_info(message)["away"]
        if (
            self.home_point_count + self.starting_points > self.away_point_count and
            self.get_game_info(message)["game_state"] == "IN_PROGRESS"
        ):
            print "you are currently winning this bet"
        elif (
            self.home_point_count + self.starting_points > self.away_point_count and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            print "you won this bet"
            self.edgebet.win = True
            self.edgebet.save()
            self.on_game_end(ws)

        elif (
            self.home_point_count + self.starting_points < self.away_point_count and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            print "you lost this bet"
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end(ws)

        else:
            print "You are currently losing this bet"
        

    def track_point_spread_away_to_win(self, ws, message):
        print "trackingpoint spread away to win"
        self.starting_points = self.edgebet.handicap
        print "away team started with {}".format(self.starting_points)
        self.home_point_count = self.get_game_info(message)["home"]
        self.away_point_count = self.get_game_info(message)["away"]
        if (
            self.away_point_count + self.starting_points > self.home_point_count and
            self.get_game_info(message)["game_state"] == "IN_PROGRESS"
        ):
            print "you are currently winning this bet"

        elif (
            self.away_point_count + self.starting_points > self.home_point_count and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            print "you won this bet"
            self.edgebet.win = True
            self.edgebet.save()
            self.on_game_end(ws)

        elif (
            self.away_point_count + self.starting_points < self.home_point_count and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            print "you lost this bet"
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end(ws)
        
        
        else:
            print "you are currently losing this bet"
            


    def track_moneyline_home_to_win(self, ws, message):
        print "tracking home to win straight up"
        self.home_point_count = self.get_game_info(message)["home"]
        self.away_point_count = self.get_game_info(message)["away"]
        if (
            self.home_point_count > self.away_point_count and
            self.get_game_info(message)["game_state"] == "IN_PROGRESS"
        ):
            print "you are currently winning this bet"
        elif (
            self.home_point_count > self.away_point_count and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            print "you won this bet"
            self.edgebet.win = True
            self.edgebet.save()
            self.on_game_end(ws)

        elif (
            self.home_point_count < self.away_point_count and
            self.get_game_info(message)["game_state"] == "IN_PROGRESS"
        ):
            print "you are currently losing this bet"


        elif (
            self.home_point_count < self.away_point_count and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            print "you lost this bet"
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end(ws)
           


    def track_moneyline_away_to_win(self, ws, message):
        print "tracking away to win straight up"
        self.home_point_count = self.get_game_info(message)["home"]
        self.away_point_count = self.get_game_info(message)["away"]
        if (
            self.home_point_count < self.away_point_count and
            self.get_game_info(message)["game_state"] == "IN_PROGRESS"
        ):
            print "you are currently winning this bet"
        elif (
            self.home_point_count < self.away_point_count and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            print "you won this bet"
            self.edgebet.win = True
            self.edgebet.save()
            self.on_game_end(ws)

        elif (
            self.home_point_count > self.away_point_count and
            self.get_game_info(message)["game_state"] == "IN_PROGRESS"
        ):
            print "you are currently losing this bet"


        elif (
            self.home_point_count > self.away_point_count and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            print "you lost this bet"
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end(ws)


    def track_total_points_over(self, ws, message):
        print "tracking total points over {}".format(self.edgebet.handicap)
        self.score_to_beat = self.edgebet.handicap
        print "need to beat {}".format(self.score_to_beat)
        self.current_score = self.get_game_info(message)["home"] + self.get_game_info(message)["away"]
        if self.current_score > self.score_to_beat:
            print "you won this bet. The score is home: {}, away: {}".format(self.get_game_info(message)["home"], self.get_game_info(message)["away"])
            if self.edgebet.win != True:
                self.edgebet.win = True
                self.edgebet.save()
                self.on_game_end(ws)
        elif self.get_game_info(message)["game_state"] == "IN_PROGRESS" and self.current_score < self.score_to_beat:
            print "you're currently losing this bet"

        elif self.get_game_info(message)["game_state"] == "GAME_END" and self.current_score < self.score_to_beat:
            print "you lost this bet"
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end(ws)

    def track_total_points_under(self, ws, message):
        self.score_to_beat = self.edgebet.handicap
        print "need to stay under {}".format(self.score_to_beat)
        self.current_score = self.get_game_info(message)["home"] + self.get_game_info(message)["away"]
        if self.current_score >= self.score_to_beat:
            print "you lost this bet. The score is home: {}, away: {}".format(self.get_game_info(message)["home"], self.get_game_info(message)["away"])
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end()
        elif self.get_game_info(message)["game_state"] == "IN_PROGRESS" and self.current_score < self.score_to_beat:
            print "you're currently winning this bet"

        elif self.get_game_info(message)["game_state"] == "IN_PROGRESS" and self.current_score >= self.score_to_beat:
            print "you're currently winning this bet"


        elif self.get_game_info(message)["game_state"] == "GAME_END" and self.current_score < self.score_to_beat:
            print "you won this bet"
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end(ws)

        elif self.get_game_info(message)["game_state"] == "GAME_END" and self.current_score == self.score_to_beat:
            print "you tied this bet"
            self.on_game_end(ws)

        elif self.get_game_info(message)["game_state"] == "GAME_END" and self.current_score >= self.score_to_beat:
            print "you lost this bet"
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end(ws)

    def track_moneyline_draw(self, ws, message):
        if (
            self.get_game_info(message)["home"] != self.get_game_info(message)["away"] and
            self.get_game_info(message)["game_state"] == "GAME_END"
        ):
            self.edgebet.win = False
            self.edgebet.save()
            self.on_game_end(ws) 

        elif (
            self.get_game_info(message)["home"] == self.get_game_info(message)["away"]
        ):
            self.edgebet.win = True
            self.edgebet.save()
            self.on_game_end(ws)






    def on_game_end(self, ws):
        print "game ended"
        ws.close()
        self.join()

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        print "### closed ###"

    def on_open(self, ws):
        log.log(logging.INFO, sys.stdout)


    def run(self):
        #websocket.enableTrace(True)
        
        if (
            self.edgebet.outcome_type == "O"
        ): 
            self.callback_function = self.track_total_points_over
        elif (
            self.edgebet.outcome_type == "U"
        ):
            self.callback_function = self.track_total_points_under
        elif (
            self.edgebet.outcome_type == "H" and self.edgebet.odds_type == 0 or
            self.edgebet.outcome_type == "H" and self.edgebet.odds_type == 1
        ):
            self.callback_function = self.track_moneyline_home_to_win

        elif (
            self.edgebet.outcome_type == "A" and self.edgebet.odds_type == 0 or
            self.edgebet.outcome_type == "A" and self.edgebet.odds_type == 1
        ):
            self.callback_function = self.track_moneyline_away_to_win

        elif (
            self.edgebet.outcome_type == "A" and self.edgebet.odds_type == 3
        ):
            self.callback_function = self.track_point_spread_away_to_win

        elif (
            self.edgebet.outcome_type == "H" and self.edgebet.odds_type == 3
        ):

            self.callback_function = self.track_point_spread_home_to_win

        elif (
            self.edgebet.outcome_type == "D"
        ):
            self.callback_function = self.track_moneyline_draw

        self.ws = websocket.WebSocketApp(
            "wss://sports.bovada.lv/services/sports/results/api/v1/scores/subscribe/atmosphere/{}?X-Atmosphere-tracking-id=0&X-Atmosphere-Framework=2.2.8-jquery&X-Atmosphere-Transport=websocket&X-Sports-Origin=L".format(self.match_id),
             on_message = self.callback_function,
             on_error = self.on_error,
             on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.on_game_end = self.on_game_end
        self.ws.run_forever()
       

        



   



