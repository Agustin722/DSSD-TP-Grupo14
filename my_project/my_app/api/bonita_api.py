import requests
from my_app.helpers.auth_helper import authenticate_bonita
from django.conf import settings

def start_bonita_process(process_definition_id, variables):
    bonita_url = getattr(settings, 'BONITA_URL', 'http://localhost:8080/bonita')
    url = f"{bonita_url}/API/bpm/process/{process_definition_id}/instantiation"
    
    # Autenticar y obtener cookies
    session_cookies = authenticate_bonita()
    
    # Formatear las variables para Bonita
    bonita_variables = []
    for var in variables:
        bonita_variables.append({
            "name": f"material_{var['tipo_material']}_cantidad",
            "value": var['cantidad']
        })
    
    payload = {
        "variables": bonita_variables
    }
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    response = requests.post(url, json=payload, cookies=session_cookies, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al iniciar el proceso en Bonita: {response.text}")
