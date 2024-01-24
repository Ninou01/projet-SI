from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

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

# class CustomUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     nom = models.CharField(max_length=255, blank=True, null=True)
#     prenom = models.CharField(max_length=255, blank=True, null=True)
#     dateNaissance = models.DateField(blank=True, null=True)
#     sexe = models.CharField(max_length=10, blank=True, null=True, choices=sexe_choices)
#     adresse = models.TextField(blank=True, null=True)
#     num_tel = models.CharField(max_length=20, blank=True, null=True)

#     def __str__(self):
#         return f"{self.Nom} {self.Prenom}"

#     def save(self, *args, **kwargs):
#         self.user.first_name = self.prenom
#         self.user.last_name = self.nom
#         self.user.username = f"{self.last_name} {self.first_name}"
#         super().save(*args, **kwargs)

#     @property
#     def role(self):
#         return None

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    dateNaissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True, choices=sexe_choices)
    adresse = models.TextField(blank=True, null=True)
    num_tel = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, null=True)

    class Meta:
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def clean(self):
        if self.dateNaissance and self.dateNaissance > timezone.now().date():
            raise ValidationError("Date of birth cannot be greater than today's date.")

    def save(self, *args, **kwargs):
        self.clean()
        self.user.first_name = self.prenom
        self.user.last_name = self.nom
        self.user.username = f"{self.nom} {self.prenom}"
        self.user.email = self.email
        self.user.save() 
        super().save(*args, **kwargs)

    @property
    def role(self):  # Fix the typo here
        return role.get("Patient")
    
class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    dateNaissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True, choices=sexe_choices)
    adresse = models.TextField(blank=True, null=True)
    num_tel = models.CharField(max_length=20, blank=True, null=True)
    specialite = models.CharField(max_length=30, blank=True, null=True, choices=SPECIALITE_CHOICES)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='medecins')
    email = models.EmailField(unique=True, null=True)

    class Meta:
        verbose_name_plural = "Medecins"

    @property
    def role(self):  # Fix the typo here
        return role.get("Patient")
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    def clean(self):
        if self.dateNaissance and self.dateNaissance > timezone.now().date():
            raise ValidationError("Date of birth cannot be greater than today's date.")

    def save(self, *args, **kwargs):
        self.clean()
        self.user.first_name = self.prenom
        self.user.last_name = self.nom
        self.user.username = f"{self.nom} {self.prenom}"
        self.user.email = self.email
        self.user.save() 
        super().save(*args, **kwargs)
    
    def is_disponible(self, date, heure):
        return True
    
class Service(models.Model):
    nom = models.CharField(max_length=255)
    chef = models.OneToOneField(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='chef_de_service')

    def clean(self):
        if self.chef and self.chef.service.pk != self.pk:
            raise ValidationError("chef_service must be from the current service")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Service {self.nom} - Chef: {self.chef}"
    
class Tache(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tache: {self.titre} - Service: {self.service}"
    

class Salle(models.Model):
    numero = models.PositiveIntegerField(unique=True)

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

    old_status = None

    def __str__(self):
        return f"RendezVous for {self.patient} with {self.medecin} on {self.Date} at {self.Heure}"
    
    def clean(self):
        if self.pk is not None:  # Check if the instance has already been saved
            original_instance = RendezVous.objects.get(pk=self.pk)
            self.old_status = original_instance.status  # Store the old status

            if self.old_status == STATUS_CHOICES[3][1]:  # Check if original status is 'terminé'
                raise ValueError("Cannot modify a RendezVous with status 'terminé'")
            
        current_datetime = timezone.now()
        if self.Date and self.Date < current_datetime.date():
            raise ValidationError("Date must be greater than or equal to the current date.")
        elif self.Heure and self.Date == current_datetime.date() and self.Heure < current_datetime.time():
            raise ValidationError("Heure must be greater than or equal to the current time.")
    
    def save(self, *args, **kwargs):
        self.clean()
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




