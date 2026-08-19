from django.urls import path
from .views import *
from school.views import *
from bulletin.views import *
urlpatterns = [
    
    path('home/',home,name='home'),
    path('', connexion,name='connexion'),
    path('deconnexion/', deconnexion,name='deconnexion'),
    path('accueil_admin/',accueil_admin,name='accueil_admin'),


    path('accueil_professeur/',accueil_professeur,name='accueil_professeur'),
    path('ajouter_professeur/', ajouter_professeur,name='ajouter_professeur'),
    path('liste_professeur/',liste_professeur,name='liste_professeur'),
    path('modifier_professeur/<int:id>/',modifier_professeur,name='modifier_professeur'),
    path('supprimer_professeur/<int:id>/',supprimer_professeur,name='supprimer_professeur'),


    path('accueil_etudiant/',accueil_etudiant,name='accueil_etudiant'),
    path('ajouter_etudiant/', ajouter_etudiant,name='ajouter_etudiant'),
    path('liste_etudiant/',liste_etudiant,name='liste_etudiant'),
    path('modifier_etudiant/<int:id>/',modifier_etudiant,name='modifier_etudiant'),
    path('supprimer_etudiant/<int:id>/',supprimer_etudiant,name='supprimer_etudiant'),
   
    
    
   
    path('liste_utilisateur/',liste_utilisateur,name='liste_utilisateur'),
    path('modifier_utilisateur/<int:id>/',modifier_utilisateur,name='modifier_utilisateur'),
    path('supprimer_utilisateur/<int:id>/',supprimer_utilisateur,name='supprimer_utilisateur'),


    path('ajouter_classe/',ajouter_classe,name='ajouter_classe'),
    path('lister_classe/',lister_classe,name='lister_classe'),
    path('modifier_classe/<int:id>/',modifier_classe,name='modifier_classe'),
    path('supprimer_classe/<int:id>/',supprimer_classe,name='supprimer_classe'),

    path('ajouter_matiere/',ajouter_matiere,name='ajouter_matiere'),
    path('lister_matiere/',lister_matiere,name='lister_matiere'),
    path('modifier_matiere/<int:id>/',modifier_matiere, name='modifier_matiere'),
    path('supprimer_matiere/<int:id>/',supprimer_matiere,name='supprimer_matiere'),

    path('lister_note/',lister_note,name='lister_note'),
    path('ajouter_note/<int:id>/',ajouter_note,name='ajouter_note'),   
    path('note_modifier/<int:id>/', modifier_note, name='modifier_note'),
    path('note_supprimer/<int:id>/', supprimer_note, name='supprimer_note'), 

      
    path('lister_etudiant_prof/',lister_etudiant_prof,name='lister_etudiant_prof'), 

    path('lister_absence/', lister_absence, name='lister_absence'),
    path('ajouter_absence/<int:id>/', ajouter_absence, name='ajouter_absence'),
    path('modifier_absence/<int:id>/',modifier_absence,name='modifier_absence'),
    path('supprimer_absence/<int:id>/', supprimer_absence, name='supprimer_absence'), 


    
    path("mes_notes/",lister_note_etudiant,name="lister_note_etudiant"),
    path("mes_absences/",mes_absences,name="mes_absences"),
    path("accueil_etudiant/",accueil_etudiant,name="accueil_etudiant"),
    path("bulletin/",bulletin,name="bulletin"),
    
]
