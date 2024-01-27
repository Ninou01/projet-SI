from datetime import datetime
import re
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.utils import timezone
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
)

User = get_user_model()

def validate_password_like_django(password):
  """
  Validates a password according to Django's criteria.

  Args:
    password: The password string to be validated.

  Returns:
    A list of error messages if the password is invalid, or an empty list if it's valid.
  """
  errors = []
  try:
    validate_password(password)
  except ValidationError as e:
    errors = e.messages
  return errors

def validateCreatePatient(POST):
    errors = []

    # Validate required string fields
    if not isinstance(POST.get('nom'), str) or not POST.get('nom'):
        errors.append("Nom is required and should be a non-empty string.")
    if not isinstance(POST.get('prenom'), str) or not POST.get('prenom'):
        errors.append("Prenom is required and should be a non-empty string.")
    if not isinstance(POST.get('adresse'), str) or not POST.get('adresse'):
        errors.append("Adresse is required and should be a non-empty string.")
    if not isinstance(POST.get('password'), str) or not POST.get('password'):
        errors.append("Password is required and should be a non-empty string.")
    else: 
        password_validation_errors = validate_password_like_django(POST.get('password'))
        errors += password_validation_errors

    # Validate phone number using regex
    phone_regex = re.compile(r"^(00213|\+213|0)(5|6|7)[0-9]{8}$")
    if not re.match(phone_regex, POST.get('num_tel')):
        errors.append("Invalid phone number format. It should match ^(00213|\+213|0)(5|6|7)[0-9]{8}$.")

    # Validate email format and uniqueness
    if not POST.get("email") or not isinstance(POST.get("email"), str):
        errors.append("Email is required and should be a non-empty string.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", POST.get("email")):
        errors.append("Invalid email format.")
    elif User.objects.filter(email=POST.get("email")).exists():
        errors.append("Email is already in use")

    # Validate date of birth
    
    if POST.get('dateNaissance'):
        dateNaissance = datetime.strptime(POST.get('dateNaissance'), "%Y-%m-%d").date()
        if dateNaissance > timezone.now().date():
            errors.append("Date of birth cannot be greater than today's date.")
    else: 
            errors.append("Date of birth cannot be null.")


    # Validate sexe against choices
    if POST.get('sexe') not in dict(SEXE_CHOICES).keys():
        errors.append("Invalid value for sexe. Please choose from the provided options.")


    # Return result
    return not bool(errors), errors

def validateUpdatePatient(POST, patient_instance):
    errors = []

    # Validate required string fields
    if POST.get("nom") and not isinstance(POST.get("nom"), str):
        errors.append("Nom is required and should be a non-empty string.")
    if POST.get("prenom") and not isinstance(POST.get("prenom"), str):
        errors.append("Prenom is required and should be a non-empty string.")
    if POST.get("adresse") and not isinstance(POST.get("adresse"), str):
        errors.append("Adresse is required and should be a non-empty string.")

    # Validate phone number using regex
    phone_regex = re.compile(r"^(00213|\+213|0)(5|6|7)[0-9]{8}$")
    if not re.match(phone_regex, POST.get('num_tel')):
        errors.append("Invalid phone number format. It should match ^(00213|\+213|0)(5|6|7)[0-9]{8}$.")

    # Validate email format and uniqueness
    if POST.get('email'):
        user = User.objects.get(email=POST.get('email'))
        if not isinstance(POST.get('email'), str):
            errors.append("Email is required and should be a non-empty string.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", POST.get('email')):
            errors.append("Invalid email format.")
        elif (user and patient_instance.user != user):
            errors.append("Email is already in use")

    # Validate date of birth
    if POST.get('dateNaissance'):
        dateNaissance = datetime.strptime(POST.get('dateNaissance'), "%Y-%m-%d").date()
        if dateNaissance > timezone.now().date():
            errors.append("Date of birth cannot be greater than today's date.")

    # Validate sexe against choices
    if POST.get('sexe') not in dict(SEXE_CHOICES).keys():
        errors.append("Invalid value for sexe. Please choose from the provided options.")

    # Return result
    return not bool(errors), errors

