from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from webApp.models import Question,Anonym_user,Answer,User


class Home(View):
    html = 'webApp/home.html'

    """
        Renvoie la page d'Inscription au chargement de la page
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            print(dir(user))
            print(user.question_set.all())
            return render(request, self.html, locals())