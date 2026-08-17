import random
from profil.models import Etudiant
from datetime import datetime ,date
from profil.models import Utilisateur

def generematricule():
    date = datetime.now().year
    jour = str(random.randint(1000 , 9999))
    matricule = f"BMN-{date}-{jour}"

    while Etudiant.objects.filter(matricule=matricule).exists():
        jour = str(random.randint(1000 , 9999))
        matricule = f"BMN-{date}-{jour}"

    return matricule
        

def genereemail(nom,prenom):
    email = f"{nom}.{prenom}@gmail.com"
    nombre = random.randint(1,9)
    while Utilisateur.objects.filter(email = email ).exists():
        email =  f"{nom}.{prenom}{nombre}@gmail.com"
    return email


def generepassword(nom : str):
    date= datetime.now().year
    nom_up = nom.lower()
    password = f"{nom_up}{date}"
    return password 



def annee_scolaire():
    today = date.today()
    if today.month >= 9:  # à partir de septembre
        return f"{today.year}-{today.year + 1}"
    else:
        return f"{today.year - 1}-{today.year}"

def annee(request):
    return {"annee_scolaire": annee_scolaire()}
