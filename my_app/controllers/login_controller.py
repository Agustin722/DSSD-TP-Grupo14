# my_app/controllers/auth_controller.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from my_app.schemas.login_schema import login_schema
from my_app.models.recolector import Recolector
from marshmallow import ValidationError

def login_view(request):
    if request.method == 'POST':
        form_data = {
            'dni': request.POST.get('dni'),
            'password': request.POST.get('password'),
        }
        
        # Validar datos con Marshmallow
        try:
            validated_data = login_schema.load(form_data)   
        except ValidationError as err:
            messages.error(request, f"Errores de validación: {err.messages}")
            return render(request, 'login.html')
        
        # Autenticar la inforacion obtenida con una base de datos con datos de recolectores(el dni es unico)
        try:
            user = Recolector.objects.get(dni=validated_data['dni'], password=validated_data['password'])
            login(request, user, backend='my_app.helpers.login_backend.DniAuthBackend')  # Inicia la sesion
            return redirect('submit-materials')  # Redirige al formulario de materiales
        except Recolector.DoesNotExist:
            messages.error(request, "Credenciales incorrectas")
    
    return render(request, 'login.html')