def validateCreateMedecin(POST):
    errors = []

    # Validate required string fields
    if not isinstance(POST.get('nom'), str) or not POST.get('nom'):
        errors.append("Nom is required and should be a non-empty string.")
    if not isinstance(POST.get('prenom'), str) or not POST.get('prenom'):
        errors.append("Prenom is required and should be a non-empty string.")
    if not isinstance(POST.get('adresse'), str) or not POST.get('adresse'):
        errors.append("Adresse is required and should be a non-empty string.")

    # Validate phone number using regex
    phone_regex = re.compile(r"^(00213|\+213|0)(5|6|7)[0-9]{8}$")
    if not re.match(phone_regex, POST.get('num_tel')):
        errors.append("Invalid phone number format. It should match ^(00213|\+213|0)(5|6|7)[0-9]{8}$.")

    # Validate specialite against choices
    if POST.get('specialite') not in dict(SPECIALITE_CHOICES).keys():
        errors.append("Invalid value for specialite. Please choose from the provided options.")

    # Validate service (if provided)
    if POST.get('service'):
        if POST.get('service') not in dict(SERVICE_NAME_CHOICES).keys():
            errors.append("Invalid value for service name. Please choose from the provided options.")
        else: 
            try:
                Service.objects.get(nom=POST.get('service'))
            except Service.DoesNotExist:
                errors.append("Invalid service.")

    # Validate email format and uniqueness
    if not POST.get('email') or not isinstance(POST.get('email'), str):
        errors.append("Email is required and should be a non-empty string.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", POST.get('email')):
        errors.append("Invalid email format.")
    elif User.objects.filter(email=POST.get('email')).exists():
        errors.append("Email is already in use")

    # Validate date of birth
    if POST.get('dateNaissance'):
        dateNaissance = datetime.strptime(POST.get('dateNaissance'), "%Y-%m-%d").date()
        if dateNaissance > timezone.now().date():
            errors.append("Date of birth cannot be greater than today's date.")
    else: 
            errors.append("Date of birth cannot be null.")

    # Validate sexe against choices
    if POST.get('sexe') not in dict(SEXE_CHOICES).keys():
        errors.append("Invalid value for sexe. Please choose from the provided options.")

    # Return result
    return not bool(errors), errors

def validateUpdateMedecin(POST, medecin_instance):
    errors = []

    # Validate required string fields
    if POST.get('nom') and not isinstance(POST.get('nom'), str):
        errors.append("Nom is required and should be a non-empty string.")
    if POST.get('prenom') and not isinstance(POST.get('prenom'), str):
        errors.append("Prenom is required and should be a non-empty string.")
    if POST.get('adresse') and not isinstance(POST.get('adresse'), str):
        errors.append("Adresse is required and should be a non-empty string.")

    # Validate phone number using regex
    phone_regex = re.compile(r"^(00213|\+213|0)(5|6|7)[0-9]{8}$")
    if POST.get('num_tel') and not re.match(phone_regex, POST.get('num_tel')):
        errors.append("Invalid phone number format. It should match ^(00213|\+213|0)(5|6|7)[0-9]{8}$.")

    # Validate specialite against choices
    if POST.get('specialite') and POST.get('specialite') not in dict(SPECIALITE_CHOICES).keys():
        errors.append("Invalid value for specialite. Please choose from the provided options.")

    # Validate service (if provided)
    if POST.get('service'):
        try:
            Service.objects.get(pk=POST.get('service'))
        except Service.DoesNotExist:
            errors.append("Invalid service.")

    # Validate email format and uniqueness
    if POST.get('email'):
        user = User.objects.get(email=POST.get('email'))
        if not isinstance(POST.get('email'), str):
            errors.append("Email is required and should be a non-empty string.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", POST.get('email')):
            errors.append("Invalid email format.")
        elif (user and medecin_instance.user != user):
            errors.append("Email is already in use")

    # Validate date of birth
    if POST.get('dateNaissance'):
        dateNaissance = datetime.strptime(POST.get('dateNaissance'), "%Y-%m-%d").date()
        if dateNaissance > timezone.now().date():
            errors.append("Date of birth cannot be greater than today's date.")

    # Validate sexe against choices
    if POST.get('sexe') and POST.get('sexe') not in dict(SEXE_CHOICES).keys():
        errors.append("Invalid value for sexe. Please choose from the provided options.")

    # Return result
    return not bool(errors), errors

