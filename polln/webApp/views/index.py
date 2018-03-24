from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from webApp.forms import LoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from webApp.utils.arel import Arel
from django.contrib.auth.models import User

class Index(View):
    html = 'webApp/index.html'

    """
        Renvoie la page d'Inscription au chargement de la page
    """
    def get(self, request, *args, **kwargs):
        if('username' in request.session):
            return HttpResponseRedirect(reverse('home'))
        else:
            form = LoginForm()
            return render(request, self.html, locals())
    def post(self,request,*args):
        form = LoginForm(request.POST)
        error = ""
        if form.is_valid():
            print("valid !")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            arel = Arel()
            token = arel.get_token(username,password) #request to get token for arel

            if (token):
                print("token !")
                '''
                rep_arel = arel.requete_arel('api/me',token) #request to get infos for user
                nom = rep_arel['lastName']
                prenom = rep_arel['firstName']
                email = rep_arel['email']
                '''
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username,password='')
                
                request.session['username'] = username
                return HttpResponseRedirect(reverse('home'))
        error = "username or password incorrect"
        return render(request, self.html, locals())

