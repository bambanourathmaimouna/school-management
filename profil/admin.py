from django.contrib import admin
from .models import Utilisateur,Etudiant,Professeur
# Register your models here.

admin.site.register(Utilisateur)
admin.site.register(Etudiant)
admin.site.register(Professeur)