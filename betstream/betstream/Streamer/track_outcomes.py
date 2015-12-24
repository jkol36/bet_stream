import websocket
import thread
import time

def on_message(ws, message):
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "listening"
   


def track(event_id):
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp(
		"wss://sports-event-api.bovada.lv/api/atmosphere/eventNotification/events/A/{}?liveOnly=true&X-Atmosphere-tracking-id=0&X-Atmosphere-Framework=2.2.8-jquery&X-Atmosphere-Transport=websocket".format(event_id),
	     on_message = on_message,
	     on_error = on_error,
	     on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()





