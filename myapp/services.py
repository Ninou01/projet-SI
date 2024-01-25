from django.contrib.auth import get_user_model
from .models import (
    Patient,
    Medecin,
    Tache,
    Service,
    Salle,
    RendezVous,
    Consultation,
)

User = get_user_model()

#####
# utils

def getServiceByName(nom):
    service = Service.objects.get(nom=nom)
    return service

def getMedecinById(id):
    medecin = Medecin.objects.get(id=id)
    return medecin

def getPatientById(id):
    patient = Patient.objects.get(id=id)
    return patient

def getSalleByNumero(numero):
    salle = Salle.objects.get(numero=numero)
    return salle

def getRendezVousById(id):
    rdv = RendezVous.objects.get(id=id)
    return rdv


###############
# create


def createUser(username, email, password):
    user = User.objects.create(username=username, email=email, password=password)
    return user
    
def createPatient(POST):
    username = f"{POST.get('email')}"
    email = POST.get('email')
    password = POST.get('password')
    user = createUser(username, email, password)
    patient = Patient.objects.create(
        user=user,
        nom=POST.get('nom'),
        prenom=POST.get('prenom'),
        adresse=POST.get('adresse'),
        num_tel=POST.get('num_tel'),
        email=POST.get('email'),
        sexe=POST.get('sexe'),
        dateNaissance=POST.get('dateNaissance'),
    )
    return patient

def createMedecin(POST):
    username = f"{POST.get('email')}"
    email = POST.get('email')
    password = POST.get('password')
    user = createUser(username, email, password)
    service = getServiceByName(POST.get('service'))
    medecin = Medecin.objects.create(
        user=user,
        service=service,
        nom=POST.get('nom'),
        prenom=POST.get('prenom'),
        adresse=POST.get('adresse'),
        num_tel=POST.get('num_tel'),
        email=POST.get('email'),
        sexe=POST.get('sexe'),
        dateNaissance=POST.get('dateNaissance'),
        specialite=POST.get('specialite'),
    )
    return medecin

def createTache(POST):
    titre = POST.get('titre')
    description = POST.get('description')
    service = getServiceByName(POST.get('service'))
    tache = Tache.objects.create(service=service, titre=titre, description=description)
    return tache

def createSalle(POST):
    numero = int(POST.get('numero'))
    salle = Salle.objects.create(numero=numero)
    return salle

def createRendezVous(POST):
    date = POST.get('date')
    heure = POST.get('heure')
    medecin = getMedecinById('medecin')
    patient = getPatientById('patient')
    salle = getSalleByNumero('salle')
    status = POST.get('status')

    rendezvous = RendezVous.objects.create(
        date=date,
        heure=heure,
        medecin=medecin,
        patient=patient,
        salle=salle,
        status=status,
    )
    return rendezvous

def createConsultation(POST):
    rendezvous=getRendezVousById(POST.get('rendezvous'))
    diagnostique=POST.get('diagnostique')
    prescription=POST.get('prescription')

    consultation = Consultation.objects.create(
        rendezvous=rendezvous,
        diagnostique=diagnostique,
        prescription=prescription,
    )
    return consultation


###############
# update


def updatePatient(patient_instance, POST):
    # Update Patient information
    patient_instance.nom = POST.get('nom')
    patient_instance.prenom = POST.get('prenom')
    patient_instance.adresse = POST.get('adresse')
    patient_instance.num_tel = POST.get('num_tel')
    patient_instance.email = POST.get('email')
    patient_instance.sexe = POST.get('sexe')
    patient_instance.dateNaissance = POST.get('dateNaissance')

    # Save changes
    patient_instance.save()

    return patient_instance

def updateMedecin(medecin_instance, POST):
    # Update Medecin information
    medecin_instance.nom = POST.get('nom')
    medecin_instance.prenom = POST.get('prenom')
    medecin_instance.adresse = POST.get('adresse')
    medecin_instance.num_tel = POST.get('num_tel')
    medecin_instance.email = POST.get('email')
    medecin_instance.sexe = POST.get('sexe')
    medecin_instance.dateNaissance = POST.get('dateNaissance')
    medecin_instance.specialite = POST.get('specialite')

    # Update Service if necessary
    service_name = POST.get('service')
    if service_name:
        service = getServiceByName(service_name)
        if service:
            medecin_instance.service = service

    # Save changes
    medecin_instance.save()

    return medecin_instance

def updateService(service_instance, POST):

    # Update Chef Medecin if necessary
    chef_medecin_id = POST.get('chef_medecin')
    if chef_medecin_id:
        chef_medecin = getMedecinById(chef_medecin_id)
        service_instance.chef = chef_medecin

    service_instance.save()

    return service_instance

def updateTache(tache_instance, POST):
    # Update Tache information
    tache_instance.titre = POST.get('titre')
    tache_instance.description = POST.get('description')

    # Save changes
    tache_instance.save()

    return tache_instance


def updateRendezVous(rendezvous_instance, POST):
    # Update RendezVous information
    rendezvous_instance.date = POST.get('date')
    rendezvous_instance.heure = POST.get('heure')
    rendezvous_instance.status = POST.get('status')

    # Update Medecin if necessary
    medecin_id = POST.get('medecin')
    if medecin_id:
        try:
            medecin = Medecin.objects.get(pk=medecin_id)
            rendezvous_instance.medecin = medecin
        except Medecin.DoesNotExist:
            raise ValueError("Invalid medecin.")

    # Update Patient if necessary
    patient_id = POST.get('patient')
    if patient_id:
        try:
            patient = Patient.objects.get(pk=patient_id)
            rendezvous_instance.patient = patient
        except Patient.DoesNotExist:
            raise ValueError("Invalid patient.")

    # Update Salle if necessary
    salle_numero = POST.get('salle')
    if salle_numero:
        salle = getSalleByNumero(salle_numero)
        if salle:
            rendezvous_instance.salle = salle

    # Save changes
    rendezvous_instance.save()

    return rendezvous_instance

def updateConsultation(consultation_instance, POST):
    # Update Consultation information
    consultation_instance.diagnostique = POST.get('diagnostique')
    consultation_instance.prescription = POST.get('prescription')

    # Save changes
    consultation_instance.save()

    return consultation_instance

