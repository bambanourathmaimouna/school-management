from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.

def ajouter_classe(request):
    forms = Classeform()
    if request.method == 'POST':
        forms=Classeform(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("lister_classe")
    else:
        forms=Classeform()
    return render(request,"template_school/ajouter_classe.html",{'forms':forms})


def lister_classe(request):
   classe = Classe.objects.all()
   return render(request,"template_school/lister_classe.html",{'classe':classe})


def modifier_classe(request, id):
    classe = get_object_or_404(Classe,id=id)
    if request.method == 'POST':
        forms = Classeform(request.POST, instance=classe)
        if forms.is_valid():
            forms.save()
            return redirect('lister_classe')
    else:
        forms = Classeform(instance=classe)
    return render(request,"template_school/ajouter_classe.html",{"id": id,"classe":classe,"forms":forms})


def supprimer_classe(request, id):
    classe =  get_object_or_404(Classe,id=id)
    classe.delete()
    return redirect("lister_classe")



def ajouter_matiere(request):
    forms = Matiereform()
    if request.method == 'POST':
        forms=Matiereform(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("lister_matiere")
    else:
        forms=Matiereform()
    return render(request,"template_school/ajouter_matiere.html",{'forms':forms})


def lister_matiere(request):
   matiere = Matiere.objects.all()
   return render(request,"template_school/lister_matiere.html",{'matiere':matiere})


def modifier_matiere(request, id):
    matiere = get_object_or_404(Matiere,id=id)
    if request.method == 'POST':
        forms = Matiereform(request.POST, instance=matiere)
        if forms.is_valid():
            forms.save()
            return redirect('lister_matiere')
    else:
        forms = Matiereform(instance=matiere)
    return render(request,"template_school/ajouter_matiere.html",{"id": id,"matiere":matiere,"forms":forms})


def supprimer_matiere(request, id):
    matiere =  get_object_or_404(Matiere,id=id)
    matiere.delete()
    return redirect("lister_matiere")