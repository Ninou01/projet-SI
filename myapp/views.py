from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render

from .validations import (
    validateCreateConsultation,
    validateCreateMedecin,
    validateCreatePatient,
    validateCreateRendezVous,
    validateCreateSalle,
    validateCreateTache,
    validateUpdateConsultation,
    validateUpdateMedecin,
    validateUpdatePatient,
    validateUpdateRendezVous,
    validateUpdateService,
    validateUpdateTache
)
from .services import (
    createConsultation,
    createMedecin,
    createPatient,
    createRendezVous,
    createSalle,
    updateConsultation,
    updateMedecin,
    updatePatient,
    updateRendezVous,
    updateTache
)
from .models import (
    SEXE_CHOICES, 
    SPECIALITE_CHOICES,
    SERVICE_NAME_CHOICES,
    STATUS_CHOICES,
    Patient,
    Medecin,
    Service,
    Salle,
    RendezVous,
    Consultation,
    Tache,
) 

# Create your views here.

def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)


def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)

def home(request):
    return render(request, "home.html")

##############################################################################
# services

def AllServices(request):
    services = Service.objects.all()

    context = {
        'services': services,
        'test': 'test'

    }
    return render(request, 'service/AllServices.html', context)

def OneService(request, id):
    service = get_object_or_404(Service, id=id)
    context = {
        'service': service,
    }
    return render(request, 'service/OneService.html', context)

def UpdateService(request, id):
    # Get the Service instance or return a 404 error if not found
    service_id = id
    service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        # Validate the update using your validation function
        is_valid, errors = validateUpdateService(request.POST, service)

        if is_valid:
            # Update the Service instance
            chef_medecin_id = request.POST.get('chef_medecin')
            if chef_medecin_id:
                service.chef = Medecin.objects.get(pk=chef_medecin_id)
            else:
                service.chef = None
            
            service.save()

            # Redirect to a success page or another appropriate page
            return redirect(f'/services/{id}')
        else:
            # If validation fails, render the form with error messages
            medecins = Medecin.objects.filter(service=service)
            context = {
                'service': service, 
                'medecins': medecins, 
                'errors': errors
            }
            return render(request, 'service/UpdateService.html', {'service': service, 'medecins': medecins, 'errors': errors})

    else:
        # If it's a GET request, render the form with current data
        errors = []
    
    # Get the list of medecins associated with the service for the dropdown
    medecins = Medecin.objects.filter(service=service)
    context = {
        'service': service, 
        'medecins': medecins, 
        'errors': errors
    }
    return render(request, 'service/UpdateService.html', context)

def AllServiceTaches(request, id):
    service_id = id
    service = get_object_or_404(Service, id=service_id)
    taches = Tache.objects.filter(service=service)

    context = {
        'taches': taches,
    }
    return render(request, 'tache/AllTaches.html', context)

##############################################################################
# medecins

def AllMedecins(request):
    medecins = Medecin.objects.all()

    context = {
        'medecins': medecins,
        'test': 'test'

    }
    return render(request, 'medecin/AllMedecins.html', context)

def OneMedecin(request, id):
    medecin = get_object_or_404(Medecin, id=id)
    context = {
        'medecin': medecin,
    }
    return render(request, 'medecin/OneMedecin.html', context)

def AddMedecin(request):
    context = {
        "services": dict(SERVICE_NAME_CHOICES),
        "specialites": dict(SPECIALITE_CHOICES),
        "errors": None,
    }
    if request.method == 'POST':

        # Validate the data
        is_valid, errors = validateCreateMedecin(request.POST)

        if is_valid:
            medecin = createMedecin(request.POST)
            # Redirect to the home page or another appropriate page
            return redirect('/medecins')
        else:
            # Data is not valid, render the form with error messages
            context['errors'] = errors
            return render(request, 'medecin/AddMedecin.html', context)

    # If it's a GET request, just render the form
    return render(request, 'medecin/AddMedecin.html', context)

def UpdateMedecin(request, id):
    medecin_id = id
    # Get the Medecin instance or return a 404 error if not found
    medecin_instance = get_object_or_404(Medecin, pk=medecin_id)

    if request.method == 'POST':
        # Validate the update using your validation function
        is_valid, errors = validateUpdateMedecin(request.POST, medecin_instance)

        if is_valid:
            # Update the Medecin instance
            updated_medecin = updateMedecin(medecin_instance, request.POST)

            # Redirect to a success page or another appropriate page
            return redirect(f'/medecins/{medecin_id}')
        else:
            # If validation fails, render the form with error messages
            services = Service.objects.all()  # Get all services for dropdown
            return render(request, 'medecin/UpdateMedecin.html', {'medecin': medecin_instance, 'services': services, 'errors': errors, 'SPECIALITE_CHOICES': SPECIALITE_CHOICES})

    else:
        # If it's a GET request, render the form with current data
        errors = []
        services = Service.objects.all()  # Get all services for dropdown

    return render(request, 'medecin/UpdateMedecin.html', {'medecin': medecin_instance, 'services': services, 'errors': errors, 'SPECIALITE_CHOICES': SPECIALITE_CHOICES})

