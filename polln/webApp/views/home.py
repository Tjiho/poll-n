from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

class Home(View):
    html = 'webApp/home.html'

    """
        Renvoie la page d'Inscription au chargement de la page
    """
    def get(self, request, *args, **kwargs):
        return render(request, self.html, locals())