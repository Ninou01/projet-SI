from django.contrib import admin
from .models import (
    Patient,
    Medecin,
    Service,
    Tache,
    Salle,
    RendezVous,
    Consultation,
)

# Register your models here.

admin.site.register(Patient)
admin.site.register(Medecin)
admin.site.register(Service)
admin.site.register(Tache)
admin.site.register(Salle)
admin.site.register(RendezVous)
admin.site.register(Consultation)
