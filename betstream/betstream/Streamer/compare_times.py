from django.utils import timezone






#returns the time differencce between a old datetime obj and timezone.now()
def time_difference(event):
	return event - timezone.now()



def hours_until_event(event):
	time_until_event = event - timezone.now()
	return str(time_until_event)[:2].split(":")[0]



