from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_user")
    age = models.IntegerField(blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pic', default='profile_pic/default_pic.jpg', max_length=1000)


    def __str__(self):
        return self.user.username
    
    
class Friend(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="user_name")
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friend")
    
    
    def __str__(self):
        return f"{self.friend.user.username} friend of {self.user.user.username}"
    
    
class Request(models.Model):
    request_from = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="request_from")
    request_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="request_to")
    
    
    def __str__(self):
        return f"{self.request_from.user.username} requested to {self.request_to.user.username}"
    
    
class Message(models.Model):
    body = models.TextField()
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.body