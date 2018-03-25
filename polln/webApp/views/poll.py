from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from webApp.forms import PseudoForm
from webApp.models import Question,Anonym_user,Option,Answer
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
            return self.getOrCreateForm(request,request.user.username,kwargs.get("key"),request.user)
        elif "user_anonym" in request.session:
            return self.getOrCreateForm(request,request.session["user_anonym"],kwargs.get("key"))
        else:
            form = PseudoForm()
            if("key" in kwargs):
                urlPost = "/poll/"+kwargs["key"]+"/"
            else:
                urlPost = "/poll/"
            return render(request, self.html_login, locals())

    def post(self, request, *args, **kwargs):
        form = PseudoForm(request.POST)

        if form.is_valid():
            request.session["user_anonym"] = form.cleaned_data["name"]
            return self.getOrCreateForm(request,request.session["user_anonym"],kwargs.get("key"))
        else:
            return render(request, self.html_login, locals())

    def getOrCreateForm(self,request,username,token,user=None,):
        
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
                user = user
            )
            return HttpResponseRedirect("/poll/"+token_admin)
        list_options = Option.objects.all()
        list_questions = Answer.objects.filter(question=question)
        return render(request, self.html, locals())

        
            
            

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()