def AllMedecinRendezVous(request, id):
    medecin_id = id
    medecin = get_object_or_404(Medecin, id=medecin_id)
    rendezVous = RendezVous.objects.filter(medecin=medecin)

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllMedecinRendezVousEnAttente(request, id):
    medecin_id = id
    medecin = get_object_or_404(Medecin, id=medecin_id)
    rendezVous = RendezVous.objects.filter(medecin=medecin, status='en-attente')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllMedecinRendezVousAnnule(request, id):
    medecin_id = id
    medecin = get_object_or_404(Medecin, id=medecin_id)
    rendezVous = RendezVous.objects.filter(medecin=medecin, status='annulé')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllMedecinRendezVousTemrine(request, id):
    medecin_id = id
    medecin = get_object_or_404(Medecin, id=medecin_id)
    rendezVous = RendezVous.objects.filter(medecin=medecin, status='terminé')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllMedecinRendezVous(request, id):
    medecin_id = id
    medecin = get_object_or_404(Medecin, id=medecin_id)
    rendezVous = RendezVous.objects.filter(medecin=medecin)
    consultations = []
    for rdv in rendezVous:
        try:
            consultation = rdv.consultation
            consultations.append(consultation)
        except Consultation.DoesNotExist:
            pass

    context = {
        'rendezVous': rendezVous,
        # 'consultation': consultation,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllMedecinConsultations(request, id):
    medecin_id = id
    medecin = get_object_or_404(Medecin, id=medecin_id)
    rendezVous = RendezVous.objects.filter(medecin=medecin)
    consultations = []
    for rdv in rendezVous:
        try:
            consultation = rdv.consultation
            consultations.append(consultation)
        except Consultation.DoesNotExist:
            pass

    context = {
        # 'rendezVous': rendezVous,
        'consultations': consultations,
    }
    return render(request, 'consultation/AllConsultations.html', context)



##############################################################################
# patients

def AllPatients(request):
    patients = Patient.objects.all()

    context = {
        'patients': patients,
        'test': 'test'

    }
    return render(request, 'patient/AllPatients.html', context)

def OnePatient(request, id):
    patient = get_object_or_404(Patient, id=id)
    context = {
        'patient': patient,
    }
    return render(request, 'patient/OnePatient.html', context)

def AddPatient(request):
    if request.method == 'POST':

        # Validate the data
        is_valid, errors = validateCreatePatient(request.POST)

        if is_valid:
            # Data is valid, create a new patient
            patient = createPatient(request.POST)
            # Redirect to the home page
            return redirect('/patients')
        else:
            # Data is not valid, render the form with error messages
            return render(request, 'patient/AddPatient.html', {'errors': errors})

    # If it's a GET request, just render the form
    return render(request, 'patient/AddPatient.html')

def UpdatePatient(request, id):
    # Retrieve the patient instance
    patient_id = id
    patient = Patient.objects.get(pk=patient_id)

    if request.method == 'POST':
        # Validate the update data
        is_valid, errors = validateUpdatePatient(request.POST, patient)

        if is_valid:
            # Update the patient
            updatePatient(patient, request.POST)
            return redirect(f'/patients/{patient_id}')  # Redirect to the home page after successful update
        else:
            # If validation fails, render the form with error messages
            return render(request, 'patient/UpdatePatient.html', {'patient': patient, 'errors': errors})
    else:
        # If it's a GET request, render the form with the current patient data
        return render(request, 'patient/UpdatePatient.html', {'patient': patient, 'errors': []})

def AllPatientRendezVous(request, id):
    patient_id = id
    patient = get_object_or_404(Patient, id=patient_id)
    rendezVous = RendezVous.objects.filter(patient=patient)

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllPatientRendezVousEnAttente(request, id):
    patient_id = id
    patient = get_object_or_404(Patient, id=patient_id)
    rendezVous = RendezVous.objects.filter(patient=patient, status='en-attente')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllPatientRendezVousAnnule(request, id):
    patient_id = id
    patient = get_object_or_404(Patient, id=patient_id)
    rendezVous = RendezVous.objects.filter(patient=patient, status='annulé')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllPatientRendezVousTemrine(request, id):
    patient_id = id
    patient = get_object_or_404(Patient, id=patient_id)
    rendezVous = RendezVous.objects.filter(patient=patient, status='terminé')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)


