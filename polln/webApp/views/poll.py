from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from webApp.forms import PseudoForm
from webApp.models import Question,Anonym_user,Option,Answer,User
from django.http import HttpResponseRedirect
import binascii
import os

class Poll(View):
    html = 'webApp/poll.html'
    html_login = 'webApp/getPseudo.html'

    """
        Renvoie la page d'Inscription au chargement de la page
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.getOrCreateForm(request,request.user,kwargs.get("key"),request.user)
        elif "user_anonym" in request.session:
            user = Anonym_user.objects.get(pk=request.session["user_anonym"])
            return self.getOrCreateForm(request,user,kwargs.get("key"))
        else:
            form = PseudoForm()
            if("key" in kwargs):
                urlPost = "/poll/"+kwargs["key"]+"/"
            else:
                urlPost = "/poll/"
            return render(request, self.html_login, locals())

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.getOrCreateForm(request,request.user,kwargs.get("key"),request.user)
        elif "user_anonym" in request.session:
            user = Anonym_user.objects.get(pk=request.session["user_anonym"])
            return self.getOrCreateForm(request,user,kwargs.get("key"))
        else:
            form = PseudoForm(request.POST)

            if form.is_valid():
                anonym = Anonym_user.objects.create(
                    name = form.cleaned_data["name"]
                )
                request.session["user_anonym"] = anonym.pk
                return self.getOrCreateForm(request,anonym,kwargs.get("key"))
            else:
                return render(request, self.html_login, locals())

    def getOrCreateForm(self,request,user,token,login_user=None,):
        
        #q_user = Question.objects.get(token=token)
        #q_admin = Question.objects.get(token_admin=token)
        
        if token:
            if Question.objects.filter(token=token).exists():
                admin = False
                question = Question.objects.get(token=token)
            elif Question.objects.filter(token_admin=token).exists():
                admin = True
                question = Question.objects.get(token_admin=token)
            else:
                return HttpResponseRedirect("/404/")
        else:
            token_user = self.generate_key()
            token_admin = self.generate_key()
            admin = True
            question = Question.objects.create(
                title = "enter a question",
                description = "enter a description",
                token = token_user,
                token_admin = token_admin,
                user = login_user
            )
            
            return HttpResponseRedirect("/poll/"+token_admin)
        
        
        
        list_options = Option.objects.all()
        list_answer = Answer.objects.filter(question=question)
        list_answer_checked = list(map(user.answer_checked,list_answer))
        list_answer_zip = zip(list_answer,list_answer_checked)
        print(list_answer_checked)
        return render(request, self.html, locals())

        
            
            

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()