# def validateCreateService(nom, chef_medecin):
#     errors = []

#     # Validate service name against choices
#     if nom not in dict(SERVICE_NAME_CHOICES).keys():
#         errors.append("Invalid value for service name. Please choose from the provided options.")

#     # Validate chef_medecin (if provided)
#     if chef_medecin:
#         try:
#             medecin = Medecin.objects.get(pk=chef_medecin)
#             if medecin.service:
#                 errors.append("Selected medecin is already assigned to another service.")
#         except Medecin.DoesNotExist:
#             errors.append("Invalid medecin.")

#     # Return result
#     return not bool(errors), errors

def validateUpdateService(POST, service_instance):
    errors = []

    # Validate service name against choices
    # if POST.get('nom') not in dict(SERVICE_NAME_CHOICES).keys():
    #     errors.append("Invalid value for service name. Please choose from the provided options.")

    # Validate chef_medecin (if provided)
    if POST.get('chef_medecin'):
        try:
            medecin = Medecin.objects.get(pk=POST.get('chef_medecin'))
            if medecin.service and medecin.service.pk != service_instance.pk:
                errors.append("Selected medecin is already assigned to another service.")
        except Medecin.DoesNotExist:
            errors.append("Invalid medecin.")

    # Return result
    return not bool(errors), errors

def validateCreateTache(POST):
    errors = []

    titre = POST.get('titre')
    if not titre and not titre.strip():
        errors.append("Titre is required and should be a non-empty string.")

    description = POST.get('description')
    if not description and not description.strip():
        errors.append("Description is required and should be a non-empty string.")

    # Validate service
    if POST.get('service') not in dict(SERVICE_NAME_CHOICES).keys():
        errors.append("Invalid value for service name. Please choose from the provided options.")

    # Return result
    return not bool(errors), errors

def validateUpdateTache(POST):
    errors = []

    titre = POST.get('titre')
    if not titre or not titre.strip():
        errors.append("Titre cannot be blank.")

    description = POST.get('description')
    if not description or not description.strip():
        errors.append("Description cannot be blank.")

    # Return result
    return not bool(errors), errors

def validateCreateSalle(POST):
    errors = []

    # Validate positive integer field
    if not POST.get('numero'):
            errors.append("numero is required and should be a non-empty int.")
    else: 
        try:
            numero = int(POST.get('numero'))
            if numero <= 0:
                errors.append("Numero should be a positive integer.")
            elif Salle.objects.filter(numero=numero).exists():
                errors.append("Salle with this numero already exists.")
        except: 
            errors.append("Numero should be a positive integer.")

    # Return result
    return not bool(errors), errors

def validateUpdateSalle(POST, salle_instance):
    errors = []

    if POST.get('numero'): 
        try:
            numero = int(POST.get('numero'))
            if numero <= 0:
                errors.append("Numero should be a positive integer.")
            elif Salle.objects.filter(numero=numero).exists():
                errors.append("Salle with this numero already exists.")
        except: 
            errors.append("Numero should be a positive integer.")

    # Return result
    return not bool(errors), errors

