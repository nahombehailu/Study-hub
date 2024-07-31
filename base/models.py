from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
   
    name=models.CharField(max_length=200 ,null=True)
    email=models.EmailField( unique=True, null=True)
    bio=models.TextField(null=True,blank=True)
    
    avatar=models.ImageField( null=True,default='avatar.svg')
   
    REQUIRED_FIELDS=[]
    USERNAME_FIELD='email'


class Topic(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    name=models.CharField(max_length=200)
    descriptions=models.TextField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-updated','-created']
    
    def __str__(self):
        return self.name
    
    
    
class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.body[0:50]  