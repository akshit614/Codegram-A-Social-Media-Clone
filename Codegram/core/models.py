from email.policy import default
from pickle import TRUE
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class ProFil(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to = 'profile_images' , default='abcd.jpg')
    location = models.CharField(max_length=100, blank=True)


    def __str__(self) :
        return self.user.username



class Poost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images' , default='abcd.jpg')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)


    def __str__(self) :
        return self.user
