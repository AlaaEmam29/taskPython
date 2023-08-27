from django.db import models
from datetime import datetime, timedelta

class User(models.Model):
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=100)
    registration_time = models.DateTimeField(auto_now_add=True)

class Singer(models.Model):
    name = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)
    voting_window_start = models.DateTimeField(default=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    voting_window_end = models.DateTimeField(default=datetime.now() + timedelta(days=7))

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)
    vote_time = models.DateTimeField(auto_now_add=True)
