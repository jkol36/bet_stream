from django.contrib import admin
from models import ApiKey, Profile




class ApiKeyAdmin(admin.ModelAdmin):
	list_display = [

		"created",
		"value",
		"is_valid"
	]

class ProfileAdmin(admin.ModelAdmin):

	list_display = [
		"API_KEY"
	]


	

admin.site.register(ApiKey, ApiKeyAdmin)
admin.site.register(Profile, ProfileAdmin)
