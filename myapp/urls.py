# from django.contrib import admin
from django.urls import path
from . import auth
from . import views
urlpatterns = [
    path('', views.home, name="Home"),

    path('login/', auth.Login, name="Login"),
    path('logout/', auth.Logout, name="Logout"),


    path('medecins/', views.AllMedecins, name="AllMedecins"),
    path('medecins/add/', views.AddMedecin, name="AddMedecin"),
    path('medecins/<id>/', views.OneMedecin, name="OneMedecin"),
    path('medecins/<id>/update/', views.UpdateMedecin, name="UpdateMedecin"),
    path('medecins/<id>/rendezvous/', views.AllMedecinRendezVous, name="AllMedecinRendezVous"),
    path('medecins/<id>/rendezvous/en-attente/', views.AllMedecinRendezVousEnAttente, name="AllMedecinRendezVousEnAttente"),
    path('medecins/<id>/rendezvous/annule/', views.AllMedecinRendezVousAnnule, name="AllMedecinRendezVousAnnule"),
    path('medecins/<id>/rendezvous/termine/', views.AllMedecinRendezVousTemrine, name="AllMedecinRendezVousTemrine"),
    path('medecins/<id>/consultations/', views.AllMedecinConsultations, name="AllMedecinConsultations"),

    path('patients/', views.AllPatients, name="AllPatients"),
    path('patients/add/', views.AddPatient, name="AddPatient"),
    path('patients/<id>/', views.OnePatient, name="OnePatient"),
    path('patients/<id>/update/', views.UpdatePatient, name="UpdatePatient"),
    path('patients/<id>/rendezvous/', views.AllPatientRendezVous, name="AllPatientRendezVous"),
    path('patients/<id>/rendezvous/en-attente/', views.AllPatientRendezVousEnAttente, name="AllPatientRendezVousEnAttente"),
    path('patients/<id>/rendezvous/annule/', views.AllPatientRendezVousAnnule, name="AllPatientRendezVousAnnule"),
    path('patients/<id>/rendezvous/termine/', views.AllPatientRendezVousTemrine, name="AllPatientRendezVousTemrine"),
    path('patients/<id>/consultations/', views.AllPatientConsultations, name="AllPatientConsultations"),

    
    path('services/', views.AllServices, name="AllServices"),
    path('services/<id>/', views.OneService, name="OneService"),
    path('services/<id>/taches/', views.AllServiceTaches, name="AllServiceTaches"),
    path('services/<id>/update/', views.UpdateService, name="UpdateService"),

    path('rendezvous/', views.AllRendezVous, name="AllRendezVous"),
    path('rendezvous/<id>/', views.OneRendezVous, name="OneRendezVous"),
    path('rendezvous/<id>/update/', views.UpdateRendezVous, name="UpdateRendezVous"),
    path('rendezvous/<id>/addconsultation/', views.AddConsultation, name="AddConsultation"),
    path('rendezvous/<id>/delete/', views.deleterdv, name="deleterdv"),
    path('rendezvous/selectdatetime/', views.SelectDatetime, name="SelectDatetime"),
    path('rendezvous/add/', views.AddRendezVous, name="AddRendezVous"),

    path('consultations/', views.AllConsultations, name="AllConsultations"),
    path('consultations/<id>/', views.OneConsultation, name="OneConsultation"),
    path('consultations/<id>/update/', views.UpdateConsultation, name="UpdateConsultation"),

    path('salles/', views.AllSalles, name="AllSalles"),
    path('salles/add/', views.AddSalle, name="AddSalle"),
    path('salles/<id>/rendezvous/', views.AllSalleRendezVous, name="AllSalleRendezVous"),
    path('salles/<id>/rendezvous/en-attente/', views.AllSalleRendezVousEnAttente, name="AllSalleRendezVousEnAttente"),
    path('salles/<id>/rendezvous/annule/', views.AllSalleRendezVousAnnule, name="AllSalleRendezVousAnnule"),
    path('salles/<id>/rendezvous/termine/', views.AllSalleRendezVousTemrine, name="AllSalleRendezVousTemrine"),


    path('taches/', views.AllTaches, name="AllTaches"),
    path('taches/add/', views.AddTache, name="AddTache"),
    path('taches/<id>/', views.OneTache, name="OneTache"),
    path('taches/<id>/update/', views.UpdateTache, name="UpdateTache"),
]