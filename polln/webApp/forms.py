from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Pseudo",max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,label="Mot de passe")

class PseudoForm(forms.Form):
    name = forms.CharField(max_length=100)
