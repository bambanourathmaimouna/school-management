from django import forms
from .models import *



class Classeform(forms.ModelForm):
    class Meta:
        model = Classe
        fields = "__all__"


class Matiereform(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = "__all__"