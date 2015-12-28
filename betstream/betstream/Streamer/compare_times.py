from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO






#returns the time differencce between a old datetime obj and timezone.now()
def time_difference(event):
	return event - timezone.now()



def seconds_until_event(event):
	print "getting seconds until event"
	utc = UTC()
	if isinstance(event, datetime):
		print "got a datetime instance not a string"
		time_until_event = event - datetime.now(utc)
		return time_until_event.total_seconds()
	#parse out the day
	event_year = event[:4]
	event_month = event[5:7]
	event_day = event[8:10]
	event_hour = event[11:13]
	event_min = event[14:16]
	event = datetime(
		year = int(event_year),
		month = int(event_month),
		day = int(event_day),
		hour = int(event_hour),
		minute = int(event_min),
		tzinfo=utc
	)
	time_until_event = event - datetime.now(utc)

	return time_until_event.total_seconds()





