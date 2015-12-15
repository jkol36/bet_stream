from django.contrib import admin
from models import Bovadabet, Edgebet




class BovadabetAdmin(admin.ModelAdmin):
	list_display = [
		"home_team",
		"away_team",
		"sport",
		"odds_type",
		"odds", 
		"handicap",
		"outcome_type",
		"match_id",
		"outcome_id",
		"price_id"
	]

class EdgebetAdmin(admin.ModelAdmin):

	list_display = [
		"home_team",
		"away_team",
		"sport",
		"odds_type",
		"odds", 
		"handicap",
		"outcome_type",
		"edgebet_id",
		"edge",
	]
		
	

admin.site.register(Bovadabet, BovadabetAdmin)
admin.site.register(Edgebet, EdgebetAdmin)