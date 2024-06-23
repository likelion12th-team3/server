from django.contrib import admin
from .models import News, Location, User,UserCategory,UserLocation

# Register your models here.
admin.site.register(News)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(UserLocation)
admin.site.register(UserCategory)