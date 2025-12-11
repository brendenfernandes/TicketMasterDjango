from django.db import models

class Favorite(models.Model):
    event_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    image = models.URLField()
    url = models.URLField()
    venue = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    day = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=20)
    note = models.TextField(blank=True)
