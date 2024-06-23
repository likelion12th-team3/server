from django.contrib import admin
from .models import News, Location, User

# Register your models here.
admin.site.register(News)
admin.site.register(Location)
admin.site.register(User)