def validateCreateRendezVous(POST):
    errors = []

    # Check if all fields are provided
    required_fields = ['date', 'heure', 'medecin', 'patient', 'salle']
    missing_fields = [field for field in required_fields if not POST.get(field)]
    if missing_fields:
        errors.extend([f"{field.capitalize()} is required." for field in missing_fields])
    else:
        # Validate datetime fields
        current_datetime = timezone.now()
        if POST.get('date') < str(current_datetime.date()):
            errors.append("Date must be greater than or equal to the current date.")
        elif POST.get('date') == str(current_datetime.date()) and POST.get('heure') < str(current_datetime.time()):
            errors.append("Heure must be greater than or equal to the current time.")

        # Validate medecin and salle availability
        try:
            medecin = Medecin.objects.get(pk=POST.get('medecin'))
            if not medecin.is_disponible(POST.get('date'), POST.get('heure')):
                errors.append("Medecin is not available at the specified date and heure.")
        except Medecin.DoesNotExist:
            errors.append("Medecin not found.")

        try:
            salle = Salle.objects.get(pk=POST.get('salle'))
            if not salle.is_disponible(POST.get('date'), POST.get('heure')):
                errors.append("Salle is not available at the specified date and heure.")
        except Salle.DoesNotExist:
            errors.append("Salle not found.")

        try:
            patient = Patient.objects.get(pk=POST.get('patient'))
        except Patient.DoesNotExist:
            errors.append("Patient not found.")

    # Return result
    return not bool(errors), errors

def validateUpdateRendezVous(POST, rendezvous_instance):
    errors = []
    if rendezvous_instance.status == 'terminé':
            errors.append("Cannot update a RendezVous with status 'terminé'.")
    else:
        if not POST.get('status'):
            errors.append("Status is required for updating RendezVous.")
        else:
            status = POST['status']
            
            # Validate status against choices
            if status not in dict(STATUS_CHOICES).keys():
                errors.append("Invalid value for status. Please choose from the provided options.")

    # Return result
    return not bool(errors), errors

# def validateUpdateRendezVous(POST, rendezvous_instance):
#     errors = []

#     # Validate datetime fields
#     current_datetime = timezone.now()
#     if POST.get('date') and POST.get('date') < current_datetime.date():
#         errors.append("date must be greater than or equal to the current date.")
#     elif POST.get('heure') and POST.get('date') == current_datetime.date() and POST.get('heure') < current_datetime.time():
#         errors.append("Heure must be greater than or equal to the current time.")

#     # Validate medecin and salle availability
#     if medecin:
#         medecin = Medecin.objects.get(pk=medecin)
#         if medecin: 
#             errors.append("Medecin is not found.")

#         elif not medecin.is_disponible(POST.get('date'), POST.get('heure')):
#             errors.append("Medecin is not available at the specified date and heure.")

#     if salle:
#         salle = Salle.objects.get(pk=salle)
#         if salle: 
#             errors.append("Salle is not found.")

#         elif not salle.is_disponible(POST.get('date'), POST.get('heure')):
#             errors.append("Salle is not available at the specified date and heure.")

#     # Return result
#     return not bool(errors), errors

def validateCreateConsultation(POST):
    errors = []

    # Validate rendezvous and status
    if POST.get("rendezvous"): 
        try:
            rendezvous = RendezVous.objects.get(pk=POST.get("rendezvous"))
            if rendezvous: 
                if rendezvous.status == dict(STATUS_CHOICES)["annulé"]:  # Check if RendezVous is 'annulé'
                    errors.append("Cannot create consultation for a RendezVous with status 'annulé'.")
            if not POST.get('diagnostique'):
                errors.append("Diagnostique is required.")
            if not POST.get('prescription'):
                errors.append("Prescription is required.")
            
        except RendezVous.DoesNotExist:
            errors.append("Invalid RendezVous.")

        # Validate diagnostique and prescription
    else:
        errors.append("Rendez Vous is required.")

    # Return result
    return not bool(errors), errors

def validateUpdateConsultation(POST, consultation_instance):
    errors = []

    # Validate diagnostique if it is not blank in POST
    diagnostique = POST.get('diagnostique')
    if not diagnostique or not diagnostique.strip():
        errors.append("Diagnostique cannot be blank.")

    # Validate prescription if it is not blank in POST
    prescription = POST.get('prescription')
    if not prescription or not prescription.strip():
        errors.append("Prescription cannot be blank.")

    # Return result
    return not bool(errors), errors


