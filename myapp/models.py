from collections.abc import Iterable
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify


# Create your models here.

role = {
    "Patient": "Patient", 
    "Medecin": "Medecin", 
}

SEXE_CHOICES = [
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

SERVICE_NAME_CHOICES = [
    ('Cardiologie', 'Cardiologie'),
    ('Neurologie', 'Neurologie'),
    ('Urologie', 'Urologie'),
    ('Rhumatologie', 'Rhumatologie'),
    ('Oto-rhino-laryngologie', 'Oto-rhino-laryngologie'),
    ('Médecine Générale', 'Médecine Générale'),
]

STATUS_CHOICES = [
        ('en-attente', 'en-attente'),
        # ('confirmé', 'confirmé'),
        ('annulé', 'annulé'),
        ('terminé', 'terminé'),
    ]

# class CustomUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     nom = models.CharField(max_length=255, blank=True, null=True)
#     prenom = models.CharField(max_length=255, blank=True, null=True)
#     dateNaissance = models.DateField(blank=True, null=True)
#     sexe = models.CharField(max_length=10, blank=True, null=True, choices=SEXE_CHOICES)
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
    sexe = models.CharField(max_length=10, blank=True, null=True, choices=SEXE_CHOICES)
    adresse = models.TextField(blank=True, null=True)
    num_tel = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, null=True)

    class Meta:
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def clean(self):
        if self.dateNaissance:
            dateNaissance = datetime.strptime(self.dateNaissance, "%Y-%m-%d").date()
            if dateNaissance > timezone.now().date():
                raise ValidationError("Date of birth cannot be greater than today's date.")
        

    def save(self, *args, **kwargs):
        if not self.pk: 
            group, created = Group.objects.get_or_create(name='patient')
            self.user.groups.add(group)
        self.clean()
        
        self.user.first_name = self.prenom
        self.user.last_name = self.nom
        self.user.username = f"{self.email}"
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
    sexe = models.CharField(max_length=10, blank=True, null=True, choices=SEXE_CHOICES)
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
        if self.dateNaissance:
            dateNaissance = datetime.strptime(self.dateNaissance, "%Y-%m-%d").date()
            if dateNaissance > timezone.now().date():
                raise ValidationError("Date of birth cannot be greater than today's date.")

    def save(self, *args, **kwargs):
        if not self.pk: 
            group, created = Group.objects.get_or_create(name='medecin')
            self.user.groups.add(group)

        self.clean()
        self.user.first_name = self.prenom
        self.user.last_name = self.nom
        self.user.username = f"{self.email}"
        self.user.email = self.email
        self.user.save() 
        super().save(*args, **kwargs)
    
    def is_disponible(self, date, heure):
        rdv = RendezVous.objects.filter(medecin__pk=self.id, heure=heure, date=date, status='en-attente').first()
        return not bool(rdv)
    
class Service(models.Model):
    nom = models.CharField(max_length=255, choices=SERVICE_NAME_CHOICES, unique=True)
    chef = models.OneToOneField(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='chef_de_service')
    slug = models.CharField(max_length=255, null=True, blank=True, unique=True)


    def clean(self):
        if self.chef and self.chef.service and self.chef.service.pk != self.pk:
            raise ValidationError("chef_service must be from the current service")
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)
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
        rdv = RendezVous.objects.filter(salle__pk=self.id, heure=heure, date=date, status='en-attente').first()
        return not bool(rdv)


class RendezVous(models.Model):
    date = models.DateField(blank=True, null=True)
    heure = models.TimeField(blank=True, null=True)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default=STATUS_CHOICES[0][1], choices=STATUS_CHOICES)

    old_status = None

    def __str__(self):
        return f"RendezVous for {self.patient} with {self.medecin} on {self.date} at {self.heure}"
    
    def clean(self):
        if self.pk is not None:  # Check if the instance has already been saved
            original_instance = RendezVous.objects.get(pk=self.pk)
            self.old_status = original_instance.status  # Store the old status

            if self.old_status == dict(STATUS_CHOICES)["terminé"]:  # Check if original status is 'terminé'
                raise ValueError("Cannot modify a RendezVous with status 'terminé'")
        # else:    
        #     if self.date:
        #         current_datetime = timezone.now()
        #         date = datetime.strptime(self.date, "%Y-%m-%d").date()
        #         if date < current_datetime.date():
        #             raise ValidationError("Date must be greater than or equal to the current date.")
                
        #         if self.heure:
        #             heure = datetime.strptime(self.heure, "%H:%M").time()
        #             if self.date == current_datetime.date() and heure < current_datetime.time():
        #                 raise ValidationError("Heure must be greater than or equal to the current time.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
class Consultation(models.Model): 
    rendezvous = models.OneToOneField(RendezVous ,on_delete=models.CASCADE)
    diagnostique = models.TextField()
    prescription = models.TextField()

    @property
    def patient(self):
        return self.rendezvous.patient

    @property
    def medecin(self):
        return self.rendezvous.medecin

    def __str__(self):
        patient_name = self.rendezvous.patient
        doctor_name = self.rendezvous.medecin
        return f"Consultation: {patient_name} - {doctor_name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.rendezvous.status == dict(STATUS_CHOICES)["annulé"]:
                raise ValueError("Cannot create consultation for a RendezVous with status 'annulé'")
            self.rendezvous.status = dict(STATUS_CHOICES)["terminé"]  # Set status to 'terminé'
            self.rendezvous.save()  # Save the updated RendezVous instance
        super().save(*args, **kwargs)




