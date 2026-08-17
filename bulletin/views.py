from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

def ajouter_note(request,id):
    professeur = request.user.professeur
    matiere = professeur.matiere
    etudiant = get_object_or_404(Etudiant,id=id,classe=professeur.classe)
    if request.method == 'POST':
        form = Noteform(request.POST, professeur=professeur)
        if form.is_valid():
            Note.objects.create(etudiant=etudiant,matiere=matiere,note=form.cleaned_data['note'])
            return redirect('lister_note')
        else:
            print(form.errors)
    else:
   
        form = Noteform(professeur=professeur)
    context = {
        'form': form,
        'etudiant': etudiant,
    }
    return render(request,"template_bulletin/ajouter_note.html",context)


def lister_note(request):
    professeur = request.user.professeur
    etudiants = Etudiant.objects.filter(classe=professeur.classe)
    notes = Note.objects.filter(etudiant__classe=professeur.classe,matiere=professeur.matiere).order_by('etudiant_id', 'id') 
    notes_par_etudiant = {}
    for n in notes:
        notes_par_etudiant.setdefault(n.etudiant_id, []).append(n)

    max_notes = max((len(v) for v in notes_par_etudiant.values()), default=0)
    for etudiant in etudiants:
        liste_notes = notes_par_etudiant.get(etudiant.id, [])
        liste_notes = liste_notes + [None] * (max_notes - len(liste_notes))
        etudiant.notes_professeur = liste_notes
    context = {
        'etudiants': etudiants,
        'professeur': professeur,
        'range_notes': range(max_notes),
    }
    return render(request, "template_bulletin/lister_note.html", context)



def modifier_note(request, id):
    professeur = request.user.professeur
    note = get_object_or_404(Note, id=id, etudiant__classe=professeur.classe,matiere=professeur.matiere)
    if request.method == 'POST':
        form = Noteform(request.POST, professeur=professeur)
        if form.is_valid():
            note.note = form.cleaned_data['note']
            note.save()
            return redirect('lister_note')
    else:
        form = Noteform(professeur=professeur, initial={'note': note.note})
    context = {
        'form': form,
        'etudiant': note.etudiant,
        'note': note,
        }
    return render(request,"template_bulletin/ajouter_note.html",context)


def supprimer_note(request, id):
    professeur = request.user.professeur
    note = get_object_or_404(Note,id=id,etudiant__classe=professeur.classe,matiere=professeur.matiere)

    if request.method == 'POST':
        note.delete()
        return redirect('lister_note')
    context = {'note': note}
    return render(request, "template_bulletin/supprimer_note.html", context)



def ajouter_absence(request, id):
    professeur = request.user.professeur
    matiere = professeur.matiere
    etudiant = get_object_or_404(Etudiant, id=id, classe=professeur.classe)

    if request.method == 'POST':
        form = Absenceform(request.POST, professeur=professeur)
        if form.is_valid():
            Absence.objects.create(etudiant=etudiant,date=form.cleaned_data['date'],motif=form.cleaned_data['motif'],justification=form.cleaned_data['justification'])
            return redirect('lister_absence')
    else:
        form = Absenceform(professeur=professeur)

    context = {
        'form': form,
        'etudiant': etudiant,
    }
    return render(request, "template_bulletin/ajouter_absence.html", context)


def lister_absence(request):
    professeur = request.user.professeur
    etudiants = Etudiant.objects.filter(classe=professeur.classe)
    absences = Absence.objects.filter(etudiant__classe=professeur.classe).order_by('etudiant_id','id')
    absences_par_etudiant = {}
    for absence in absences:
        absences_par_etudiant.setdefault(absence.etudiant_id,[]).append(absence)

    max_absences = max((len(v) for v in absences_par_etudiant.values()), default=0)
    for etudiant in etudiants:
        liste_absences = absences_par_etudiant.get(etudiant.id,[])
        liste_absences = liste_absences + [None] * (max_absences - len(liste_absences))
        etudiant.absences_professeur = liste_absences

    context = {
        'etudiants': etudiants,
        'professeur': professeur,
        'range_absences': range(max_absences),
    }
    return render( request,"template_bulletin/lister_absence.html",context)



def modifier_absence(request, id):
    professeur = request.user.professeur

    absence = get_object_or_404(
        Absence,
        id=id,
        etudiant__classe=professeur.classe
    )

    if request.method == 'POST':
        form = Absenceform(
            request.POST,
            instance=absence,
            professeur=professeur
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "L'absence a été modifiée avec succès."
            )
            return redirect('lister_absence')

    else:
        form = Absenceform(
            instance=absence,
            professeur=professeur
        )

    return render(
        request,
        'template_bulletin/ajouter_absence.html',
        {
            'form': form,
            'modifier': True,
            'absence': absence,
        }
    )


def supprimer_absence(request, id):
    professeur = request.user.professeur

    absence = get_object_or_404(
        Absence,
        id=id,
        etudiant__classe=professeur.classe
    )

    if request.method == 'POST':
        absence.delete()

        messages.success(
            request,
            "L'absence a été supprimée avec succès."
        )

        return redirect('lister_absence')

    return render(
        request,
        'template_bulletin/supprimer_absence.html',
        {
            'absence': absence
        }
    )
    