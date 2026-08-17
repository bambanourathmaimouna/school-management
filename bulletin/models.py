from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from school.models import Matiere
from profil.models import Etudiant

# Create your models here.


class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    note = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(20)])
    date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.nom

class Absence(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date = models.DateField()
    motif = models.CharField(max_length=50)
    justification = models.BooleanField(default=False,null=True,blank= True)

    
    def __str__(self):
        return f"{self.etudiant} {self.date}"
   