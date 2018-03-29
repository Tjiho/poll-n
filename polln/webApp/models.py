from django.db import models
from django.contrib.auth.models import AbstractUser

#user
class User(AbstractUser):
    def is_login(self):
        return True

    def __str__(self):
        return self.username

    def answer_checked(self,answer):
        return (answer in self.answer_set.all())

#non connected user
class Anonym_user(models.Model):
    name = models.CharField(max_length=100)
    
    def is_login(self):
        return False

    def __str__(self):
        return self.name
    
    def answer_checked(self,answer):
        return (answer in self.answer_set.all())

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

#answer
class Answer(models.Model):
    title = models.CharField(max_length=500)
    users = models.ManyToManyField(Anonym_user,null=True,blank=True)
    connected_users = models.ManyToManyField(User,null=True,blank=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    
    def check_for_user(self, user_pk,is_login):
        if is_login:
            user = User.objects.get(pk=user_pk)
            list_user = self.connected_users.all()
        else:
            user = Anonym_user.objects.get(pk=user_pk)
            list_user = self.users.all()
        
        return user in list_user

    def change_state_user(self,user_pk,is_login,new_state):
        old_state = self.check_for_user(user_pk,is_login)
        if old_state != new_state:
            if is_login:
                user = User.objects.get(pk=user_pk)
                list_user = self.connected_users
            else:
                user = Anonym_user.objects.get(pk=user_pk)
                list_user = self.users

            if new_state:
                list_user.add(user)
            else:
                list_user.remove(user)

            self.save()
        return old_state != new_state
        
                


            






