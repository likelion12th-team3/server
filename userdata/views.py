from rest_framework import viewsets
from .models import User, Location, News
from .serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .news_crawling import news_crawling
from .woosan_crawling import woosan_crawling

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@csrf_exempt
def update_today_data(request):
    if request.method == "POST":
        categories, news_data = news_crawling()
        for category in categories:
            news = News()
            news.category = category
            news.title = news_data[category]["title"]
            news.content = news_data[category]["content"] 
            news.link = news_data[category]["link"] 
            news.save()

        locations, woosan_data = woosan_crawling()
        for location in locations:
            new_location = Location()
            new_location.gu_name = location
            new_location.woosan = woosan_data[location]["woosan"]
            new_location.temperature = woosan_data[location]["temperature"]
            new_location.save()

        return JsonResponse({"Success" : "News & Locations are updated"}, status=200)