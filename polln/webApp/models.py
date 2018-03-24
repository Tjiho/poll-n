from django.db import models
from django.contrib.auth.models import User

#user

#questions

class Question(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    username = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    token = models.CharField(max_length = 50)
    token_admin = models.CharField(max_length = 50)

#non connected user
class Anonym_user(models.Model):
    name = models.CharField(max_length=100)

#answer
class Answer(models.Model):
    title = models.CharField(max_length=500)
    users = models.ManyToManyField(Anonym_user,null=True,blank=True)