def AllPatientConsultations(request, id):
    patient_id = id
    patient = get_object_or_404(Patient, id=patient_id)
    rendezVous = RendezVous.objects.filter(patient=patient)
    consultations = []
    for rdv in rendezVous:
        try:
            consultation = rdv.consultation
            consultations.append(consultation)
        except Consultation.DoesNotExist:
            pass

    context = {
        # 'rendezVous': rendezVous,
        'consultations': consultations,
    }
    return render(request, 'consultation/AllConsultations.html', context)


##############################################################################
# Salles
def AllSalles(request):
    salles = Salle.objects.all()

    context = {
        'salles': salles,
        'test': 'test'

    }
    return render(request, 'salle/AllSalles.html', context)

def AddSalle(request):
    if request.method == 'POST':

        # Validate the data
        is_valid, errors = validateCreateSalle(request.POST)

        if is_valid:
            # Data is valid, create a new salle
            salle = createSalle(request.POST)
            # Redirect to the home page or another appropriate page
            return redirect('/salles')
        else:
            # Data is not valid, render the form with error messages
            return render(request, 'salle/AddSalle.html', {'errors': errors})

    # If it's a GET request, just render the form
    return render(request, 'salle/AddSalle.html')

def AllSalleRendezVous(request, id):
    salle_id = id
    salle = get_object_or_404(Salle, id=salle_id)
    rendezVous = RendezVous.objects.filter(salle=salle)

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllSalleRendezVousEnAttente(request, id):
    salle_id = id
    salle = get_object_or_404(Salle, id=salle_id)
    rendezVous = RendezVous.objects.filter(salle=salle, status='en-attente')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllSalleRendezVousAnnule(request, id):
    salle_id = id
    salle = get_object_or_404(Salle, id=salle_id)
    rendezVous = RendezVous.objects.filter(salle=salle, status='annulé')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def AllSalleRendezVousTemrine(request, id):
    salle_id = id
    salle = get_object_or_404(Salle, id=salle_id)
    rendezVous = RendezVous.objects.filter(salle=salle, status='terminé')

    context = {
        'rendezVous': rendezVous,
    }
    return render(request, 'rendezvous/AllRendezVous.html', context)



##############################################################################
# consultations

def AllConsultations(request):
    consultations = Consultation.objects.all()

    context = {
        'consultations': consultations,
        'test': 'test'

    }
    return render(request, 'consultation/AllConsultations.html', context)

def OneConsultation(request, id):
    consultation = get_object_or_404(Consultation, id=id)
    context = {
        'consultation': consultation,
    }
    return render(request, 'consultation/OneConsultation.html', context)

def AddConsultation(request, id):
    rendezvous_id = id
    rdv = get_object_or_404(RendezVous, id=rendezvous_id)

    context = {
        'rendezvous_id': rendezvous_id,
        'errors': None
    }
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        # request.POST['rendezvous'] = rendezvous_id
        is_valid, errors = validateCreateConsultation(request.POST)

        # Check if the form is valid
        if is_valid:
            # Create a Consultation instance but don't save it yet
            consultation = createConsultation(request.POST)

            # Redirect to a success page or another appropriate page
            return redirect(f'/rendezvous/{rendezvous_id}')
        else:
            context['errors'] = errors
            return render(request, 'consultation/AddConsultation.html', context)

    if rdv and rdv.status == 'annulé':
        return redirect(f'/rendezvous/{rendezvous_id}')
    
    return render(request, 'consultation/AddConsultation.html', context)

def UpdateConsultation(request, id):
    consultation_id = id
    consultation_instance = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST':
        is_valid, errors = validateUpdateConsultation(request.POST, consultation_instance)

        if is_valid:
            # Update consultation
            updateConsultation(consultation_instance, request.POST)
            
            # Redirect to the consultation page or any other desired page
            return redirect(f'/consultations/{id}')
        else:
            # If validation fails, render the update page with errors
            return render(request, 'consultation/UpdateConsultation.html', {'consultation': consultation_instance, 'errors': errors})

    # If it's a GET request, render the form with the current consultation data
    return render(request, 'consultation/UpdateConsultation.html', {'consultation': consultation_instance})

##############################################################################
# RendezVous

def AllRendezVous(request):
    rendezvous = RendezVous.objects.all()

    context = {
        'rendezVous': rendezvous,
        'test': 'test'

    }
    return render(request, 'rendezvous/AllRendezVous.html', context)

def OneRendezVous(request, id):
    rendezvous = get_object_or_404(RendezVous, id=id)
    context = {
        'rendezvous': rendezvous,
    }
    return render(request, 'rendezvous/OneRendezVous.html', context)


