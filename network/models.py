from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='maker')
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('User', blank=True)
    edited = models.BooleanField(default=False)

class Userprofile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='profile')
    follower = models.ManyToManyField('User', blank=True, related_name='follower')
    following = models.ManyToManyField('User', blank=True, related_name='following')
