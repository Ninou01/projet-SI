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
    path('medecins/<int:id>/', views.OneMedecin, name="OneMedecin"),
    path('medecins/<int:id>/update/', views.UpdateMedecin, name="UpdateMedecin"),
    path('medecins/<int:id>/rendezvous/', views.AllMedecinRendezVous, name="AllMedecinRendezVous"),
    path('medecins/<int:id>/rendezvous/en-attente/', views.AllMedecinRendezVousEnAttente, name="AllMedecinRendezVousEnAttente"),
    path('medecins/<int:id>/rendezvous/annule/', views.AllMedecinRendezVousAnnule, name="AllMedecinRendezVousAnnule"),
    path('medecins/<int:id>/rendezvous/termine/', views.AllMedecinRendezVousTemrine, name="AllMedecinRendezVousTemrine"),
    path('medecins/<int:id>/consultations/', views.AllMedecinConsultations, name="AllMedecinConsultations"),

    path('patients/', views.AllPatients, name="AllPatients"),
    path('patients/add/', views.AddPatient, name="AddPatient"),
    path('patients/<int:id>/', views.OnePatient, name="OnePatient"),
    path('patients/<int:id>/update/', views.UpdatePatient, name="UpdatePatient"),
    path('patients/<int:id>/rendezvous/', views.AllPatientRendezVous, name="AllPatientRendezVous"),
    path('patients/<int:id>/rendezvous/en-attente/', views.AllPatientRendezVousEnAttente, name="AllPatientRendezVousEnAttente"),
    path('patients/<int:id>/rendezvous/annule/', views.AllPatientRendezVousAnnule, name="AllPatientRendezVousAnnule"),
    path('patients/<int:id>/rendezvous/termine/', views.AllPatientRendezVousTemrine, name="AllPatientRendezVousTemrine"),
    path('patients/<int:id>/consultations/', views.AllPatientConsultations, name="AllPatientConsultations"),

    
    path('services/', views.AllServices, name="AllServices"),
    path('services/<int:id>/', views.OneService, name="OneService"),
    path('services/<int:id>/taches/', views.AllServiceTaches, name="AllServiceTaches"),
    path('services/<int:id>/update/', views.UpdateService, name="UpdateService"),

    path('rendezvous/', views.AllRendezVous, name="AllRendezVous"),
    path('rendezvous/<int:id>/', views.OneRendezVous, name="OneRendezVous"),
    path('rendezvous/<int:id>/update/', views.UpdateRendezVous, name="UpdateRendezVous"),
    path('rendezvous/<int:id>/addconsultation/', views.AddConsultation, name="AddConsultation"),
    path('rendezvous/<int:id>/delete/', views.deleterdv, name="deleterdv"),
    path('rendezvous/selectdatetime/', views.SelectDatetime, name="SelectDatetime"),
    path('rendezvous/add/', views.AddRendezVous, name="AddRendezVous"),

    path('consultations/', views.AllConsultations, name="AllConsultations"),
    path('consultations/<int:id>/', views.OneConsultation, name="OneConsultation"),
    path('consultations/<int:id>/update/', views.UpdateConsultation, name="UpdateConsultation"),

    path('salles/', views.AllSalles, name="AllSalles"),
    path('salles/add/', views.AddSalle, name="AddSalle"),
    path('salles/<int:id>/rendezvous/', views.AllSalleRendezVous, name="AllSalleRendezVous"),
    path('salles/<int:id>/rendezvous/en-attente/', views.AllSalleRendezVousEnAttente, name="AllSalleRendezVousEnAttente"),
    path('salles/<int:id>/rendezvous/annule/', views.AllSalleRendezVousAnnule, name="AllSalleRendezVousAnnule"),
    path('salles/<int:id>/rendezvous/termine/', views.AllSalleRendezVousTemrine, name="AllSalleRendezVousTemrine"),


    path('taches/', views.AllTaches, name="AllTaches"),
    path('taches/add/', views.AddTache, name="AddTache"),
    path('taches/<int:id>/', views.OneTache, name="OneTache"),
    path('taches/<int:id>/update/', views.UpdateTache, name="UpdateTache"),
]