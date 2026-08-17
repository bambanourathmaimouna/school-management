from django import forms
from .models import *




class Noteform(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note']  # Ajoutez d'autres champs si nécessaire (ex: 'appreciation')

    def __init__(self, *args, **kwargs):
        # On extrait 'professeur' des arguments s'il est transmis
        professeur = kwargs.pop('professeur', None)
        super().__init__(*args, **kwargs)

        

class Absenceform(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date','motif','justification']

    def __init__(self, *args, **kwargs):
        # On extrait 'professeur' des arguments nommés
        professeur = kwargs.pop('professeur', None)
        super().__init__(*args, **kwargs)




