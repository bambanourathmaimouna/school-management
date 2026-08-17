from django.db import models
from profil.models import Utilisateur
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.


class Classe(models.Model):
    classe = models.CharField(max_length= 50)
    def __str__(self):
        return self.classe


class Matiere(models.Model):
    matiere = models.CharField(max_length= 100)
    def __str__(self):
        return self.matiere
        



