from django.db import models
from django.contrib.auth.models import User

#user

#poll options
class Option(models.Model):
    name = models.CharField(max_length=100)

#question / poll
class Question(models.Model):
    title = models.CharField(max_length=500) #the question
    description = models.TextField()
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE) # if it was created by a connected user
    token = models.CharField(max_length = 50) 
    token_admin = models.CharField(max_length = 50) # token to edit option etc...
    options = models.ManyToManyField(Option,blank=True) # if link to option then option is "on" else option is off

#non connected user
class Anonym_user(models.Model):
    name = models.CharField(max_length=100)

#answer
class Answer(models.Model):
    title = models.CharField(max_length=500)
    users = models.ManyToManyField(Anonym_user,null=True,blank=True)
    connected_users = models.ManyToManyField(User,null=True,blank=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)






