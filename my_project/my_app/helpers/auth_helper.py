import requests
from django.conf import settings

def authenticate_bonita():
    bonita_url = getattr(settings, 'BONITA_URL', 'http://localhost:8080/bonita')
    username = getattr(settings, 'BONITA_USER', 'walter.bates')
    password = getattr(settings, 'BONITA_PASSWORD', 'bpm')
    
    login_url = f"{bonita_url}/loginservice"
    payload = {
        "username": username,
        "password": password,
        "redirect": "false"
    }
    
    response = requests.post(login_url, data=payload)
    if response.status_code == 200:
        return response.cookies
    else:
        raise Exception("Error de autenticación con Bonita")
