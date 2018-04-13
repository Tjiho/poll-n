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
    
    @property
    def username(self):
        return self.name

    def is_login(self):
        return False

    def __str__(self):
        return self.name
    
    def answer_checked(self,answer):
        return (answer in self.answer_set.all())

#question / poll
class Question(models.Model):
    title = models.CharField(max_length=500) #the question
    description = models.TextField()
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE) # if it was created by a connected user
    token = models.CharField(max_length = 50) 
    token_admin = models.CharField(max_length = 50) # token to edit option etc...
    
    annonymous_can_add_answer = models.BooleanField(default=False)
    annonymous_can_answer = models.BooleanField(default=False)

    connected_participant = models.ManyToManyField(User,blank=True,related_name="participateTo")
    anonym_participant = models.ManyToManyField(Anonym_user,blank=True,related_name="participateTo")
    

    @property
    def participant(self):
        l1 = self.anonym_participant.all()
        l2 = self.connected_participant.all()
        list_user = list(l1)+list(l2)
        return list_user

    #return list of user who check at least one answer 
    @property
    def real_participant(self):
        def f(ele):
            for answer in self.answer_set.all():
                if answer in ele.answer_set.all():
                    return True

            return False

        return list(filter(f,self.participant))

    

#answer
class Answer(models.Model):
    title = models.CharField(max_length=500)
    users = models.ManyToManyField(Anonym_user,null=True,blank=True)
    connected_users = models.ManyToManyField(User,null=True,blank=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)

    @property
    def percentage(self):
        nbr_check = len(self.users.all())+len(self.connected_users.all())
        nbr_tot = len(self.question.real_participant)
        if nbr_tot > 0:
            return (nbr_check/nbr_tot)*100
        else:
            return 0
    def check_for_user(self, user_pk,is_login):
        if is_login:
            user = User.objects.get(pk=user_pk)
            list_user = self.connected_users.all()
        else:
            user = Anonym_user.objects.get(pk=user_pk)
            list_user = self.users.all()
        
        return user in list_user

    def change_state_user(self,user_pk,is_login,new_state,force=False):
        old_state = self.check_for_user(user_pk,is_login)
        if old_state != new_state:
            if is_login:
                user = User.objects.get(pk=user_pk)
                list_user = self.connected_users
            elif self.question.annonymous_can_answer or force:
                user = Anonym_user.objects.get(pk=user_pk)
                list_user = self.users
            else:
                return False

            if new_state:
                list_user.add(user)
            else:
                list_user.remove(user)

            self.save()
        return old_state != new_state
        
                


            






