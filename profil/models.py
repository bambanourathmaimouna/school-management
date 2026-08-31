from django.db import models
from django.contrib.auth.models import AbstractUser



class Utilisateur(AbstractUser):
    ROLE = (
        ('admin', 'administrateur'),
        ('professeur', 'professeur'),
        ('etudiant', 'etudiant')
    )

    role = models.CharField(max_length=40, choices=ROLE)
    
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.username}"
    
    
class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    matricule = models.CharField(max_length=50, unique=True)
    classe = models.ForeignKey('school.classe', on_delete=models.CASCADE)
    user_name = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    classe = models.ForeignKey('school.classe', on_delete=models.CASCADE)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    matiere = models.ForeignKey('school.matiere', on_delete=models.CASCADE, related_name='professeurs')    

    def __str__(self):
        return f"{self.nom} {self.prenom}"




