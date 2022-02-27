from django.db import models

# Create your models here.
class Subreddit(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    subs = models.IntegerField()
