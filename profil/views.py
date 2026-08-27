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
from django.db.models import Q

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
                messages.success(request,f"L'étudiant {nom} {prenom} a été créé. Mot de passe généré : {password}")
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
    nbr_etudiant = etudiants.count()
    nbr_note = Note.objects.filter(matiere=professeur.matiere,etudiant__classe=professeur.classe).count()
    nbr_absence = Absence.objects.filter( professeur=professeur).count()

    for etudiant in etudiants:
        etudiant.number_note = Note.objects.filter(etudiant=etudiant,matiere=professeur.matiere).count()
        etudiant.number_absence = Absence.objects.filter(etudiant=etudiant,professeur=professeur).count()
    context = {
        "etudiants": etudiants,
        "nbr_etudiant": nbr_etudiant,
        "nbr_note": nbr_note,
        "nbr_absence": nbr_absence,
    }
    return render(request,"template_profil/accueil_professeur.html",context)


def accueil_etudiant(request):
    etudiant = get_object_or_404(Etudiant,user_name=request.user)
    notes = Note.objects.filter(etudiant=etudiant).order_by("-id")
    absences = Absence.objects.filter(etudiant=etudiant)
    nbr_note = notes.count()
    nbr_absence = absences.count()
    if nbr_note > 0:
        moyenne = sum(note.note for note in notes) / nbr_note
        moyenne_generale = round(moyenne, 2)
    else:
        moyenne_generale = 0
    dernieres_notes = notes[:10]
    context = {
        "etudiant": etudiant,
        "notes": notes,
        "dernieres_notes": dernieres_notes,
        "nbr_note": nbr_note,
        "nbr_absence": nbr_absence,
        "moyenne_generale": moyenne_generale,
    }

    return render (request,"template_profil/accueil_etudiant.html",context)

        
def liste_etudiant(request):
        recherche = request.GET.get('q', '').strip()
        etudiant = Etudiant.objects.all()
        if recherche:
                etudiant = etudiant.filter(
                    Q(nom__icontains=recherche) |
                    Q(prenom__icontains=recherche) |
                    Q(matricule__icontains=recherche) |
                    Q(classe__classe__icontains=recherche)
                )

        return render(request, "template_profil/liste_etudiant.html", {'etudiant': etudiant, })
   

def liste_professeur(request):
   recherche = request.GET.get('q', '').strip()
   professeur = Professeur.objects.all()
   if recherche:
    professeur = professeur.filter(
    Q(nom__icontains=recherche) |
    Q(matiere__matiere__icontains=recherche) |
    Q(prenom__icontains=recherche) |
    Q(classe__classe__icontains=recherche)
    )
   return render(request,"template_profil/liste_professeur.html",{'professeur':professeur})


def liste_utilisateur(request):
   recherche = request.GET.get('q', '').strip()
   utilisateurs = Utilisateur.objects.all()
   if recherche:
        utilisateurs = utilisateurs.filter(
        Q(first_name__icontains=recherche) |
        Q(last_name__icontains=recherche) |
        Q(username__icontains=recherche) |
        Q(email__icontains=recherche) |
        Q(role__icontains=recherche)
    )
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
    return render(request,"template_profil/modifier_utilisateur.html",{"id": id,"utilisateurs":utilisateurs,"form":form})


def supprimer_etudiant(request, id):
    etudiant = get_object_or_404(Etudiant, id=id)
    if request.method == "POST":
        etudiant.delete()
        return redirect("liste_etudiant")
    return render(request,"template_profil/supprimer_etudiant.html",{"etudiant": etudiant} )


def supprimer_utilisateur(request, id):
    utilisateur = get_object_or_404(Utilisateur, id=id)
    if request.method == "POST":
        utilisateur.delete()
        return redirect("liste_utilisateur")
    return render(request,"template_profil/supprimer_utilisateur.html",{"utilisateur": utilisateur})

def supprimer_professeur(request, id):
    professeur = get_object_or_404(Professeur, id=id)
    if request.method == "POST":
        professeur.delete()
        return redirect("liste_professeur")
    return render(request,"template_profil/supprimer_professeur.html",{"professeur": professeur})

def home(request):
   return render(request,"template_profil/base.html")


def lister_etudiant_prof(request):
    try:
        professeur = request.user.professeur
        classe = professeur.classe
        matiere = professeur.matiere
        recherche = request.GET.get('q', '').strip()
        etudiants = Etudiant.objects.filter(classe=classe)
        if recherche:
            etudiants = etudiants.filter(
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche) |
                Q(matricule__icontains=recherche)
            )

    except ObjectDoesNotExist:
        professeur = None
        classe = None
        matiere = None
        recherche = ''
        etudiants = Etudiant.objects.none()

    context = {
        'etudiants': etudiants,
        'matiere': matiere,
        'classe': classe,
        'professeur': professeur,
        'recherche': recherche,
    }

    return render(request,"template_profil/lister_etudiant_prof.html", context)


