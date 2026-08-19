from django import forms
from .models import *



class Utilisateurform(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username','first_name','last_name','email','role',]
        help_texts = {"username": "",}



class Etudiantform(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom','prenom','age','classe']


class Professeurform(forms.ModelForm):
    class Meta:
        model = Professeur
        fields = ['nom','prenom','classe','matiere']
    



class Connexionform(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput(),label="Mot de passe")



