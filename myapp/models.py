from django.db import models
from django.contrib.auth.models import User

# Create your models here.

role = {
    "Patient": "Patient", 
    "Medecin": "Medecin", 
}

sexe_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
]

SPECIALITE_CHOICES = [
    ('Cardiologue', 'Cardiologue'),
    ('Neurologue', 'Neurologue'),
    ('Urologue', 'Urologue'),
    ('Rhumatologue', 'Rhumatologue'),
    ('ORL', 'ORL'),
    ('Generaliste', 'Generaliste'),
]

STATUS_CHOICES = [
        ('en-attente', 'en-attente'),
        ('confirmé', 'confirmé'),
        ('annulé', 'annulé'),
        ('terminé', 'terminé'),
    ]

class CustomUser(User):
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    dateNaissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True, choices=sexe_choices)
    adresse = models.TextField(blank=True, null=True)
    num_tel = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.Nom} {self.Prenom}"

    def save(self, *args, **kwargs):
        self.first_name = self.prenom
        self.last_name = self.nom
        self.username = f"{self.last_name} {self.first_name}"
        super().save(*args, **kwargs)

    @property
    def role(self):
        return None

class Patient(CustomUser):

    class Meta:
        verbose_name_plural = "Patients"

    @property
    def role(self):  # Fix the typo here
        return role.get("Patient")
    
class Medecin(CustomUser):
    specialite = models.CharField(max_length=30, blank=True, null=True, choices=SPECIALITE_CHOICES)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='medecins')
    
    class Meta:
        verbose_name_plural = "Medecins"

    @property
    def role(self):  # Fix the typo here
        return role.get("Patient")
    
    def is_disponible(self, date, heure):
        return True
    
class Service(models.Model):
    nom = models.CharField(max_length=255)
    chef = models.OneToOneField(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='chef_de_service')

    def __str__(self):
        return f"Service {self.nom} - Chef: {self.chef}"
    
class Tache(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tache: {self.titre} - Service: {self.service}"
    

class Salle(models.Model):
    numero = models.PositiveIntegerField()

    def __str__(self):
        return f"Salle {self.numero}"
    
    def is_disponible(self, date, heure):
        return True


class RendezVous(models.Model):
    Date = models.DateField(blank=True, null=True)
    Heure = models.TimeField(blank=True, null=True)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default=STATUS_CHOICES[0][1], choices=STATUS_CHOICES)

    def __str__(self):
        return f"RendezVous for {self.patient} with {self.medecin} on {self.Date} at {self.Heure}"
    
    def save(self, *args, **kwargs):
        if self.status == STATUS_CHOICES[3][1]:  # Check if status is 'terminé'
            raise ValueError("Cannot modify a RendezVous with status 'terminé'")
        super().save(*args, **kwargs)
    
class Consultation(models.Model): 
    rendezvous = models.OneToOneField(RendezVous ,on_delete=models.CASCADE)
    diagnostique = models.TextField()
    prescription = models.TextField()

    def __str__(self):
        patient_name = self.rendezvous.patient
        doctor_name = self.rendezvous.medecin
        return f"Consultation: {patient_name} - {doctor_name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.rendezvous.status = STATUS_CHOICES[3][1]  # Set status to 'terminé'
            self.rendezvous.save()  # Save the updated RendezVous instance
        super().save(*args, **kwargs)




