from django.contrib import admin
from .models import Profile, BovadaProfile



class ProfileAdmin(admin.ModelAdmin):
	list_display = ("username", "email")

class BovadaProfileAdmin(admin.ModelAdmin):
	list_display = ("bovada_username", "bovada_password")





admin.site.register(Profile, ProfileAdmin)
admin.site.register(BovadaProfile, BovadaProfileAdmin)