def SelectDatetime(request):
    if request.method == 'POST':
        # Get date and time from the form
        date = request.POST.get('date')
        heure = request.POST.get('heure')

        # Convert the date and time to a datetime object
        datetime_str = f'{date} {heure}'
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        # Retrieve all Medecins and salles
        all_medecins = Medecin.objects.all()
        all_salles = Salle.objects.all()

        # Filter available medecins and salles in Python
        available_medecins = [medecin for medecin in all_medecins if medecin.is_disponible(datetime_obj.date(), datetime_obj.time())]
        available_salles = [salle for salle in all_salles if salle.is_disponible(datetime_obj.date(), datetime_obj.time())]
        patients = Patient.objects.all()
        
        
        context = {
            'medecins': available_medecins, 
            'salles': available_salles, 
            'patients': patients, 
            'datetime': datetime_obj, 
            'date': date, 
            'heure': heure
        }
        return render(request, 'rendezvous/AddRendezVous.html', context)

    # If it's a GET request, just render the form
    return render(request, 'rendezvous/SelectDatetime.html')

def AddRendezVous(request):
    if request.method == 'POST':
        context = {
            'errors': None, 
            # 'date': request.POST.get('date'), 
            # 'heure': request.POST.get('heure')
        }

        # Validate the data
        is_valid, errors = validateCreateRendezVous(request.POST)

        if is_valid:
            # Data is valid, create a new rendezvous for each selected medecin and salle
            rdv = createRendezVous(request.POST)
            
            # Redirect to the home page or another appropriate page
            return redirect('/rendezvous')
        else:
            # Data is not valid, render the form with error messages
            context['errors'] = errors
            return render(request, 'rendezvous/SelectDatetime.html', context)

    # If it's a GET request, redirect to the available options page
    return redirect('/rendezvous/selectdatetime')

def deleterdv(request, id):
    instance = RendezVous.objects.get(id=id)
    instance.delete()
    return redirect("/rendezvous/")


def UpdateRendezVous(request, id):
    # Get the RendezVous instance
    rendezvous_id = id
    rendezvous_instance = get_object_or_404(RendezVous, pk=rendezvous_id)

    # Handle POST request
    if request.method == 'POST':
        # Validate the update
        is_valid, errors = validateUpdateRendezVous(request.POST, rendezvous_instance)

        if is_valid:
            # Update the RendezVous
            updateRendezVous(rendezvous_instance, request.POST)
            return redirect(f'/rendezvous/{id}')  # Redirect to the RendezVous list page after successful update
        else:
            # If validation fails, render the form with error messages
            return render(request, 'rendezvous/UpdateRendezVous.html', {'errors': errors, 'rendezvous': rendezvous_instance})

    # Handle GET request
    if rendezvous_instance and rendezvous_instance.status == 'terminé':
        return redirect(f'/rendezvous/{rendezvous_id}')
    return render(request, 'rendezvous/UpdateRendezVous.html', {'rendezvous': rendezvous_instance, 'status_choices': STATUS_CHOICES})


##############################################################################
# Tache

def AllTaches(request):
    taches = Tache.objects.all()

    context = {
        'taches': taches,
    }
    return render(request, 'tache/AllTaches.html', context)

def OneTache(request, id):
    tache = get_object_or_404(Tache, id=id)
    context = {
        'tache': tache,
    }
    return render(request, 'tache/OneTache.html', context)

def AddTache(request):
    # Handle POST request
    if request.method == 'POST':
        # Validate the creation
        is_valid, errors = validateCreateTache(request.POST)

        if is_valid:
            # Create the Tache
            service = get_object_or_404(Service, nom=request.POST.get('service'))
            Tache.objects.create(
                titre=request.POST.get('titre'),
                description=request.POST.get('description'),
                service=service
            )
            return redirect('/taches')  # Redirect to the Tache list page after successful creation
        else:
            # If validation fails, render the form with error messages
            return render(request, 'tache/AddTache.html', {'errors': errors, 'services': SERVICE_NAME_CHOICES})

    # Handle GET request
    return render(request, 'tache/AddTache.html', {'services': SERVICE_NAME_CHOICES})

def UpdateTache(request, id):
    tache_id = id
    tache_instance = get_object_or_404(Tache, pk=tache_id)

    if request.method == 'POST':
        # Validate the update using the provided function
        is_valid, errors = validateUpdateTache(request.POST)

        if is_valid:
            # Update the Tache instance
            updated_tache = updateTache(tache_instance, request.POST)
            
            # Redirect to a success page or the Tache details page
            return redirect(f'/taches/{tache_id}', tache_id=updated_tache.id)
        else:
            # If validation fails, render the same page with error messages
            return render(request, 'tache/UpdateTache.html', {'errors': errors, 'tache': tache_instance})
    else:
        # If it's a GET request, simply render the UpdateTache.html template with the Tache instance
        return render(request, 'tache/UpdateTache.html', {'tache': tache_instance})
