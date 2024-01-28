from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def adminonly(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_func


def admin_or_medecin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or hasattr(request.user, 'medecin'):
                return view_func(request, *args, **kwargs)
        return redirect('/')  # Redirect to the specified URL if not admin or medecin
    return wrapper_func

def admin_or_medecin_concerned(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or (hasattr(request.user, 'medecin') and str(request.user.medecin.id) == kwargs.get('id')):
                return view_func(request, *args, **kwargs)
        return redirect('/')  # Redirect to the specified URL if not admin or medecin with the correct ID
    return wrapper_func

def admin_or_patient_concerned(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or (hasattr(request.user, 'patient') and str(request.user.patient.id) == kwargs.get('id')):
                return view_func(request, *args, **kwargs)
        return redirect('/')  # Redirect to the specified URL if not admin or medecin with the correct ID
    return wrapper_func

def admin_or_concerned(model):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_staff:
                    return view_func(request, *args, **kwargs)

                instance = get_object_or_404(model, pk=kwargs.get('id'))

                if hasattr(request.user, 'medecin') and request.user.medecin == instance.medecin:
                    return view_func(request, *args, **kwargs)

                if hasattr(request.user, 'patient') and request.user.patient == instance.patient:
                    return view_func(request, *args, **kwargs)

            return redirect('/')  # Redirect to the specified URL if not admin or concerned user
        return wrapper_func
    return decorator


