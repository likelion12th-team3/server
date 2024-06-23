from django.db import models

# Create your models here.

class News(models.Model):
    category = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField(max_length=100)

    def __str__(self):
        return self.category
    
class Location(models.Model):
    gu_name = models.CharField(max_length=20, primary_key=True)
    woosan = models.BooleanField()
    temperature = models.FloatField()

    def __str__(self):
        return self.gu_name

class User(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categoryuser')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news')

    def __str__(self):
        return f"{self.user} - {self.news}"

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locationuser')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')

    def __str__(self):
        return f"{self.user} - {self.location}"
