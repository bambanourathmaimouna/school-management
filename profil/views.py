from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from .forms import *
from .models import *
from school.forms import *
from school.models import *
from django.contrib import messages
from django.db import transaction
from school.matricule import generematricule,generepassword,genereemail
from django.contrib import messages
from bulletin.models import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import Connexionform

def connexion(request):
    if request.method == 'POST':
        form = Connexionform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                role = getattr(user, 'role', None) 
                if role == 'admin':
                    return redirect("accueil_admin")
                elif role == 'professeur':
                    return redirect("accueil_professeur")
                elif role == 'etudiant':
                    return redirect("accueil_etudiant")
                else:
                    messages.error(request, "Aucun rôle attribué à cet utilisateur.")
                    return redirect("login")  
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = Connexionform()
    return render(request, "template_profil/login.html", {'form': form})



def deconnexion (request):
    return redirect('connexion')




def ajouter_etudiant(request):
    forms = Etudiantform()
    if request.method == 'POST':
        forms = Etudiantform(request.POST)
        if forms.is_valid():
            data = forms.cleaned_data
            nom = data["nom"]
            prenom = data["prenom"]
            age = data["age"]
            classe = data["classe"]
            matricule = generematricule()
            email = genereemail(nom, prenom)
            password = generepassword(nom)
            try:
                with transaction.atomic():
                    user = Utilisateur.objects.create_user(username=email,password=password,first_name=nom,last_name=prenom,email=email,role='etudiant')
                    Etudiant.objects.create(user_name=user,nom=nom,prenom=prenom,age=age,classe=classe,matricule=matricule)
                messages.success(request,f"L'étudiant {nom} {prenom} a été créé.")
                return redirect('liste_etudiant')
            except Exception as erreur:
                messages.error(request, str(erreur))
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    return render(request,'template_profil/ajouter_etudiant.html',{'forms': forms})



def ajouter_professeur(request):
    forms = Professeurform()
    if request.method == 'POST':
        forms = Professeurform(request.POST)
        if forms.is_valid():
            data = forms.cleaned_data
            nom = data["nom"]
            prenom = data["prenom"]
            classe = data["classe"]
            matiere = data["matiere"]
            email = genereemail(nom, prenom)
            password = generepassword(nom)
            try:
                with transaction.atomic():
                    user = Utilisateur.objects.create_user(username=email,password=password,first_name=nom,last_name=prenom,email=email,role='professeur')
                    Professeur.objects.create(utilisateur=user,nom=nom,prenom=prenom,classe=classe,matiere=matiere)
                messages.success(request,f"Le professeur {nom} {prenom} a été créé. Mot de passe généré : {password}")
                return redirect('liste_professeur')
            except Exception as erreur:
                messages.error(request, str(erreur))
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
  
    return render(request,'template_profil/ajouter_professeur.html', {'forms': forms})




def accueil_admin(request):
    context={
    'nbr_etudiant' : Etudiant.objects.count(),
    'nbr_proffeseur' : Professeur.objects.count(),
    'nbr_utilisateur':Utilisateur.objects.count(),
    'nbr_classe' :Classe.objects.count(),
    'nbr_matiere' :Matiere.objects.count(),
    'nbr_note':Note.objects.count(),
    'nbr_absence':Absence.objects.count(),
    }
    return render (request,"template_profil/accueil_admin.html",context)


def accueil_professeur(request):
    professeur = request.user.professeur
    etudiants = Etudiant.objects.filter(classe=professeur.classe)
    context = {
        "professeur": professeur,
        "etudiants": etudiants,
    }

    return render(request,"template_profil/accueil_professeur.html",context)


def accueil_etudiant(request):
    return render (request,"template_profil/accueil_etudiant.html")


def liste_etudiant(request):
   etudiant = Etudiant.objects.all()
   return render(request,"template_profil/liste_etudiant.html",{'etudiant':etudiant})


def liste_professeur(request):
   professeur = Professeur.objects.all()
   return render(request,"template_profil/liste_professeur.html",{'professeur':professeur})


def liste_utilisateur(request):
   utilisateurs = Utilisateur.objects.all()
   return render(request,"template_profil/liste_utilisateur.html",{'utilisateurs':utilisateurs})


def modifier_etudiant(request, id):
    etudiant = get_object_or_404(Etudiant,id=id)
    if request.method == 'POST':
        forms = Etudiantform(request.POST, instance=etudiant)
        if forms.is_valid():
            forms.save()
            return redirect('liste_etudiant')
    else:
        forms = Etudiantform(instance=etudiant)
    return render(request,"template_profil/ajouter_etudiant.html",{"id": id,"etudiant":etudiant,"forms":forms})


def modifier_professeur(request, id):
    professeur = get_object_or_404(Professeur, id=id)

    if request.method == 'POST':
        forms = Professeurform(request.POST, instance=professeur)
        if forms.is_valid():
            forms.save()
            return redirect('liste_professeur')
    else:
        forms = Professeurform(instance=professeur)
    return render(request,"template_profil/ajouter_professeur.html",{"id": id,"professeur":professeur,"forms":forms})


def modifier_utilisateur(request, id):
    utilisateurs = get_object_or_404(Utilisateur,id= id)
    if request.method == 'POST':
        form = Utilisateurform(request.POST, instance=utilisateurs)
        if form.is_valid():
            form.save()
            return redirect('liste_utilisateur')
    else:
        form = Utilisateurform(instance=utilisateurs)
    return render(request,"template_profil/ajouter_utilisateur.html",{"id": id,"utilisateurs":utilisateurs,"form":form})



def supprimer_etudiant(request, id):
    etudiant =  get_object_or_404(Etudiant,id=id)
    etudiant.delete()
    return redirect("liste_etudiant")


def supprimer_utilisateur(request, id):
    utilisateurs =  get_object_or_404(Utilisateur,id=id)
    utilisateurs.delete()
    return redirect("liste_utilisateur")

def supprimer_professeur(request, id):
    professeur =  get_object_or_404(Professeur,id=id)
    professeur.delete()
    return redirect("liste_professeur")



def home(request):
   return render(request,"template_profil/base.html")


def lister_etudiant_prof(request):
    try:
        professeur = request.user.professeur
        classe = professeur.classe
        matiere = professeur.matiere

        if classe:
            etudiants = Etudiant.objects.filter(classe=classe)
        else:
            etudiants = Etudiant.objects.none()
          
    except ObjectDoesNotExist:
        professeur = None
        classe = None
        matiere = None
        etudiants = Etudiant.objects.none()

    context = {
        'etudiants': etudiants,
        'matiere': matiere,
        'classe': classe,
        'professeur': professeur
    }

    
    return render(request, "template_profil/lister_etudiant_prof.html", context)