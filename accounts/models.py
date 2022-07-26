from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cover = models.ImageField(null=True, blank=True, default='profile.png', upload_to='profile/')
    bio = models.TextField()
    follower = models.ManyToManyField(User, related_name='follower', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    request = models.ManyToManyField(User, related_name='request', blank=True)
    
    def __str__(self):
        return self.user.username

