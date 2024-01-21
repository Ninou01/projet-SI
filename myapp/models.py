from django.db import models
from django.contrib.auth.models import User

# Create your models here.

sexe_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
]

class Patient(User):
    Nom = models.CharField(max_length=255, blank=True, null=True)
    Prenom = models.CharField(max_length=255, blank=True, null=True)
    DateNaissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True, choices=sexe_choices)
    Adresse = models.TextField(blank=True, null=True)
    num_tel = models.CharField(max_length=20, blank=True, null=True)
    # email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.Nom} {self.Prenom}"


class Medecin(User):

    SPECIALITE_CHOICES = [
        ('Cardiologue', 'Cardiologue'),
        ('Neurologue', 'Neurologue'),
        ('Urologue', 'Urologue'),
        ('Rhumatologue', 'Rhumatologue'),
        ('ORL', 'ORL'),
        ('Generaliste', 'Generaliste'),
    ]

    Nom = models.CharField(max_length=255, blank=True, null=True)
    Prenom = models.CharField(max_length=255, blank=True, null=True)
    DateNaissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True, choices=sexe_choices)
    Adresse = models.TextField(blank=True, null=True)
    num_tel = models.CharField(max_length=20, blank=True, null=True)
    # email = models.EmailField(blank=True, null=True)
    specialite = models.CharField(max_length=30, blank=True, null=True, choices=SPECIALITE_CHOICES)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='medecins')


    def __str__(self):
        return f"{self.Nom} {self.Prenom}"
    
    def is_disponible(date, heure):
        return False
    
class Service(models.Model):
    nom = models.CharField(max_length=255)
    chef = models.OneToOneField(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='chef_de_service')

    def __str__(self):
        return f"Service {self.nom} - Chef: {self.chef}"
    

class Salle(models.Model):
    numero = models.CharField(max_length=10)

    def __str__(self):
        return f"Salle {self.numero}"
    
    def is_disponible(date, heure):
        return False



class RendezVous(models.Model):
    Date = models.DateField(blank=True, null=True)
    Heure = models.TimeField(blank=True, null=True)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    confirmer = models.BooleanField(default=False)

    def __str__(self):
        return f"RendezVous for {self.patient} with {self.medecin} on {self.Date} at {self.Heure}"


class Tache(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tache: {self.titre} - Service: {self.service}"


